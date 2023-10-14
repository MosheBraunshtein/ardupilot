#!/usr/bin/env python3

import socket


s = socket.socket()
host = socket.gethostname() # Get local machine name
listen_to = '0.0.0.0'
print(listen_to)
port = 12345                # Reserve a port for your service.
s.bind((listen_to, port))
s.listen(5)                 # Now wait for client connection.
while True:
   try:
        c, addr = s.accept()     # Establish connection with client.
        print ('Got connection from ', addr)
        message = "Thank you for connecting"
        message_bytes = message.encode('UTF-8')
        for i in range(100):
            c.send(message_bytes)
        c.close()
        break
   except KeyboardInterrupt as k:
        exit(0)