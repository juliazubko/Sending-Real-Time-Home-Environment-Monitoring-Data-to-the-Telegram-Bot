import sqlite3
import paho.mqtt.client as mqtt


class MQTTDatabaseHandler:
    def __init__(self, broker, port, topic, db_file, table_name):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.db_file = db_file
        self.table_name = table_name

        # Set up MQTT client and callbacks
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Create tables in SQLite database
        self.create_tables()

    def create_tables(self):
        # Create a connection to SQLite database
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Create tables in SQLite database
        c.execute('''CREATE TABLE IF NOT EXISTS {} (
                    id INTEGER PRIMARY KEY,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    temp_analog REAL,
                    temp_dht INTEGER,
                    humidity INTEGER) '''.format(self.table_name))

        conn.commit()
        conn.close()

    # Define MQTT callback functions
    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        try:
            # Parse the incoming message
            data = msg.payload.decode("utf-8")
            temp_analog, temp_dht, humidity = map(float, data.split(','))

            # Create a new SQLite connection for this thread
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()

            # Insert the data into the SQLite database
            c.execute("INSERT INTO {} (temp_analog, temp_dht, humidity) VALUES (?, ?, ?)".format(self.table_name),
                      (temp_analog, temp_dht, humidity))

            conn.commit()
            conn.close()
        except Exception as e:
            pass

    def run(self):
        # Connect to the MQTT broker and start the loop
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

        # Prevent the script from exiting immediately
        try:
            while True:
                pass
        except KeyboardInterrupt:
            # On Keyboard interrupt, disconnect MQTT client
            self.client.disconnect()
