## Sending Real-Time Home Environment Monitoring Data to the Telegram Bot
*(in progress)*

**This project is a practical part of the “Applied IoT” summer course offered by Linnaeus University (23ST - 1DT305).**

 

```mermaid
flowchart LR
    A(MCU MQTT Client1)-->|"sends sensor data
	(publishes to the topic)"|B{{" HiveMQ 
	MQTT Broker"}}
    
	C[("MQTT Client2
    SQLite DB")] --> |"gets sensor data, 
    stores into DB
    (subscribes to the topic)"|B 
 
    C---|"retreives 
        sensor data
        from DB, 
        plots graphs"|D(Dash Plotly Dashboard)  


    E(MQTT Client3 Telegram bot)-->|"
        gets sensor data
        textual / bot message
        representaton
        (subscribes
        to the topic)"|B  
        
    B-->C
    B-->E
```

![dash](https://github.com/juliazubko/Sensor-Data-to-Telegram-Bot/assets/102211232/02c60fc8-cc7e-4566-9a66-89852102d2fd)  

 https://github.com/juliazubko/Sensor-Data-to-Telegram-Bot/assets/102211232/bccf72ea-18f6-4ef1-930f-5c192e46bca4 

This project aims to develop an autonomous, IoT-based home environment monitoring system using a Raspberry Pi Pico WH microcontroller unit (MCU) and various sensors, with a design that allows for sensor data to be displayed via a Telegram bot upon user demand.

The current setup involves a DHT11 digital temperature and humidity sensor and a MCP9700 TO-92 analogue temperature sensor. Sensor data is transmitted via Wi-Fi, using MQTT communication protocol, to an online HiveMQ broker. 

A Telegram bot currently offers real-time sensor data on request. Future enhancements include expanding its capabilities to display insightful plots or dashboards and to trigger specific actions on the MCU through bot commands.

The eventual goal is to run the system on battery power and a local MQTT broker, potentially bypassing the need for the Broker-to-SQL + SQL-to-Dash process (considering the option to deliver data visualizations  via the Telegram bot). 

**See full description at https://hackmd.io/@iz222br/BJLkNrbY2**  




