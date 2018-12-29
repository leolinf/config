# -*- coding: utf-8 -*-

import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'example.com'
port = 80
s.connect((host, port))
msg = 'GET / HTTP/1.0 \r\nHost: example.com\r\n\r\n'.encode()
s.send(msg)
a = []
result = s.recv(40)
while result:
    a.append(result)
    result = s.recv(40)
print(a)
s.close()
