'''
Interfacing the NTC3950
'''
from machine import Pin, ADC
from math import log

class Thermistor:
    '''
    Class to read and process Thermistor
    '''
    def __init__(self, adc_pin, R_divider, Vcc, num_samples, B_factor, R_nominal, room_temp):
        '''

        :param Vcc: Vcc of micropython board, measure with multimeter to get exact value for more accuracy
        :param R_divider: the exact value of the 10k resistor in series of the voltage divider is probably not 10k exactly
        :param num_samples: the number of samples to average for every average_reading
        :param B_factor: also known as thermistor factor, value from datasheet
        :param R_nominal: Thermistor resistance value at room temperature
        '''
        # User defined attributes
        self.adc = ADC(Pin(adc_pin))
        # if device_name == Device.ESP32S3:
        #     self.adc.atten(3)

        self.Vcc = Vcc
        self.R_divider = R_divider
        self.num_samples = num_samples
        self.B_factor = B_factor
        self.R_nominal = R_nominal
        self.room_temp = room_temp + 273.15

        # processing attributes
        self.room_temp_inv = 1/self.room_temp
        self.B_factor_inv = 1/self.B_factor

    def read_V(self):
        '''
        returns voltage value read 
        '''
        return ((self.adc.read_u16()*self.Vcc)/65534)

    def read_V_averaged(self):
        '''
        reads 'num_samples' voltage samples then return average V
        '''
        samples = []
        for _ in range(self.num_samples):
            samples.append(self.read_V())

        return sum(samples)/self.num_samples

    def read_R(self):
        '''
        returns resistance value of thermistor
        '''
        Vi = self.read_V()
        return ((self.R_divider*Vi)/(self.Vcc-Vi))

    def read_R_averaged(self):
        '''
        reads 'num_samples' voltage samples then return  Resistance value from the average V
        '''
        Vi = self.read_V_averaged()
        return ((self.R_divider*Vi)/(self.Vcc-Vi))

    def read_T(self):
        '''
        reads temperature using simplified B parameter Steinhard-Hart equations
        '''
        try:
            T_inverse = self.room_temp_inv + self.B_factor_inv*log(self.read_R_averaged()/self.R_nominal)
            T_celcuis = 1/T_inverse - 273.15
        except ValueError:
            print("Encountered Math domain error")
            return 0

        return T_celcuis

    def monitor(self, time_delay=100, exit_on_interrupt=False):
        '''
        continiously print temperature until KeyboardInterrupt

        :param time_delay: how much time to delay between each print in ms

        could be used with terminal command tee to pull data off the micorpython device
        '''
        try:
            while True:
                # print(f"Temperature: {self.read_T()}\r", end='')
                print(f"Temperature: {self.read_T()}", end='\r')  # for use in logging
                sleep_ms(time_delay)

        except KeyboardInterrupt:
            # if exit_on_interrupt:
            #     _thread.exit()  # doesn't work for some reason ?!?
            # else:
            return

        finally:
            do_nothing()


