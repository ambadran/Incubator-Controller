'''
Sensor Interfacing
Abstraction Layer to unify the reading of every sensor in the system
'''
from machine import Pin, ADC
import time
from dht import DHT22
from MQ135 import MQ135

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
        self.latest_value2 = 0 # for sensors that output two values like dht22
        self.limits = limits
        self.lower_limit = limits[0]
        self.upper_limit = limits[1]

    def keep_reading(self, delay_ms: int):
        '''
        keep printing sensor values, usually for testing
        :delay_ms: delay value between readings in ms
        '''
        try:
            while True:
                print(self.read())
                time.sleep_ms(delay_ms)

        except KeyboardInterrupt:
            print("Stopped printing sensor values!")

        except Exception as e:
            print(f"Error: {e}")

class Sensors:
    '''
    Sensors Object to read all sensor objects
    '''
    def __init__(self, ntc3950_pin: int, ntc3950_bounds: tuple[int, int], limit_switch_pin: int, limit_switch_bounds: tuple[int, int], dht22_pin: int, dht22_bounds: tuple[int, int], motion_sensor_pin: int, motion_sensor_bounds: tuple[int, int], mq135_pin: int, mq135_bounds: tuple[int, int]):
        '''
        constructor of all sensors
        '''
        self.ntc3950 = Sensor(ADC(Pin(ntc3950_pin)), self.ntc3950_read, ntc3950_bounds)
        self.limit_switch = Sensor(Pin(limit_switch_pin, Pin.IN, Pin.PULL), self.limit_switch_read, limit_switch_bounds)
        self.dht22 = Sensor(DHT22(Pin(dht22_pin)), self.dht22_read, dht22_bounds)
        self.motion_sensor = Sensor(Pin(motion_sensor_pin, Pin.IN, Pin.PULL), self.motion_sensor_read, motion_sensor_bounds)
        self.mq135 = Sensor(MQ135(mq135_pin), self.mq135_read, mq135_bounds)

        # Grouping the sensors
        self.all_sensors = [self.ntc3950, self.limit_switch, self.dht22, self.motion_sensor, self.mq135]

    def read_all(self):
        '''
        reads all sensor data and saves them to the latest_value variable
        '''

    def ntc3950_read(self):
        '''
        ntc reading
        '''

        self.ntc3950.latest_value = 0

    def limit_switch_read(self):
        '''
        limit switch reading
        '''

        self.limit_switch.latest_value = 0

    def dht22_read(self):
        '''
        DHT22 reading
        '''

        self.dht22.latest_value = 0
        self.dht22.latest_value2 = 0

    def motion_sensor_read(self):
        '''
        Motion Sensor reading
        '''

        self.motion_sensor.latest_value = 0

    def mq135_read(self):
        '''
        MQ135 reading
        '''

        self.mq135.latest_value = 0

    def all_values(self):
        '''
        return all the sensor data with the naming 
        like programmed in the html files
        '''
        return {'skinTemperature': self.ntc3950.latest_value,
                'coverClosed': self.limit_switch.latest_value,
                'humidity': self.dht22.latest_value,
                'temperature': self.dht22.latest_value2,
                'motionSensor': self.motion_sensor_latest_value,
                'o2Level': self.mq135.latest_value}



