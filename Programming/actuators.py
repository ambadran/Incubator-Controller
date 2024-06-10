'''
Actuator Control
Abstraction layer to unify the handling of every actuator in the system
'''
from machine import Pin
from sensors import Sensor

class Actuator:
'''
    Abstract Actuator Object
    '''
    #TODO: remove the other_func_names thing and just re-define the handler for the buzzer as an Actuators method and assign it manually in the init
    def __init__(self, handler, control: callable=None, other_func_names: list[callable]=[]):
        '''
        :param handler: could be anything that is going to be used to read the sensor
        :param control: func to control the actuator, if control func is not defined then it's
                        Pin object and the control func will be Pin.value
        '''
        self.handler = handler

        # setting main control func
        if control is not None:
            self.control = control
        else:
            if type(self.handler) != Pin:
                raise ValueError("control parameter not defined for a non `Pin` object")

            self.control = self.handler.value

        # setting other control funcs
        for func_name in other_func_names:
            method = getattr(Actuators, func_name)
            setattr(self, func_name, method.__get__(self, self.__class__))

class Actuators:
    '''
    Class to control All Actuators and initialize them
    '''
    def __init__(self, main_psu_pin: int, blue_light_pin: int, uv_light_pin: int, buzzer_pin: int, humidifier_pin: int):
        '''
        Constructor for actuator objects
        '''
        self.main_psu: Actuator = Actuator(Pin(main_psu_pin, Pin.OUT))
        self.blue_light: Actuator = Actuator(Pin(blue_light_pin, Pin.OUT))
        self.uv_light: Actuator = Actuator(Pin(uv_light_pin, Pin.OUT))
        self.buzzer: Actuator = Actuator(Pin(buzzer_pin, Pin.OUT), other_func_names=[self.beep.__name__])
        self.humidifier: Actuator = Actuator(Pin(humidifier_pin, Pin.OUT))

    # this is a MUST to make it a shared method so that when I assign it to another object dynamically, I don't duplicate it memory.
    @staticmethod  
    def beep(self, sound_beep: int):
        '''
        :param sound_beep: the duration of the beep in ms
        '''
        self.control(1)
        time.sleep_ms(sound_beep)
        self.control(0)
        time.sleep_ms(sound_beep)

    def constraint(self, sensor: Sensor, inside_bound_value=0, outside_bound_value=1):
        '''
        turn off actuator if sensor limits are breached
        '''
        #TODO: implement checking more than one sensor per actuator
        if sensor.latest_value < sensor.lower_limit || sensor.latest_value > sensor.upper_limit:
            self.handler(outside_bound_value)
        else:
            self.handler(inside_bound_value)

    def all_values(self):
        '''
        return all the actuator states with the naming 
        like programmed in the html files

        'autoManualSwitch' this is the javascript id of the auto/manual switch. It shouldn't be read by the client. Only the client should set it.
        '''
        return {'psuControl': self.main_psu.control(),
                'blueLight': self.blue_light.control(),
                'uvLight': self.uv_light.control(),
                'buzzer': self.buzzer.control(),
                'humidifier':self.humidifier.control()}
 

