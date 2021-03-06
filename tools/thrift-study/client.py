# -*-coding: utf-8 -*-

import time
import random
import socket
import traceback
import logging
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


log = logging.getLogger()

Urllib2Client = None


class ThriftClient:
    def __init__(self, server, thriftmod, timeout=0, framed=False, raise_except=False):

        '''server - 为Selector对象，或者地址{'addr':('127.0.0.1',5000),'timeout':1000}'''

        self.starttime = time.time()
        self.server_selector = None
        self.server = server
        self.client = None
        self.thriftmod = thriftmod
        self.frame_transport = framed
        self.raise_except = raise_except  # 是否在调用时抛出异常
        self.timeout = timeout

        while True:
            if self.open() == 0:
                break

    def open(self):

        starttime = time.time()
        err = ''
        self.transport = None
        #try:
    #    self.server = self.server_selector.next()
        if not self.server:
            restore(self.server_selector, self.thriftmod)

    #        self.server = self.server_selector.next()
            if not self.server:
                log.error('server=%s|err=no server!', self.thriftmod.__name__)
                raise Exception
        addr = self.server['addr']

        try:
            self.socket = TSocket.TSocket(addr[0], addr[1])
            if self.timeout > 0:
                self.socket.setTimeout(self.timeout)
            else:
                self.socket.setTimeout(self.server['timeout'])
            if self.frame_transport:
                self.transport = TTransport.TFramedTransport(self.socket)
            else:
                self.transport = TTransport.TBufferedTransport(self.socket)
            protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

            self.client = self.thriftmod.Client(protocol)
            self.transport.open()
        except Exception as e:
            err = str(e)
            log.error(traceback.format_exc())
            self.server['valid'] = False

            if self.transport:
                self.transport.close()
                self.transport = None
        finally:
            endtime = time.time()
            addr = self.server['addr']
            tname = self.thriftmod.__name__
            pos = tname.rfind('.')
            if pos > 0:
                tname = tname[pos+1:]
            msg = 'server=%s|func=open|addr=%s:%d/%d|time=%d|err=%s' % (
                tname, addr[0], addr[1], self.server['timeout'],
                int((endtime-starttime)*1000000), repr(err)
            )
            log.info(msg)
        if not err:
            return 0
        return -1

    def __del__(self):
        self.close()

    def close(self):
        if self.transport:
            self.transport.close()
            self.transport = None
            self.client = None

    def call(self, funcname, *args, **kwargs):
        def _call_log(ret, err=''):
            endtime = time.time()
            addr = self.server['addr']
            tname = self.thriftmod.__name__
            pos = tname.rfind('.')
            if pos > 0:
                tname = tname[pos+1:]

            s = 'server=%s|func=%s|addr=%s:%d/%d|time=%d|framed=%s|args=%d|kwargs=%d' % \
                    (tname, funcname,
                    addr[0], addr[1],
                    self.server['timeout'],
                    int((endtime-starttime)*1000000),
                    self.frame_transport,
                    len(args), len(kwargs))
            if err:
                s += '|err=%s' % (repr(err))
                log.warn(s)
            else:
                log.info(s)

        starttime = time.time()
        ret = None
        try:
            func = getattr(self.client, funcname)
            ret = func(*args, **kwargs)
        except Exception as e:
            _call_log(ret, e)
            #如果是thrift自定义的异常
            if 'thrift_spec' in dir(e):
                log.warn(traceback.format_exc())
            else:
                log.error(traceback.format_exc())
            if self.raise_except:
                raise
        else:
            _call_log(ret)
        return ret

    def __getattr__(self, name):
        def _(*args, **kwargs):
            return self.call(name, *args, **kwargs)
        return _

def restore(selector, thriftmod, framed=False):
    invalid = selector.not_valid()
    log.debug('invalid server:%s', invalid)
    for server in invalid:
        transport = None
        try:
            log.debug('try restore %s', server['server']['addr'])
            addr = server['server']['addr']
            transport = TSocket.TSocket(addr[0], addr[1])
            transport.setTimeout(server['server']['timeout'])
            if framed:
                transport = TTransport.TFramedTransport(transport)
            else:
                transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = thriftmod.Client(protocol)
            transport.open()
            client.ping()
        except:
            log.error(traceback.format_exc())
            log.debug("restore fail: %s", server['server']['addr'])
            continue
        finally:
            if transport:
                transport.close()

        log.debug('restore ok %s', server['server']['addr'])
        server['valid'] = True
