# -*- coding: utf-8 -*-

import logging
from hello import HelloService

from thrift.transport import TSocket
from thrift.transport import TTransport, TZlibTransport
from thrift.protocol import (
    TBinaryProtocol, TCompactProtocol, TJSONProtocol
)
from thrift.server import TServer, TNonblockingServer, THttpServer, TProcessPoolServer

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(process)d,%(threadName)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
log = logger


class HelloServiceHandler:
    def say(self, msg):
        log.info("Received: ")
        log.info(msg)
        return msg.name


# 创建对应的服务处理
handler = HelloServiceHandler()
processor = HelloService.Processor(handler)
# 监听端口
transport = TSocket.TServerSocket("0.0.0.0", 9090)

# 选择传输层
tfactory = TTransport.TBufferedTransportFactory()
# tfactory = TTransport.TFramedTransportFactory()
# tfactory = TZlibTransport.TZlibTransportFactory()

# 选择传输协议
pfactory = TBinaryProtocol.TBinaryProtocolFactory()  # 二进制格式
# pfactory = TBinaryProtocol.TBinaryProtocolAcceleratedFactory()  # 二进制格式加速版
# pfactory = TCompactProtocol.TCompactProtocolFactory()  # 压缩格式
# pfactory = TJSONProtocol.TJSONProtocolFactory()  # json格式

# 选择服务模型
# server = THttpServer.THttpServer(processor, ("0.0.0.0", 9090), tfactory, pfactory)  # http
server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)  # 单进程
# server = TProcessPoolServer.TProcessPoolServer(processor, transport, tfactory, pfactory)  #  进程池
# server = TNonblockingServer.TNonblockingServer(processor, transport, pfactory, pfactory)  # 非阻塞(client 必须使用TFramedTransport 传输)

log.info("Starting thrift server in python...")
log.info("Starting host:0.0.0.0,port:9090")
# 启动
server.serve()
