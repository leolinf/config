# -*- coding: utf-8 -*-


import socket

from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ


selector = DefaultSelector()
stopped = False
url_todo = ['/']


class Fulture:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)

    def __iter__(self):
        yield self
        return self.result


class Crawler:

    def __init__(self, url):
        self.url = url
        self.response = b''

    def fetch(self):

        sock = socket.socket()

        sock.setblocking(False)
        try:
            sock.connect(('baidu.com', 80))
        except BlockingIOError:
            pass

        f = Fulture()

        def on_conected():
            f.set_result(None)
        selector.register(sock.fileno(), EVENT_WRITE, on_conected)
        yield f
        selector.unregister(sock.fileno())

        global stopped
        get = 'GET / HTTP/1.0\r\nHost: baidu.com\r\n\r\n'
        sock.send(get.encode('ascii'))
        while True:
            f = Fulture()
            def on_readable():
                f.set_result(sock.recv(4096))
            selector.register(sock.fileno(), EVENT_READ, on_readable)
            chunk = yield f
            selector.unregister(sock.fileno())
            if chunk:
                self.response += chunk
            else:
                url_todo.remove(self.url)
                if not url_todo:
                    stopped = True
                    break


class Task:
    def __init__(self, coro):
        self.coro = coro
        f = Fulture()
        f.set_result(None)
        self.step(f)

    def step(self, fulture):
        try:
            next_fulture = self.coro.send(fulture.result)
        except StopIteration:
            return
        next_fulture.add_done_callback(self.step)


def loop():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback()


if __name__ == '__main__':
    import time
    a = time.time()
    for url in url_todo:
        crawler = Crawler(url)
        Task(crawler.fetch())
    loop()
    print(time.time()-a)
