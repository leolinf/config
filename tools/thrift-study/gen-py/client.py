# -*- coding: utf-8 -*-

from hello import HelloService

import sys

from thrift import Thrift
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol

def main():
    try:
        transport = TSocket.TSocket("localhost", 9090)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = HelloService.Client(protocol)
        transport.open()
        print("client - say")
        msg = client.say("world")
        print("server - " + msg )
        transport.close()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
