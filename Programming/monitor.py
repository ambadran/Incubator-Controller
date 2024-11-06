'''
Monitor Sensor Values and Actuator States
'''
from machine import Timer, I2C, Pin
import ssd1306

class Monitor:
    '''
    Class to Monitor the system sensors and actuators.
    '''
    DEFAULT_TIME_BTW_SCREEN = 5000
    def __init__(self, sensors, ssd1306_scl_pin: int, ssd1306_sda_pin: int):
        self.display = ssd1306.SSD1306_I2C(128, 64, I2C(1, scl=Pin(ssd1306_scl_pin), sda=Pin(ssd1306_sda_pin)))

        self.sensors = sensors

        self._current_screen = True  # two screen

        self.run()

    def run(self):
        '''
        prints stuff on screen 
        ''' 
        self.timer = Timer(period=self.DEFAULT_TIME_BTW_SCREEN, mode=Timer.PERIODIC, callback=self.show_screen)

    def stop(self):
        '''
        stops printing
        '''
        self.timer.deinit()

    def show_screen(self, t):
        '''
        Setting First screen with newest saved sensor values
        '''
        self._current_screen = not self._current_screen
        if self._current_screen:

            # First Screen
            self.display.fill(0)

            self.display.text(f"Skin Temp: {self.sensors.ntc3950.latest_value}'C", 0, 0, 1)
            cover_state = 'Opened' if self.sensors.limit_switch.latest_value else 'Closed'
            self.display.text(f"Cover: {cover_state}", 0, 16, 1)
            motion_sensor_state = 'Yes' if self.sensors.motion_sensor.latest_value else 'No'
            self.display.text(f"Movement: {motion_sensor_state}", 0, 32, 1)
            self.display.text(f"O2: {self.sensors.mq135.latest_value}%", 0, 48, 1)

            self.display.show()

        else:

            # Second Screen
            self.display.fill(0)
        
            self.display.text(f"Temp: {self.sensors.dht22_temp.latest_value} 'C", 0, 0, 1)
            self.display.text(f"Humidity: {self.sensors.dht22_humidity.latest_value}%", 0, 32, 1)
            self.display.show()
