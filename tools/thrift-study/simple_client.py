# -*- coding: utf-8 -*-
"""
thrift_client.py
"""

from hello import HelloService

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from client import ThriftClient

TEST_SERVER = {"addr": ("0.0.0.0", 9090), "timeout": 2000}


def client_call(*args, **kwargs):
    try:
        client = ThriftClient(TEST_SERVER, HelloService, framed=False)
        client.raise_except=True
        ret = client.call('say', *args, **kwargs)
        return ret
        '''
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
        '''

    except Thrift.TException as ex:
        print("%s" % (ex.message))
        raise Exception(ex.message)


if __name__ == "__main__":
    req = client_call('123')
    print(req)
