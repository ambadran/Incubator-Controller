from micropython import const
import network
import socket
import json
import time
import random

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

        self.station = network.WLAN(network.AP_IF)
        if not self.station.active():
            self.init_access_point()
            self.init_socket()

        # should've been class method but contain self
        self.HANDLE_HTML_REQUEST = {HTML_REQUEST.GET_SENSOR_ACTUATOR: self.handle_get_values,
                               HTML_REQUEST.POST_SWITCH: self.handle_post_switches,
                               HTML_REQUEST.GET_WEB: self.handle_get_web}
     

    def init_access_point(self):
        '''
        set up the Access Point
        '''
        self.station = network.WLAN(network.AP_IF)

        self.station.active(False)
        time.sleep(5)

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


    def init_socket(self):
        '''
        initiate socket connection
        '''
        self.addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(self.addr)
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
        self.client, addr = self.s.accept()
        print('Got a connection from %s' % str(addr))

    def get_html_request(self) -> tuple[HTML_REQUEST, int, int]:
        '''
        return what the html request wants
        either an html get request for a json object with all the current sensor data
            or an html post request that mentions what switch id was triggered by the user and what value
            or an html get request for the html page itself
        '''
        # try:
        request = self.client.recv(1024)
        request = request.decode()
        print(request, end='\n\n')

        if request.startswith('GET / '):
            print("got web request")
            return (HTML_REQUEST.GET_WEB, 0, 0)

        elif request.startswith('GET /get_values'):
            print("got values get request")
            return (HTML_REQUEST.GET_SENSOR_ACTUATOR, 0, 0)

        elif request.startswith('POST /set_switch_state'):
            print("got values post request")
            content_length = int(request.split('Content-Length: ')[1].split('\r\n')[0])
            body = request.split('\r\n\r\n')[1][:content_length]
            data = json.loads(body)
            pin_id = switch_pins.get(data['id'])
            if pin_id:
                return (HTML_REQUEST.POST_SWITCH, pin_id, self.ON_OFF_MAPPING[data['state']])
            else:
                raise ValueError(f"pin_id: {pin_id}, body: {body}")

        else:
            print("got unknown request")

        # except Exception as e:
        #     print(f"Error in get html request: {e}")


    def handle_get_web(self, values):
        '''
        handles GET Request for the whole html file
        '''
        try:
            response = self.web_page
            self.client.send('HTTP/1.1 200 OK\n')
            self.client.send('Content-Type: text/html\n')
            self.client.send('Connection: close\n\n')
            self.client.sendall(response)

        except Exception as e:
            print(f"Error in handle web get request: {e}")

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
            response = json.dumps(values)
            self.client.send('HTTP/1.1 200 OK\n')
            self.client.send('Content-Type: application/json\n')
            self.client.send('Connection: close\n\n')
            self.client.sendall(response)

        except Exception as e:
            print(f"Error in handle values get request: {e}")

        finally:
            self.client.close()

    def handle_post_switches(self, values):
        '''
        Nothing to do here. the values of the switches will be processed in another file
        '''
        try:
            self.client.send('HTTP/1.1 200 OK\n')
            self.client.send('Connection: close\n\n')

        except Exception as e:
            print(f"Error in handle values post request: {e}")

        finally:
            self.client.close()


    def test_server(self):
        '''
        implements the routine of the server for testing purposes
        '''
        try:
            while True:
                self.wait_for_client()

                html_request_full = self.get_html_request()
                print(f"HTML Request: {html_request_full}")

                if html_request_full:
                    html_request, pin_id, pin_value = html_request_full

                    switch_values = [b'on', b'off']

                    values = {'skinTemperature': random.getrandbits(4),
                    'coverClosed': random.getrandbits(4),
                    'humidity': random.getrandbits(4),
                    'temperature': random.getrandbits(4),
                    'motionSensor': random.getrandbits(4),
                    'o2Level': random.getrandbits(4),
                    'autoManualSwitch': switch_values[random.getrandbits(1)],
                    'psuControl': switch_values[random.getrandbits(1)],
                    'blueLight': switch_values[random.getrandbits(1)],
                    'uvLight': switch_values[random.getrandbits(1)],
                    'buzzer': switch_values[random.getrandbits(1)],
                    'humidifier': switch_values[random.getrandbits(1)],
                    }

                    self.HANDLE_HTML_REQUEST[html_request](values)

                else:
                    self.client.close()

        except KeyboardInterrupt:
            print("Keyboard Interrupted!")

        # except Exception as e:
        #     print(f"Error in test server: {e}")

server = Server()
# server.test_server()
