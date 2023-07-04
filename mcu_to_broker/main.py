import machine as m
import time
from umqttsimple import MQTTClient
import network  
from credentials import secrets  
from sensorreader import SensorReader  


WIFI_SSID  = secrets["ssid"] 
WIFI_PASS = secrets["password"]  

BROKER = "broker.hivemq.com"  
PORT = 1883
CLIENT_ID = "pick a name for your cliet, ie 'pico-test'"
TOPIC = "choose a topic to publish, ie 'sensordata'"
CONNECTED_TOPIC = "connected" # diagnistic, shows that the your MCU client is connected to broker

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm = 0xa11140) 
wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected() and wlan.status() >= 0:
    print('.', end='')
    time.sleep(1)
                
# Print the IP assigned by router
ip = wlan.ifconfig()[0]
print('\nConnected on {}'.format(ip)) 
time.sleep(5)   

# Check if the IP address is 0.0.0.0 (optional)
if ip == "0.0.0.0":
    print("Error: No valid IP address assigned.")
else:
    time.sleep(5) 

    client = MQTTClient(CLIENT_ID, BROKER, PORT) 
    client.connect()  
    client.publish(CONNECTED_TOPIC, "{} connected".format(CLIENT_ID))  

    # Create a SensorReader object
    reader = SensorReader(22, 27)  # DHT sensor on pin 22, analog sensor on pin 27
    led = m.Pin("LED", m.Pin.OUT)  # diagnostic, on when sending message 
    led.off()    

    while True:
        led.on()

        # Use the SensorReader to read the sensor data
        temp_analog = reader.read_analog_temp()
        temp_dht, humidity = reader.read_dht()

        # Publish the sensor data
        if temp_analog is not None and temp_dht is not None and humidity is not None:
            message = '{},{},{}'.format(temp_analog, temp_dht, humidity)
            client.publish(TOPIC, message)

        # delay, not to overflow (so sends every 4 seconds)
        time.sleep(2)
        led.off()
        time.sleep(2)

    # Disconnect from the MQTT broker
    client.disconnect()  

    