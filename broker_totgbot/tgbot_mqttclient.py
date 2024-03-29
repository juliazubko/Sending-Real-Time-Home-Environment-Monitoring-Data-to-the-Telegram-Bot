import asyncio
import paho.mqtt.client as mqtt
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
from datetime import datetime, timedelta
 

class TelegramMqttClient:
    def __init__(self, broker, port, topic, bot_token, chat_id):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.data = None
        self.last_received = datetime.now()

        # Set up MQTT client and callbacks
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Set up Telegram bot
        self.bot = Bot(token=self.bot_token)
        self.dp = Dispatcher(self.bot)
        self.dp.register_message_handler(self.get_sensor_data, Command("get_sensor_data"))
        self.dp.register_message_handler(self.get_status, Command("status"))

    # Define MQTT callback functions
    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        try:
            # Parse the incoming message
            self.data = msg.payload.decode("utf-8")
            self.last_received = datetime.now()
        except Exception as e:
            print(e)

    async def send_telegram_message(self, message_text: str):
        await self.bot.send_message(chat_id=self.chat_id, text=message_text)

    async def get_sensor_data(self, message: types.Message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if self.data is not None:
            temp_analog, temp_dht, humidity = map(float, self.data.split(','))

            # Format the data
            message_text = f"Timestamp: {timestamp}" \
                           f"\nTemperature (Analog): {temp_analog}°C" \
                           f"\nTemperature (DHT): {temp_dht}°C" \
                           f"\nHumidity: {humidity}%"
        else:
            message_text = f"Timestamp: {timestamp}" \
                           f"\nTemperature (Analog): NA" \
                           f"\nTemperature (DHT): NA" \
                           f"\nHumidity: NA"

        # Send the data to the Telegram bot
        await self.send_telegram_message(message_text)

    async def get_status(self, message: types.Message):
        # Consider the station to be offline if no message was received in the last 5 minutes
        # temporary solution
        if datetime.now() - self.last_received > timedelta(minutes=1):
            await self.send_telegram_message("The home station is currently offline.")
        else:
            await self.send_telegram_message("The home station is online.")

    def run(self):
        loop = asyncio.get_event_loop()

        # Connect to the MQTT broker and start the loop
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

        # Start polling updates from Telegram
        loop.run_until_complete(self.dp.start_polling())

        # Prevent the script from exiting immediately
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            # On Keyboard interrupt, disconnect MQTT client
            self.client.disconnect()


if __name__ == "__main__":
    mqtt_broker = "broker.hivemq.com"
    mqtt_port = 1883
    mqtt_topic = "topic-test-1"
    bot_token = "...put your bot token here (get one from BotFather on bot creation)"
    chat_id = "... your chat id here (run get_chat_id code if you dont know your chat_id)"    

    handler = TelegramMqttClient(mqtt_broker, mqtt_port, mqtt_topic, bot_token, chat_id)
    handler.run()
