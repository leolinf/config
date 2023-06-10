# -*- coding: utf-8 -*-
import time
import json
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
from tornado.queues import Queue
import tornado.web
import socket
'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes.
'''

global_ws = []


class WSHandler(tornado.websocket.WebSocketHandler):

    def open(self, *args):
        print(args)
        print('new connection')
        global_ws.append(self)

    def on_message(self, message):
        print('message received:  %s' % message)
        # Reverse Message and send it back
        # print('sending back message: %s' % message[::-1])
        # self.write_message(message[::-1])

    def on_close(self):
        print('connection closed')
        global_ws.pop(0)

    @classmethod
    def new_send(cls, message):
        global_ws[0].write_message(message)

    def check_origin(self, origin):
        return True


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
        a = {
            "cmd": 1001,
            "data": {
                "account": {
                    "id": "123123123123123",
                    "username": "timdenglin",
                    "password": "asdfghjkl.123",
                    "phoneNo": "447867903305",
                },
                "proxyLine": {
                    "ip": "47.242.225.168",
                    "port": 40001,
                },
                "task": {
                    "id": '123132132313123123',
                    "itemId": "1234567890234234",
                    "taskType": "FOLLOW",
                    "platform": "FACEBOOK",
                    "param": {
                        # "link": "https://www.facebook.com/permalink.php?story_fbid=10152283823810813&id=348993755812",
                        # "link": "https://www.facebook.com/387703671687392/posts/1144405326017219",
                        "link": "https://www.facebook.com/cnliziqi",
                        "content": "very good",
                        }
                    }
                }
            }
        WSHandler.new_send(json.dumps(a))


application = tornado.web.Application([
    (r'/node/(.*)', WSHandler),
    (r'/test', MainHandler),
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8181)
    myIP = socket.gethostbyname(socket.gethostname())
    print('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
