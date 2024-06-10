from micropython import const
import network
import socket
import json
import gc
import time

class Server:
    # Access Point Parameters
    SSID = const("Smart Incubator Controller")
    PASSWORD = const("12345678")
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

    def handle_client(self):
        '''
        handle one client HTML request
        '''
        try:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            request = str(request)
            print(request, end='\n\n')

            if '/get_sensors' in request:
                sensor1, sensor2 = read_sensors()
                difference = abs(sensor1 - sensor2)
                response = json.dumps({
                    "sensor1": sensor1,
                    "sensor2": sensor2,
                    "difference": difference
                })
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: application/json\n')
                conn.send('Connection: close\n\n')
                conn.sendall(response)

                # display.move(0, 0)
                # display.write(f"S1 {sensor1}, S2 {sensor2}")

            elif '/set_valve?valve=1' in request:
                valve1.value(not valve1.value())
                response = 'Valve 1 toggled'
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/plain\n')
                conn.send('Connection: close\n\n')
                conn.sendall(response)

                # display.move(0, 1)
                # display.write(f"V1: {valve1.value()}")

            elif '/set_valve?valve=2' in request:
                valve2.value(not valve2.value())
                response = 'Valve 2 toggled'
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/plain\n')
                conn.send('Connection: close\n\n')
                conn.sendall(response)

                # display.move(7, 1)
                # display.write(f"V2: {valve2.value()}")

            else:
                response = web_page()
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                conn.sendall(response)

                led.off()
        
        except Exception as e:
            print(f"Error: {e}")
            # tim.deinit()

        finally:
            conn.close()
            gc.collect()

    def run_server(self):
        '''
        Hosting the web page and processing HTML requests
        '''

        while True:
            # tim.init(period=500, mode=Timer.PERIODIC, callback=lambda t: led.value(not led.value()))

            try:


