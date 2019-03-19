# -*- coding: utf-8 -*-
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8081))
s.listen(10)

while 1:
    conn, addr = s.accept()

    print(conn, addr)

    data = conn.recv(10)
    print('sdfdf', data)
    if not data:
        break
    reply = b'ok ...'
    conn.sendall(reply)

conn.close()
s.close()
