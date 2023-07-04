**(in progress)** 

*This project is a practical part of the "Applied IoT" summer course offered by Linnaeus University (23ST - 1DT305).*





**Name**: xx yy XX222X

# Project Description

This project is a prototype designed to monitor the home environment using IoT devices and the MQTT protocol. The current setup involves a DHT11 digital temperature and humidity sensor and a TO-92 analogue temperature sensor, both connected to a Raspberry Pi Pico W microcontroller unit (MCU). 

The sensor data is transmitted via Wi-Fi using the MQTT protocol, which typically operates over TCP/IP and is used to transport lightweight messages between devices, to a free online public HiveMQ MQTT broker. 

A local SQLite database client subscribes to the HiveMQ broker, retrieves the sensor messages, and stores them in a table. Another thread in the same process retrieves the SQL table data and displays it in real-time as several time-series line plots on a Dash dashboard. 

Additionally, a Telegram bot client also subscribes to the HiveMQ broker and provides current sensor data to the user on demand. 

The project is currently in progress, with one of the goals of enhancing the Telegram bot's functionality to also display plots or dashboards that provide insights into the sensor data. 

The ultimate objective is to develop a fully autonomous system that can operate without manual intervention. This involves connecting additional environment monitoring sensors, ensuring that the MCU with connected sensors can operate on battery power, and setting up a local MQTT broker.

As the project requirements evolve, the necessity of the MQTT-to-SQL + SQL-to-Dash process may diminish. One consideration is to send a simple screenshot in .png format of the current time-series line plots via the Telegram bot. However, further investigation into available data visualization options is required to determine the most effective approach.

Once these components are finalized, they will be packaged into a container for efficient, concurrent execution.

## Project Duration

A beginner in hardware, sensors, and network concepts might expect an estimated completion time of around 5 weeks, assuming a relaxed pace within a standard 40-hour work week.


## Project Objective

This project is driven by a genuine interest in IoT and the significant potential of real-time data monitoring. 

Despite the existence of numerous similar projects, the primary objective here is to personally recreate and understand the steps involved in generating and visualizing real-time environmental data from a domestic setting. This approach offers a deeper understanding of the process compared to using ready-to-use automated solutions currently available in the market.

The data collected from the sensors can be accessed remotely via a Telegram app bot, which was chosen as a beginner-friendly and easy-to-set-up alternative to creating a mobile app for home environment monitoring. 

Insights derived from real-time environmental data can be used to make adjustments for improved comfort and energy efficiency. The immediacy of the data also potentially allows for prompt responses to any significant changes in the environment.     

## List of Materials
- Raspberry Pi Pico WH
- Breadboard 840 connections
- USB cable A-male – micro B 5p male 1.8m
- 20x 41012684 Lab cable 30cm male/male
- Digital temperature and humidity sensor DHT11
- MCP9700 TO-92 Temperature sensor (analogue)   




## Short Specifications

