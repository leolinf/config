# -*- coding: utf-8 -*-
"""
thrift_client.py
"""

# from hello import HelloService
import os, sys

HOME = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(HOME))
print(HOME)


from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from client import ThriftClient
from summer import Spring
from log.logg import logger

TEST_SERVER = {"addr": ("0.0.0.0", 7110), "timeout": 2000}



async def client_call(*args, **kwargs):
    try:
        '''
        client = ThriftClient(TEST_SERVER, Spring, framed=True)
        client.raise_except = True
        #ret = client.call('getssn', *args, **kwargs)
        ret = client.call('getssn', *args, **kwargs)
        return ret
        '''
        transport = TSocket.TSocket('192.168.0.7', 7110)
        transport.setTimeout(1000)
        transport = TTransport.TBufferedTransport(transport)
        transport = TTransport.TFramedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = Spring.Client(protocol)
        transport.open()
        msg = client.getssn()
        #msg = client.say(msg)
        logger.debug(msg)
        transport.close()
        return msg

    except Thrift.TException as ex:
        print("%s" % (ex.message))
        return Exception(ex.message)


import asyncio
loop = asyncio.get_event_loop()

def main():
    import sys
    a = int(sys.argv[1])
    while 1:
        tasks = [client_call() for i in range(a)]
        loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == "__main__":
    main()
