'''
Incubator Controller Main MCU
    -   Read Sensors
    -   Interface Actuators
    -   Control algorithms linking sensor data with actuator actions
    -   Monitor System (oled and web)
'''
from sensors import sensors
from actuators import actuators
from server2 import Server
import _thread
from machine import Pin, Timer, I2C
import ssd1306

print("All System Components Up!")

class SysMode:
    MANUAL = 0
    AUTO = 1


system_mode = SysMode.MANUAL
def controller_core():
    '''
    Main Routine for the first core which reads the sensor data 
     and controls the actuators
    '''
    global system_mode
    # System start in Auto-Mode
    while True:

        # Always read all sensors
        sensors.read_all()

        if system_mode == SysMode.AUTO:
            # Closed Loop Control
            #TODO: implement more than one bound for sensor that output more than one value
            actuators.main_psu.constraint(sensors.dht22)

        # elif system_mode == SysMode.MANUAL:
            # Nothing?!


def server_core():
    '''
    Main Routine for the second core which is hosts a web app to control and monitor the whole system

    '''
    server = Server()
    # display = ssd1306.SSD1306_I2C(128, 64, I2C(1, scl=Pin(19), sda=Pin(18)))
    while True:
        server.wait_for_client()

        server.handle_html_request(server.identify_html_request())

        # global_vars.update(server.actuators_dict)
        # display.fill(0)
        # display.text("test", 0, 0, 1)
        # display.show()

        server.led.toggle()

        print('\n')



# _thread.start_new_thread(server_core, ())
# controller_core()

sleep(5)
server_core()