| Material                                             | Description                                                                                                                     |
|--------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| Raspberry Pi Pico WH                        | RP2040 CPU, ARM Cortex-M0+ 133MHz, 256kB RAM, 30 GPIO pins, 2MB on-board QSPI Flash, CYW43439 wireless chip, IEEE 802.11 b/g/n wireless LAN, delivered with soldered 40-pin header |
| Breadboard with 840 Connection Points | Breadboard with 840 connection points                                                                                            |
| USB Cable A-Male to Micro B 5-Pin Male, 1.8m | USB cable, A-male to micro B 5-pin male, 1.8m                                                                                   |
| 20-Pack of Jumper Wires, 30cm, Male-to-Male | 20-pack of jumper wires, 30cm, male-to-male                                                                                     |
| Digital Temperature and Humidity Sensor DHT11   | A sensor module that measures temperature and relative humidity. [Detailed DHT11 datasheet](https://www.electrokit.com/uploads/productfile/41016/DHT11.pdf) |
| MCP9700 TO-92 Temperature Sensor             | A low-power linear active thermistor. [Detailed MCP9700 TO-92 datasheet](https://www.electrokit.com/uploads/productfile/41011/21942e-2.pdf)  |



## Purchase Information

All the materials were purchased as part of the "Start Kit – Applied IoT at Linnaeus University (2023)" from Electrokit. The cost of the kit is 399 SEK. The kit can be purchased from the following link: [Start Kit – Applied IoT at Linnaeus University (2023)](https://www.electrokit.com/produkt/start-kit-applied-iot-at-linnaeus-university-2023/)

# Computer and Raspberry Pi Pico W Setup 

## Visual Studio Code (VSCode) and PyMakr Extension Installation

The device is programmed using Visual Studio Code (VSCode) on Windows 11 OS, along with the PyMakr extension that facilitates the programming and debugging of MicroPython. Here are the steps to set it up:

1. Download and install [Node.js](https://nodejs.org/en/download)
2. Download and install [VS Code](https://code.visualstudio.com/download)
3. Open VS Code and then the Extensions manager. You can access it from the left panel icon, from View >> Extensions, or by pressing `Ctrl+Shift+X`.
4. Look for PyMakr and install it.

**For more detailed instructions and additional steps, please follow the [tutorial](https://hackmd.io/@lnu-iot/rkiTJj8O9) prepared by the teacher assistants of the Linnaeus University "Applied IoT" summer 2023 course.** 


## Updating Firmware on Raspberry Pi Pico W

This microcontroller also goes by the names "RP2" or "RP2040". Follow the steps below to update the firmware:

1. Remove the ESD sponge from the Pico before proceeding. (This is the black sponge attached under your Pico).
2. Download the MicroPython firmware from this [website](https://micropython.org/download/rp2-pico-w/). Be sure to download the latest one from the Releases category, not the Nightly Builds.
3. Connect the micro-USB end of your cable (the small side) into the Raspberry Pi Pico. Be sure to firmly hold the back of the USB slot to prevent bending.
4. While holding the BOOTSEL key down on the board, connect the USB Type-A end of your cable (the big side) into your computer's USB port. Release the BOOTSEL after connecting it to your computer.
5. You should see a new drive named RPI-RP2 open in your file system, which is the Raspberry Pi Pico storage. Copy and paste the uf2 file into this storage.
6. Wait until your board automatically disconnects from your computer and then reconnects. 

Do not disconnect the device from your computer during firmware installation. It may cause firmware damage and you would need to redo the steps above.  

**Additional information and guidelines can be found in this [resource](https://hackmd.io/@lnu-iot/rkFw7gao_) provided by the teacher assistants of the Linnaeus University "Applied IoT" summer 2023 course.** 


## Running a Test Code

Open VSC and follow the steps:

1. In the left toolbar, press the Pymakr badge and connect your Pico. A prompt such as 'Serial USB (COM 3...' should pop up under Pymakr devices.
2. Hover the mouse over 'Serial USB (COM 3...', and press the flash icon (Connect device).
3. Press 'Create terminal' icon (the square with a > inside). Once terminal created, after >>>, print something to see if your board is connected. For example, type `print('hi')`, your board should reply with 'hi' (REPL). 
4. In the Pymakr projects, press create project and choose your project's destination folder.
5. An empty project will appear, press ADD DEVICES, choose your 'Serial USB (COM...)...', press OK.
6. Hover your mouse over Empty project, press 'Start development mode.' This mode will automatically upload/delete changed files and restart your device.
7. Go to the file explorer in your VSC (the very upper badge in the left toolbar, which looks like two papers) and choose `main.py`. Add the following code:

    ```python
    import time
    import machine as m

    led = m.Pin("LED", m.Pin.OUT)

    while True:
        led.toggle()
        time.sleep(2)       # Delay for 2 seconds
    ```


8. Press `Ctrl+S` to save. This action will make the Raspberry Pi Pico HW RP2040's built-in LED blink every 2 seconds. If nothing happens when you press `Ctrl+S`, check if you have activated the development mode. 
    - To do so, press the Pymakr badge in the left VSC toolbar, in the PROJECTS window, hover your mouse over Empty Project, and check what it says. If it says start development mode, press the `</>` icon to start.
    - The other way to make code run on the device is: go back to your working directory (press Explorer badge in the left VSC toolbar), right-click on `main.py`, choose Pymakr -> run file on device. 



# Putting Everything Together

This section describes how all the electronic components are connected. 

## Connecting MCP9700 TO-92 Temperature Sensor to Raspberry Pi Pico WH RP2040

 A detailed circuit diagram for this connection and the MicroPython code for reading MCP9700 TO-92 Temperature Sensor data can be found in the [following tutorial](https://hackmd.io/@lnu-iot/r1hUdtzI3) made by the teacher assistants of the course.
![](https://hackmd.io/_uploads/Bkh7GF-F3.png)



## Connecting Digital Temperature and Humidity Sensor DHT11 to Raspberry Pi Pico WH RP2040

The connection diagram for this sensor, as well as the code to read its data, can be found in the course's own [GitHub repository](https://github.com/iot-lnu/applied-iot/blob/master/Raspberry%20Pi%20Pico%20(W)%20Micropython/sensor-examples/P5_DHT_11_DHT_22/main.py).
![](https://hackmd.io/_uploads/ry5kEK-Kn.png)   


# Platform


In this project, no ready-to-use IoT application builder with data analytics and visualization tools was used. The deliberate decision was made to manually recreate all the steps in obtaining and visualizing real-time sensor data. This approach is believed to be a more effective way to learn the fundamental concepts in the IoT domain.



## HiveMQ MQTT Broker 

During the current stage of development, the HiveMQ broker is serving as the communication infrastructure for the project. As part of the future plans, an MQTT broker will be set up locally. 

The project utilizes HiveMQ, a public MQTT broker that allows any user to experiment with MQTT messages. The MQTT broker, a server in the MQTT Publish/Subscribe protocol, receives all messages from MQTT clients and routes them to the appropriate subscribers.

- Broker: broker.hivemq.com
- TCP Port: 1883

The HiveMQ MQTT Browser Client can be accessed using the following [link](https://www.hivemq.com/demos/websocket-client). Note that this client uses port 8884 for testing MCU client connection and message sending.


In this project, several clients are connected to the broker:

- The MCU client, which publishes messages.
- The SQLite database client, which runs locally and subscribes to receive messages that the HiveMQ broker receives and forwards from the MCU client.
- The Telegram bot client, which also subscribes to receive sensor data from the MCU.

## SQLite Database

In the context of a home project, scalability may not be a priority. Each MQTT message or table row (id, timestamp, float, float, float) is approximately 40 bytes. Given a rate of one message every 4 seconds, an SQLite DB would accrue about 21,600 entries in 24 hours. This equates to an approximate DB size of around 0.82 GB per day. Data lifecycle management strategies can be implemented to automatically move older data to more economical storage or to delete it after a certain period. This suggests that cloud storage may not be necessary.

## Dash for Data Visualization

Dash was chosen for data visualization. It provides an easy setup for a dashboard with multiple real-time updated time-series line plots and access to this dashboard via a Dash app webserver from any localhost.

## Telegram Bot

One of the project's objectives was to enhance the functionality of the Telegram bot to allow it to display plots or dashboards that provide insights into sensor data.

<...more to come>



















