# -*- coding: utf-8 -*-

import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except Exception as e:
    print(e)
    sys.exit()

host = '127.0.0.1'

#ip = socket.gethostbyname(host)
port = 8081

s.connect((host, port))
msg = 'GET / HTTP/1.1\r\n\r\n'.encode()
s.sendall(msg)
result = s.recv(4096)
print(result)
s.close()
