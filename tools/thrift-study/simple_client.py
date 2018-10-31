# -*- coding: utf-8 -*-
"""
thrift_client.py
"""

# from hello import HelloService

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from client import ThriftClient
from summer import Spring

TEST_SERVER = {"addr": ("0.0.0.0", 7110), "timeout": 2000}


def client_call(*args, **kwargs):
    try:
        '''
        client = ThriftClient(TEST_SERVER, Spring, framed=True)
        client.raise_except = True
        #ret = client.call('getssn', *args, **kwargs)
        ret = client.call('getssn', *args, **kwargs)
        return ret
        '''
        transport = TSocket.TSocket('0.0.0.0', 7110)
        transport.setTimeout(1000)
        transport = TTransport.TBufferedTransport(transport)
        transport = TTransport.TFramedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = Spring.Client(protocol)
        transport.open()
        msg = client.getssn()
        #msg = client.say(msg)
        print(msg)
        transport.close()
        return msg

    except Thrift.TException as ex:
        print("%s" % (ex.message))
        raise Exception(ex.message)


if __name__ == "__main__":
    client_call()
