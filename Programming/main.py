'''
Incubator Controller Main MCU
    -   Read Sensors
    -   Interface Actuators
    -   Control algorithms linking sensor data with actuator actions
    -   Monitor System (oled and web)
'''
from machine import Pin, Timer, I2C
from sensors import Sensors
from actuators import Actuators
from monitor import Monitor
from server2 import Server
from time import sleep
import _thread

print("All System Components Up!\n")

sensors_dict = {
            'skinTemperature': 0,
            'coverClosed': 0,
            'humidity': 0,
            'temperature': 0,
            'motionSensor': 0,
            'o2Level': 0
        }

actuators_dict = {
           'autoManualSwitch': 'off',
           'psuControl': 'off',
           'blueLight': 'off',
           'uvLight': 'off',
           'buzzer': 'off',
           'humidifier': 'off'
       }

def controller_core():
    '''
    Main Routine for the first core which reads the sensor data 
     and controls the actuators
    '''
    global sensors_dict
    global actuators_dict

    sensors = Sensors(
                ntc3950_pin = 28,
                ntc3950_bounds = (23, 28),
                limit_switch_pin = 27,
                limit_switch_bounds = (0 , 0),
                dht22_pin = 16,
                dht22_temp_bounds = (23, 28),
                dht22_humidity_bounds = (40, 60),
                motion_sensor_pin = 26,
                motion_sensor_bounds = (0 ,0),
                mq135_pin = 8,
                mq135_bounds = (1 , 100)  #TODO
                )
    actuators = Actuators(
                    main_psu_pin = 1,
                    blue_light_pin = 3, 
                    uv_light_pin = 4, 
                    buzzer_pin = 14, 
                    humidifier_pin = 7
                    )
    monitor = Monitor(sensors, 19, 18)

    while True:

        # Always read all sensors
        sensors.read_all()
        sensors_dict.update(sensors.all_values)

        # Update Actuators
        actuators.all_values = actuators_dict
        

def server_core():
    '''
    Main Routine for the second core which is hosts a web app to control and monitor the whole system

    '''
    global sensors_dict
    global actuators_dict

    server = Server()
    # display = ssd1306.SSD1306_I2C(128, 64, I2C(1, scl=Pin(19), sda=Pin(18)))
    while True:

        # Send latest sensor data
        server.sensors_dict.update(sensors_dict)

        # Run Server
        server.wait_for_client()
        server.handle_html_request(server.identify_html_request())

        # Receive latest Actuator values
        actuators_dict.update(server.actuators_dict)

        # Toggle LED for User to see
        server.led.toggle()

        print('\n')

def main():
    ### Main Routine  ###
    sleep(5)
    _thread.start_new_thread(controller_core, ())
    sleep(2)
    server_core()


# ### Main Routine  ###
sleep(5)
_thread.start_new_thread(controller_core, ())
sleep(2)
server_core()

