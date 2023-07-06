import time
import threading
from lib.mqtt_dbhandler import MQTTDatabaseHandler
from lib.dashboard_handler import DashBoardHandler


if __name__ == "__main__":
    # MQTT Database Handler
    db_handler = MQTTDatabaseHandler(broker="broker.hivemq.com", port=1883, topic="topic-test-1",
                                     db_file="sensor_data.db", table_name="sensor_data")

    # DashBoard Handler
    dash_handler = DashBoardHandler(db_file="sensor_data.db", sensor_table_name="sensor_data")

    # Create two threads
    db_thread = threading.Thread(target=db_handler.run)
    dash_thread = threading.Thread(target=dash_handler.run)

    # Start the threads
    db_thread.start()

    # Add some delay before starting the dashboard
    time.sleep(5)  

    dash_thread.start()




