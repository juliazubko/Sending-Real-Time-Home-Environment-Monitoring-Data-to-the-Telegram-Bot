import machine as m
import dht

class SensorReader:
    def __init__(self, dht_pin, analog_pin):
        self.dht_temp_sensor = dht.DHT11(m.Pin(dht_pin))
        self.analog_temp_sensor = m.ADC(analog_pin)
        self.sf = 4095 / 65535
        self.volt_per_adc = (3.3 / 4095)

    def read_dht(self):
        try:
            self.dht_temp_sensor.measure()
            temp = self.dht_temp_sensor.temperature()
            humid = self.dht_temp_sensor.humidity()
            return temp, humid
        except Exception as e:
            print("Error reading DHT sensor: ", e)
            return None, None

    def read_analog_temp(self):
        try:
            mv = self.analog_temp_sensor.read_u16()
            adc_12b = mv * self.sf
            volt = adc_12b * self.volt_per_adc
            dx = abs (50 - 0)
            dy = abs(0 - 0.5)
            shift = volt - 0.5 
            temp = shift / (dy / dx)
            return temp
        except Exception as e:
            print("Error reading Analog sensor: ", e)
            return None
