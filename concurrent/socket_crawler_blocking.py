# -*- coding: utf-8 -*-

import socket
import time
from concurrent import futures

import logging
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(process)d,%(threadName)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
log = logger

def bloking_now():
    sock = socket.socket()
    sock.connect(("example.com", 80))
    request = "GET / HTTP/1.1\r\n\r\n"
    sock.send(request.encode())
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        log.info(b'handler+++++++' + response[:10])
        chunk = sock.recv(4096)
    return response


def nolock_way():
    sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect(('example.com', 80))
    except BlockingIOError:
        pass
    request = "GET / HTTP/1.1\r\n\r\n"
    data = request.encode()
    while True:
        try:
            sock.send(data)
            break
        except OSError:
            pass
    response = b''
    while True:
        try:
            chunk = sock.recv(4096)
            while chunk:
                response += chunk
                chunk = sock.recv(4096)
            log.info(b'handler+++++++' + response[:10])
            break
        except OSError:
            pass
    return response


def sync_way():
    res = []
    for i in range(10):
        res.append(bloking_now())
    return len(res)


def sync_noblocking_way():
    res = []
    for i in range(10):
        res.append(nolock_way())
    log.warn(res)
    return len(res)


def process_way():
    workers = 10
    with futures.ProcessPoolExecutor(workers) as executor:
        futs = {executor.submit(bloking_now) for i in range(10)}
    res = [fut.result() for fut in futs]
    return len(res)


def thread_way():
    workers = 10
    with futures.ThreadPoolExecutor(workers) as executor:
        futs = {executor.submit(bloking_now) for i in range(10)}
    res = [fut.result() for fut in futs]
    return len(res)


if __name__ == "__main__":
    star_time = time.time()
    # sync_way()
    sync_noblocking_way()
    process_way()
    thread_way()
    print('------end------- \n time=%s'%(time.time()-star_time))
