# -*- coding: utf-8 -*-

import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'example.com'
port = 80
s.connect((host, port))
print(s.getsockname())
msg = 'GET / HTTP/1.0 \r\nHost: example.com\r\n\r\n'
s.send(msg)
result = s.recv(4096)
print(result)
s.close()
