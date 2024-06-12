'''
Incubator Controller Main MCU
    -   Read Sensors
    -   Interface Actuators
    -   Control algorithms linking sensor data with actuator actions
    -   Monitor System (oled and web)
'''
def main():
    from sensors import sensors
    from actuators import actuators
    from server import server, HTML_REQUEST
    import _thread
    from machine import Pin, Timer

    led = Pin('LED', Pin.OUT)
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

        tim = Timer(-1)
        while True:

            tim.init(period=500, mode=Timer.PERIODIC, callback=lambda t: led.value(not led.value()))
            try:

                server.wait_for_client()

                html_request_full = server.get_html_request()
                print(f"HTML Request: {html_request_full}")

                if html_request_full:
                    html_request, pin_id, pin_value = html_request_full

                    switch_values = [b'on', b'off']

                    if html_request == HTML_REQUEST.GET_SENSOR_ACTUATOR:
                        values = sensors.all_values
                        values.extend(actuators.all_values)
                        server.handle_get_values(values)

                    elif html_request == HTML_REQUEST.POST_SWITCH:
                        print("TODO:")

                    elif html_request == HTML_REQUEST.GET_WEB:
                        values = None
                        server.handle_get_web(values)

                    else:
                        raise ValueError("HOW THE FUCK?!?!")

                else:
                    server.client.close()


            except Exception as e:
                print(f"Error in Main Server Loop: {e}")
                tim.deinit()

        tim.deinit


    _thread.start_new_thread(server_core, ())
    controller_core()

# main()


