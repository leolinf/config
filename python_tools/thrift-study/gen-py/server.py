# -*- coding: utf-8 -*-
import socket
import sys
from hello import HelloService
from hello.ttypes import *

from thrift.transport import TSocket, TTransport
from thrift.server import TServer
from thrift.protocol import TBinaryProtocol


class HelloServiceHanlder():

    def say(self, msg):
        ret = "Hello " + msg
        print(ret)
        return ret



handler = HelloServiceHanlder()
processer = HelloService.Processor(handler)
transport = TSocket.TServerSocket("localhost", 9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()


#server = TServer.TSimpleServer(processer, transport, tfactory, pfactory)
server = TServer.TThreadPoolServer(processer, transport, tfactory, pfactory)
print("---------------begin----------------")
server.serve()
print("---------------end---------------")
