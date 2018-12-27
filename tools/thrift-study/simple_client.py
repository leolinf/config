# -*- coding: utf-8 -*-
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport, TZlibTransport
from thrift.protocol import TBinaryProtocol, TCompactProtocol, TJSONProtocol
from hello import HelloService, ttypes


def client_call(*args, **kwargs):
    # 监听端口
    transport = TSocket.TSocket('0.0.0.0', 9090)
    transport.setTimeout(3000)
    # 选择传输层
    transport = TTransport.TBufferedTransport(transport)
#    transport = TTransport.TFramedTransport(transport)
#    transport = TZlibTransport.TZlibTransport(transport)

    # 选择传输协议
#    protocol = TBinaryProtocol.TBinaryProtocol(transport)  # 二进制格式
    protocol = TBinaryProtocol.TBinaryProtocolAccelerated(transport)  # 二进制格式加速版
#   protocol = TCompactProtocol.TCompactProtocol(transport)  # 压缩格式
#   protocol = TJSONProtocol.TJSONProtocol(transport)  # json 格式

    # 调用服务端handler
    client = HelloService.Client(protocol)
    transport.open()
    print('sdfsdfdsf')
    msg = client.say(args[0])
    print(msg)
    transport.close()


def main():
    try:
        msg = ttypes.Msg()
        msg.name = '王'.decode('utf-8')
        client_call(msg)
    except Thrift.TException as ex:
        print("%s" % (ex.message))
        return Exception(ex.message)


if __name__ == "__main__":
    main()
