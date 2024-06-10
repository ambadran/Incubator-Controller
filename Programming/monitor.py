'''
Monitor Sensor Values and Actuator States
'''

class Monitor:
    '''
    Class to Monitor the system sensors and actuators.
    '''
    def __init__(self, ssd1306_scl_pin: int, ssd1306_sda_pin: int)
        display = ssd1306.SSD1306_I2C(128, 64, I2C(1, scl=Pin(ssd1306_scl_pin), sda=Pin(ssd1306_sda_pin])))

        # server initiation

    def monitor(self):
        '''
        prints stuff on screen and on website
        '''
        pass
