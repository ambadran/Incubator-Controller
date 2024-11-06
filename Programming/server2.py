'''
Meant to run on the second Core of Pico for Optimal Performance
    - Host Web App (HTML file including the CSS and JAVASCRIPT)
    - Serve the HTML GET and POST requests
    - Updates internal variables to control Actuators through other Core
    - Updates the real-time Sensor values displayed on the Web App
'''
from micropython import const
from machine import Pin
import network
import socket
import json
from time import sleep, sleep_ms
import random

class HTML_REQUEST:
    GET_SENSOR_ACTUATOR = 0
    POST_SWITCH = 1
    GET_WEB = 2

class Server:
    # Access Point Parameters
    SSID = "Smart Incubator Controller"
    PASSWORD = "12345678"

    JAVASCRIPT_TO_PYTHON = {'on': 1, 'off': 0}
    DEFAULT_WEB_NAME = 'index.html'
    def __init__(self):
        '''
        initiate server
        '''
        self.led = Pin("LED", Pin.OUT)  # on-board LED to show state
        self.led.off()

        self.reset()
        #TODO: implement try except block to avoid redefining socket
        self.init_access_point()
        self.init_socket()

        self.sensors_dict = {
                    'skinTemperature': 0,
                    'coverClosed': 0,
                    'humidity': 0,
                    'temperature': 0,
                    'motionSensor': 0,
                    'o2Level': 0
                }

        self.actuators_dict = {
               'autoManualSwitch': 'off',
               'psuControl': 'off',
               'blueLight': 'off',
               'uvLight': 'off',
               'buzzer': 'off',
               'humidifier': 'off'
               }

        self.IDENTIFY_HTML_REQUEST = {
                'GET /': HTML_REQUEST.GET_WEB,
                'GET /get_values': HTML_REQUEST.GET_SENSOR_ACTUATOR,
                'POST /set_switch_state': HTML_REQUEST.POST_SWITCH
                } 

        self.HANDLE_HTML_REQUEST = {
                HTML_REQUEST.GET_SENSOR_ACTUATOR: self.handle_get_values,
                HTML_REQUEST.POST_SWITCH: self.handle_post_switch,
                HTML_REQUEST.GET_WEB: self.handle_get_web
                }
 
    def reset(self):
        '''
        returns station object on reset.
        just deactivate and activate again 
        '''
        self.station = network.WLAN(network.AP_IF)
        self.station.config(ssid=self.SSID, password=self.PASSWORD)

        self.station.active(False)
        sleep(2)
        self.station.active(True)

    def init_access_point(self):
        '''
        set up the Access Point
        '''
        self.station.config(ssid=self.SSID, password=self.PASSWORD)

        while not self.station.active():
            print(f"Station Initializing.. ", end=' \r')

        self.led.on()
        print('Access Point Active!')
        print(self.station.ifconfig())

    def init_socket(self):
        '''
        initiate socket connection
        '''
        try:
            self.station.config(ssid=self.SSID, password=self.PASSWORD)
            sleep_ms(500)

            self.addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
            self.s = socket.socket()
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind(self.addr)
            self.s.listen(1)  # Reduce the backlog to minimize memory usage
            print('Listening on', self.addr)
        except OSError as e:
            print(f"Caught: {e}")

    def wait_for_client(self):
        '''
        Await client to connect then return new socket object used to 
        communicate with the connected client. 
        This socket is distinct from the listening socket (s) 
        and is used for sending and receiving data with the specific client that connected.
        '''
        # try:
        self.station.config(ssid=self.SSID, password=self.PASSWORD)
        sleep_ms(500)

        self.client, addr = self.s.accept()
        # print('Got a connection from {str(addr)}', end=' \r')
        print(f"Got a connection from {str(addr)}")
        # except Exception as e:
        #     print(f"Caught: {e}")

    def identify_html_request(self) -> HTML_REQUEST:
        '''
        return what HTML request is given. 
        Every HTML request must be mapped to a function that handles it.
        '''
        # try:
        self.request = self.client.recv(1024).decode()
        
        tmp = self.request.split(' ')

        if len(tmp) > 1:
            tmp = tmp[0] + ' ' + tmp[1]
        else:
            tmp = tmp[0]

        return self.IDENTIFY_HTML_REQUEST.get(tmp, None)
        # except Exception as e:
        #     print(f"Caught in identify html: {e}")
        #     print(f"on Request {self.request}")

    def handle_html_request(self, html_request: HTML_REQUEST):
        '''
        handles the identified html request
        '''
        try:
            if html_request is not None:
                self.HANDLE_HTML_REQUEST[html_request]()
        
            else:
                self.handle_unkonwn_request()
                print(f"Got unkonwn Request:\n{self.request}")

        except Exception as e:
            print(f"Error in handle web get request: {e}")

        finally:
            self.client.close()

    def handle_get_web(self):
        '''
        Handles GET_ACTUATORS_WEB HTML GET Request
        '''
        web_name = self.request.split(' ')
        web_name = web_name[1]
        if web_name == '/':
            # default web
            web_name = self.DEFAULT_WEB_NAME

        else:
            web_name = web_name[1:]

        with open(web_name, 'r') as f:
            web_page = f.read()

        self.client.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        # self.client.send('HTTP/1.1 200 OK\n')
        # self.client.send('Content-Type: text/html\n')
        # self.client.send('Connection: close\n\n')
        self.client.sendall(web_page)

    def handle_post_switch(self):
        '''

        '''
        length = int(self.request.split('Content-Length: ')[1].split('\r\n')[0])
        body = json.loads(self.client.recv(length).decode('utf-8'))

        self.actuators_dict[body['id']] = body['state']

        response = 'HTTP/1.1 200 OK\r\n\r\n'
        self.client.send(response)

    def handle_get_values(self):
        '''

        '''
        # switch_values = [b'on', b'off']
        # self.all_values = {
        #         'skinTemperature': random.getrandbits(4),
        #         'coverClosed': random.getrandbits(4),
        #         'humidity': random.getrandbits(4),
        #         'temperature': random.getrandbits(4),
        #         'motionSensor': random.getrandbits(4),
        #         'o2Level': random.getrandbits(4),
        #         'autoManualSwitch': switch_values[random.getrandbits(1)],
        #         'psuControl': switch_values[random.getrandbits(1)],
        #         'blueLight': switch_values[random.getrandbits(1)],
        #         'uvLight': switch_values[random.getrandbits(1)],
        #         'buzzer': switch_values[random.getrandbits(1)],
        #         'humidifier': switch_values[random.getrandbits(1)],
        # }

        tmp = self.sensors_dict
        tmp.update(self.actuators_dict)

        response = json.dumps(tmp)
        self.client.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        self.client.send(response)

    def handle_unkonwn_request(self):
        '''
        Handles unknown request
        '''
        self.client.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        self.client.send('HTTP/1.1 404 Not Found\r\n\r\nFile Not Found')


