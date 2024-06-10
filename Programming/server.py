from micropython import const
import network
import socket
import json
import time

class HTML_REQUEST:
    GET_SENSOR_ACTUATOR = 0
    POST_SWITCH = 1
    GET_WEB = 2

class Server:
    # Access Point Parameters
    SSID = const("Smart Incubator Controller")
    PASSWORD = const("12345678")

    HTML_REQUEST_MAPPING = {'': HTML_REQUEST.GET_SENSOR_ACTUATOR,
                            '': HTML_REQUEST.POST_SWITCH,
                            '': HTML_REQUEST.GET_WEB}
    ON_OFF_MAPPING = {'on': 1, 'off': 0}
    def __init__(self):
        '''
        initiate server
        '''
        self.init_access_point()
        self.init_socket()

    def init_access_point(self):
        '''
        set up the Access Point
        '''
        self.station = network.WLAN(network.AP_IF)
        self.station.active(True)
        self.station.config(ssid=self.SSID, password=self.PASSWORD)

        while not self.station.active():
            pass

        print('Access Point Active!')
        # display.home()
        # display.write("AP Active!      ")
        print(self.station.ifconfig())
        # display.move(0, 1)
        # display.write(f"{station.ifconfig()[0]}")

        time.sleep(3)

    def init_socket(self):
        '''
        initiate socket connection
        '''
        self.addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(addr)
        self.s.listen(1)  # Reduce the backlog to minimize memory usage
        print('Listening on', self.addr)
        # display.home()
        # display.write()

    @property
    def web_page(self):
        '''
        return the HTML page
        '''
        with open('index.html', 'r') as f:
            web_page = f.read()

        return web_page

    def wait_for_client(self):
        '''
        Await client to connect then return new socket object used to 
        communicate with the connected client. 
        This socket is distinct from the listening socket (s) 
        and is used for sending and receiving data with the specific client that connected.
        '''
        self.client, addr = s.accept()
        print('Got a connection from %s' % str(addr))

    def get_html_request(self) -> tuple[HTML_REQUEST, int, int]:
        '''
        return what the html request wants
        either an html get request for a json object with all the current sensor data
            or an html post request that mentions what switch id was triggered by the user and what value
            or an html get request for the html page itself
        '''
        try:
            request = self.client.recv(1024)
            request = str(request)
            print(request, end='\n\n')

            if request.startswith('GET / '):
                return (HTML_REQUEST.GET_WEB)

            elif request.startswith('GET /get_values'):
                content_length = int(request.split('Content-Length: ')[1].split('\r\n')[0])
                body = request.split('\r\n\r\n')[1][:content_length]
                data = ujson.loads(body)
                pin_id = switch_pins.get(data['id'])
                if pin_id:
                    return (HTML_REQUEST.POST_SWITCH, pin_id, self.ON_OFF_MAPPING[data['state']])
                else:
                    raise ValueError(f"pin_id: {pin_id}, body: {body}")

            elif request.startswith('POST /set_switch_state'):
                return (HTML_REQUEST.GET_SENSOR_ACTUATOR)

        except Exception as e:
            print(f"Error: {e}")

        finally:
            self.client.close()

    def handle_get_web(self):
        '''
        handles GET Request for the whole html file
        '''
        try:
            response = web_page()
            self.client.send('HTTP/1.1 200 OK\n')
            self.client.send('Content-Type: text/html\n')
            self.client.send('Connection: close\n\n')
            self.client.sendall(response)

        except Exception as e:
            print(f"Error: {e}")

        finally:
            self.client.close()

    def handle_get_values(self, values: dict[str, int]):
        '''
        handle sending sensor data in this form
        {'skinTemperature': 36,
        'coverClosed': 1,
        'humidity': 50,
        'temperature': 25,
        'motionSensor': 0,
        'o2Level': 21,

        handle sending actuator states in this form
        {'autoManualSwitch': 'on',
        'psuControl': 'off',
        'blueLight': 'off',
        'uvLight': 'off',
        'buzzer': 'on',
        'humidifier': 'on',
        }

        put one of them or both together in one dictionary
        '''
        try:
            response = ujson.dumps(values)
            self.client.send('HTTP/1.1 200 OK\n')
            self.client.send('Content-Type: application/json\n')
            self.client.send('Connection: close\n\n')
            self.client.sendall(response)

        except Exception as e:
            print(f"Error: {e}")

        finally:
            self.client.close()

    def handle_post_switches(self, values=None):
        '''
        Nothing to do here. the values of the switches will be processed in another file
        '''
        try:
            self.client.send('HTTP/1.1 200 OK\n')
            self.client.send('Connection: close\n\n')

        except Exception as e:
            print(f"Error: {e}")

        finally:
            self.client.close()


