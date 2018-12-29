# -*- coding: utf-8 -*-

import socket

from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ


selector = DefaultSelector()
stopped = False
url_todo = ['/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9']


class Crawler:

    def __init__(self, url):
        self.url = url
        self.sock = None
        self.response = b''

    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('example.com', 80))
        except BlockingIOError:
            pass
        selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)

    def connected(self, key, mask):
        selector.unregister(key.fd)
        get = 'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n'
        self.sock.send(get.encode())
        selector.register(key.fd, EVENT_READ, self.read_response)

    def read_response(self, key, mask):
        global stopped
        chunk = self.sock.recv(4096)
        if chunk:
            self.response += chunk
        else:
            selector.unregister(key.fd)
            url_todo.remove(self.url)
            if not url_todo:
                stopped = True



def loop():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback(event_key, event_mask)


if __name__ == '__main__':
    import time
    a = time.time()
    for url in url_todo:
        crawler = Crawler(url)
        crawler.fetch()
    loop()
    print(time.time()-a)
