'''
Incubator Controller Main MCU
    -   Read Sensors
    -   Interface Actuators
    -   Control algorithms linking sensor data with actuator actions
    -   Monitor System (oled and web)
'''
from sensors import Sensors
from actuators import Actuators
from server import Server

led = Pin('LED', Pin.OUT)

class SysMode:
    AUTO = 0
    MANUAL = 1

# Initializing all system components
sensors = Sensors(

        )
actuators = Actuators(

        )
server = Server()

print("All System Components Up!")

def controller_core():
    '''
    Main Routine for the first core which reads the sensor data 
     and controls the actuators
    '''
    # System start in Auto-Mode
    system_mode = SysMode.AUTO
    while True:

        # Always read all sensors
        sensors.read_all()

        if system_mode == SysMode.AUTO:
            # Closed Loop Control
            #TODO: implement more than one bound for sensor that output more than one value
            actuators.main_psu.constraint(sensors.dht22)

        elif system_mode == SysMode.MANUAL:
            # 


def server_core():
    '''
    Main Routine for the second core which is hosts a web app to control and monitor the whole system
    '''
    pass
