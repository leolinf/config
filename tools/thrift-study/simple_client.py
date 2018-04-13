# -*- coding: utf-8 -*-
"""
thrift_client.py
"""

from hello import HelloService

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def client_call(msg):
    try:
        transport = TSocket.TSocket('localhost', 9090)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = HelloService.Client(protocol)
        transport.open()
        print("client - say = %s", msg)
        msg = client.say(msg)
        print("server - " + msg)
        transport.close()
        return msg

    except Thrift.TException as ex:
        print("%s" % (ex.message))
        raise Exception(ex.message)
