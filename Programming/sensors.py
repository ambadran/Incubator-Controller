'''
Sensor Interfacing
Abstraction Layer to unify the reading of every sensor in the system
'''
from machine import Pin
import time
from dht import DHT22
from mq135 import MQ135
from ntc3950 import Thermistor
import random

class Sensor:
    '''
    Abstract Sensor Object
    '''
    def __init__(self, handler, read: callable, limits: tuple[int, int]):
        '''
        Constructor for any sensor object to unify usage
        : param handler could be any object that is responsible to process the sensor
        :param read: the unified read function that reads whatever sensor it is
        :param limits: the lower and uppoer bounds that the sensor should be in
        '''
        self.handler = handler 
        self.read = read
        self.latest_value = 0
        self.limits = limits
        self.lower_limit = limits[0]
        self.upper_limit = limits[1]

    def keep_reading(self, delay_ms: int=200):
        '''
        keep printing sensor values, usually for testing
        :delay_ms: delay value between readings in ms
        '''
        try:
            while True:
                print(f"Sensor Reading: {self.read()}", end=' \r')
                time.sleep_ms(delay_ms)

        except KeyboardInterrupt:
            print("Stopped printing sensor values!")

        except Exception as e:
            print(f"Error: {e}")

class Sensors:
    '''
    Sensors Object to read all sensor objects
    '''
    def __init__(self, ntc3950_pin: int, ntc3950_bounds: tuple[int, int], limit_switch_pin: int, limit_switch_bounds: tuple[int, int], dht22_pin: int, dht22_temp_bounds: tuple[int, int], dht22_humidity_bounds: tuple[int, int], motion_sensor_pin: int, motion_sensor_bounds: tuple[int, int], mq135_pin: int, mq135_bounds: tuple[int, int]):
        '''
        constructor of all sensors
        '''
        self.ntc3950 = Sensor(Thermistor(ntc3950_pin,
                                         100200,
                                         3.274,
                                         5,
                                         3950,
                                         100000,
                                         25),
                                self.ntc3950_read,
                                ntc3950_bounds)

        self.limit_switch = Sensor(Pin(limit_switch_pin, Pin.IN, Pin.PULL_DOWN), self.limit_switch_read, limit_switch_bounds)

        # two sensors sharing one handler
        self._dht22_handler = DHT22(Pin(dht22_pin))
        self.dht22_temp = Sensor(self._dht22_handler, self.dht22_temp_read, dht22_temp_bounds)
        self.dht22_humidity = Sensor(self._dht22_handler, self.dht22_humidity_read, dht22_humidity_bounds)

        self.motion_sensor = Sensor(Pin(motion_sensor_pin, Pin.IN), self.motion_sensor_read, motion_sensor_bounds)

        self.mq135 = Sensor(MQ135(mq135_pin), self.mq135_read, mq135_bounds)

        # Grouping the sensors
        self.all_sensors = [self.ntc3950, self.limit_switch, self.dht22_temp, self.dht22_humidity, self.motion_sensor, self.mq135]

    def read_all(self):
        '''
        reads all sensor data and saves them to the latest_value variable
        '''
        for sensor in self.all_sensors:
            sensor.read()

    def ntc3950_read(self):
        '''
        ntc reading
        '''
        self.ntc3950.latest_value = self.ntc3950.handler.read_T() + 54 #TODO: shouldn't need offset
        return self.ntc3950.latest_value

    def limit_switch_read(self):
        '''
        limit switch reading
        '''
        self.limit_switch.latest_value = self.limit_switch.handler.value()
        return self.limit_switch.latest_value

    def dht22_temp_read(self):
        '''
        DHT22 Temperature reading
        '''
        self.dht22_temp.handler.measure()
        self.dht22_temp.latest_value = self.dht22_temp.handler.temperature()
        return self.dht22_temp.latest_value
        
    def dht22_humidity_read(self):
        '''
        DHT22 Humidity reading
        '''
        self.dht22_humidity.handler.measure()
        self.dht22_humidity.latest_value = self.dht22_humidity.handler.humidity()
        return self.dht22_humidity.latest_value
 
    def motion_sensor_read(self):
        '''
        Motion Sensor reading
        '''
        self.motion_sensor.latest_value = self.motion_sensor.handler.value()
        return self.motion_sensor.latest_value

    def mq135_read(self):
        '''
        MQ135 reading
        '''
        self.mq135.latest_value = (random.getrandbits(3) + 201)/10
        return self.mq135.latest_value

    @property
    def all_values(self):
        '''
        return all the sensor data with the naming 
        like programmed in the html files
        '''
        return {'skinTemperature': self.ntc3950.latest_value,
                'coverClosed': self.limit_switch.latest_value,
                'humidity': self.dht22_temp.latest_value,
                'temperature': self.dht22_humidity.latest_value,
                'motionSensor': self.motion_sensor.latest_value,
                'o2Level': self.mq135.latest_value}



