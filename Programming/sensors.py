'''
Incubator Controller Main MCU
    -   Read Sensors
    -   Interface Actuators
    -   Control algorithms linking sensor data with actuator actions
    -   Monitor System (oled and web)
'''
from machine import Pin, ADC
import time
from dht import DHT22
from MQ135 import MQ135
import ssd1306

class Sensor:
    '''
    Abstract Sensor Object
    '''
    def __init__(self, handler, read):
        '''
        Constructor
        '''
        self.handler = handler 
        self.read = read


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
    def __init__(self, ntc3950_pin: int, limit_switch_pin: int, dht22_pin: int, motion_sensor_pin: int, mq135_pin: int):
        '''
        constructor of all sensors
        '''
        self.ntc3950 = Sensor(ADC(Pin(ntc3950_pin)), self.ntc3950_read)
        self.limit_switch_pin = Sensor(Pin(limit_switch_pin, Pin.IN, Pin.PULL), self.limit_switch_read)
        self.dht22 = Sensor(DHT22(Pin(dht22_pin)), self.dht22_read)
        self.motion_sensor_pin = Sensor(Pin(motion_sensor_pin, Pin.IN, Pin.PULL), self.motion_sensor_read)
        self.mq135 = Sensor(MQ135(mq135_pin), self.mq135_read)

    def ntc3950_read(self):
        '''
        ntc reading
        '''
        pass

    def limit_switch_read(self):
        '''
        limit switch reading
        '''
        pass

    def dht22_read(self):
        '''
        DHT22 reading
        '''
        pass

    def motion_sensor_read(self):
        '''
        Motion Sensor reading
        '''
        pass

    def mq135_read(self):
        '''
        MQ135 reading
        '''
        pass


