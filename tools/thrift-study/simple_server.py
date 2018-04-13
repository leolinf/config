# -*- coding: utf-8 -*-
# coding: utf-8
"""
thrift_client.py
"""
import socket
import sys
import logging
from hello import HelloService
from hello.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(process)d,%(threadName)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
log = logger

class HelloServiceHandler:
    def say(self, msg):
        ret = "Received: " + msg
        log.info('ret = %s', ret)
        return ret


handler = HelloServiceHandler()
processor = HelloService.Processor(handler)
transport = TSocket.TServerSocket("0.0.0.0", 9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
print("Starting thrift server in python...")
print("Starting http://0.0.0.0:9090")
server.serve()
print("done!")
