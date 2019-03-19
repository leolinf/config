# -*- coding: utf-8 -*-

import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8081))
s.send('hello'.encode())
result = s.recv(40)
print(result)
s.close()
