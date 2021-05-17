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
                    "id": "123123123",
                    "username": "lin36072314",
                    "password": "Fan15181199257.",
                },
                "proxyLine": {
                    "ip": "127.0.0.1",
                    "port": 1087,
                    "username": "152.32.205.219-2000 ",
                    "password": "d1iUQB59DiWER13Gwt82"
                },
                "task": {
                    "id": '123132132313',
                    "itemId": "1234567890",
                    "taskType": "LIKE",
                    "platform": "TWITTER",
                    "param": {
                        "link": "https://twitter.com/motokorich/status/1304994515430723584",
                        "content": "",
                        }
                    }
                }
            }
        b = {"cmd":1001,"mac":"F0-18-98-18-D5-21","data":{"account":{"id":"1363671481116000256","username":"855381352654","password":"!qaz@wsx","areaCode":"855","phoneNo":"381352654","platform":"FACEBOOK"},"proxyLine":{"ip":"127.0.0.1","port":1086},"proxyIp":{"ip":"193.26.32.2","port":1111},"task":{"id":"1363738922475061248","itemId":"1363738922697359360","taskType":"LIKE","platform":"FACEBOOK","param":{"link":"https://www.facebook.com/387703671687392/posts/1144405326017219","content":None}}}}
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
