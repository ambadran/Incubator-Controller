    # def handle_client(self):
    #     '''
    #     handle one client HTML request
    #     '''
    #     try:
    #         client, addr = s.accept()
    #         print('Got a connection from %s' % str(addr))
    #         request = client.recv(1024)
    #         request = str(request)
    #         print(request, end='\n\n')

    #         if request.startswith('GET / '):
    #             response = web_page()
    #             client.send('HTTP/1.1 200 OK\n')
    #             client.send('Content-Type: text/html\n')
    #             client.send('Connection: close\n\n')
    #             client.sendall(response)
    #         elif request.startswith('GET /get_values'):
    #             values = get_sensor_values()
    #             for key, pin in switch_pins.items():
    #                 values[key] = 'on' if pin.value() else 'off'
    #             response = ujson.dumps(values)
    #             client.send('HTTP/1.1 200 OK\n')
    #             client.send('Content-Type: application/json\n')
    #             client.send('Connection: close\n\n')
    #             client.sendall(response)
    #         elif request.startswith('POST /set_switch_state'):
    #             content_length = int(request.split('Content-Length: ')[1].split('\r\n')[0])
    #             body = request.split('\r\n\r\n')[1][:content_length]
    #             data = ujson.loads(body)
    #             pin = switch_pins.get(data['id'])
    #             if pin:
    #                 if data['state'] == 'on':
    #                     pin.value(1)
    #                 else:
    #                     pin.value(0)
    #             client.send('HTTP/1.1 200 OK\n')
    #             client.send('Connection: close\n\n')
    #         client.close()
        
    #     except Exception as e:
    #         print(f"Error: {e}")

    #     finally:
    #         client.close()

    # def run_server(self):
    #     '''
    #     Hosting the web page and processing HTML requests
    #     '''

    #     while True:

    #         try:


