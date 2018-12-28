# -*- coding: utf-8 -*-

import socket

HOST = ''
PORT = 8081


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))

s.listen(10)
while 1:
    conn, addr = s.accept()

    print(conn, addr)

    data = conn.recv(1024)
    print(data)
    if not data:
        break
    reply = b'ok ...'
    conn.sendall(reply)

conn.close()
s.close()
