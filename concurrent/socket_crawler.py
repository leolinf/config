# -*- coding: utf-8 -*-

import socket


def bloking_now():
    sock = socket.socket()
    sock.connect(("baidu.com", 80))
    request = "GET / HTTP/1.1\r\n\r\n"
    sock.send(request.encode("ascii"))
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        chunk = sock.recv(4096)
    return response


def sync_way():
    res = []
    for i in range(10):
        res.append(bloking_now())
    return len(res)


if __name__ == "__main__":
    sync_way()
