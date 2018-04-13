# coding: utf-8
import os
import sys
import traceback
import multiprocessing
import struct
import logging
import time
import socket
import signal
import gevent
import thrift
import thrift.protocol

from thrift.Thrift import TException, TMessageType
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport, TSocket
from thrift.server.TServer import TServer

from gevent.server import StreamServer
from gevent.pool import Pool


log = logging.getLogger()
service = None


class SocketTransport(TTransport.TTransportBase):
    def __init__(self, obj):
        self.socket = obj

    def isOpen(self):
        return True

    def close(self):
        self.socket.close()

    def read(self, sz):
        return self.socket.recv(sz)

    def write(self, buf):
        self.socket.sendall(buf)

    def flush(self):
        pass


class GStreamServer(StreamServer):
    """
    thrift server based on gevent StreamServer
    used must after gevent monkey patch
    @yushijun

        handler   = TestHandler()
        processor = Processor(handler)
        tfactory  = TTransport.TBufferedTransportFactory()
        pfactory  = TBinaryProtocol.TBinaryProtocolFactory()

        server = GStreamServer(('',8000), processor = processor, inputTransportFactory = tfactory, inputProtocolFactory = pfactory)
        server.serve_forever()
    """
    def __init__(self, listener, processor,
                 inputTransportFactory=None, outputTransportFactory=None,
                 inputProtocolFactory=None, outputProtocolFactory=None,
                 **kwargs):
        StreamServer.__init__(self, listener=listener, handle=self._process_socket,  **kwargs)

        self.processor = processor
        self.inputTransportFactory = inputTransportFactory
        self.outputTransportFactory = outputTransportFactory or inputTransportFactory
        self.inputProtocolFactory = inputProtocolFactory
        self.outputProtocolFactory = outputProtocolFactory or inputProtocolFactory

    def _process_socket(self, client, address):
        """A greenlet for handling a single client."""
        tstart = time.time()

        log.info('func=open|client=%s:%d|pool_size=%d', address[0], address[1], len(self.pool))
        trans = TSocket.TSocket(address[0], address[1])
        trans.setHandle(client)

        itrans = self.inputTransportFactory.getTransport(trans)
        otrans = self.outputTransportFactory.getTransport(trans)
        iprot = self.inputProtocolFactory.getProtocol(itrans)
        oprot = self.outputProtocolFactory.getProtocol(otrans)
        try:
            while True:
                self.processor.process(iprot, oprot)
        except TTransport.TTransportException as tx:
            if tx.type == TTransport.TTransportException.END_OF_FILE:
                pass
            else:
                log.error(traceback.format_exc())
        except EOFError:
            pass
        except:
            log.error(traceback.format_exc())

        itrans.close()
        otrans.close()
        log.info('func=close|client=%s:%d|time=%d', address[0], address[1], (time.time()-tstart)*1000000)


def handle(client, addr):
    fd = client.fileno()
    log.info('func=open|client=%s:%d', addr[0], addr[1])
    global service
    if not service:
        raise TException('service not initial')

    def read_frame(trans):
        frame_header = trans.readAll(4)
        sz, = struct.unpack('!i', frame_header)
        if sz < 0:
            raise TException('client must use TFramedTransport')
        frame_data = trans.readAll(sz)
        return frame_data

    def unpack_name(s):
        sz, = struct.unpack('!i', s[4:8])
        return s[8:8+sz]

    tstart = time.time()
    trans = TSocket.TSocket(addr[0], addr[1])
    trans.setHandle(client)
    try:
        #frame_data = read_frame(trans)
        #log.debug('data:%s %s', repr(frame_data), unpack_name(frame_data))
        #itran = TTransport.TMemoryBuffer(frame_data)

        itran = TTransport.TFramedTransport(trans)
        otran = TTransport.TFramedTransport(trans)
        iprot = TBinaryProtocol.TBinaryProtocol(itran, False, True)
        oprot = TBinaryProtocol.TBinaryProtocol(otran, False, True)

        service.handler.remote = addr
        p = service.Processor(service.handler)
        while True:
            p.process(iprot, oprot)
            #log.info('func=call|name=%s|time=%d', unpack_name(frame_data), (time.time()-tstart)*1000000)

        #itran.close()
        #otran.close()
    except TTransport.TTransportException as tx:
        if tx.type == TTransport.TTransportException.END_OF_FILE:
            pass
        else:
            log.error(traceback.format_exc())
    except EOFError:
        #log.error(traceback.format_exc())
        #log.info('func=close|time=%d', addr[0], addr[1], (timt.time()-tstart)*1000)
        pass
    except Exception as e:
        log.error(traceback.format_exc())
    finally:
        log.info('func=close|time=%d', (time.time()-tstart)*1000000)
        client.close()

def start_gstream(module, handler_class, addr, max_conn=1000, framed=False, max_process = 1, stop_callback = None):
    global service

    handler   = handler_class()
    processor = module.Processor(handler)
    if framed:
        tfactory = TTransport.TFramedTransportFactory()
    else:
        tfactory  = TTransport.TBufferedTransportFactory()
    pfactory  = TBinaryProtocol.TBinaryProtocolFactory()


    def signal_master_handler(signum, frame):
        global service
        log.info("signal %d catched, server will exit after all request handled", signum)
        for i in service:
            i.terminate()
    def signal_worker_handler(signum, frame):
        global service
        log.info("worker [%d] will exit after all request handled", os.getpid())
        service.close()
        if stop_callback:
            stop_callback()

    def server_forever(listener):
        global service
        log.info('worker [%d] start',os.getpid())
        service = GStreamServer( listener, processor = processor, inputTransportFactory = tfactory, inputProtocolFactory = pfactory, spawn=max_conn)
        signal.signal(signal.SIGTERM, signal_worker_handler)
        service.start()
        gevent.wait()
        log.info('worker [%d] exit', os.getpid())

    listener = GStreamServer.get_listener(addr, family = socket.AF_INET)

    log.info('server start at %s:%d pid:%d', addr[0], addr[1], os.getpid())
    if max_process == 1:
        server_forever(listener)
    else:
        service = [multiprocessing.Process(target=server_forever, args=(listener,)) for i in range(max_process)]
        for i in service:
            i.start()
        signal.signal(signal.SIGTERM, signal_master_handler)
        for i in service:
            i.join()


#def start_gevent(module, handler_class, addr, proc_process, max_conn=1000, max_process=1):
def start_gevent(module, handler_class, my_process, addr, max_conn=1000, max_process=1):
    from gevent.pool import Pool
    from gevent.server import StreamServer
    from gevent.socket import wait_write, socket


    module.handler = handler_class()
    global service
    service = module

    pool = Pool(max_conn)

    server = StreamServer(addr, handle, spawn=pool)
    server.reuse_addr = 1
    server.start()

    def server_start():
        # do_trans_all_logger()
        log.info('server started addr=%s:%d pid=%d', addr[0], addr[1], os.getpid())
        server.serve_forever()

    def _start_process(index):
        server_name = 'process%02d' % index
        process = multiprocessing.Process(target=server_start, name=server_name)
        process.start()

        return process

    # 创建工作进程
    processes = [
        _start_process(index)
        for index in range(0, max_process)
    ]
    for item in processes:
        my_process.append(item)
    #proc_process = processes
    # 等待所有的子进程结束
    map(
        lambda p: p.join(),
        processes
    )


def start_threadpool(module, handler_class, addr, max_thread=1, max_proc=1):
    import threadpool, multiprocessing, threading
    from threadpool import ThreadPool, Task
    import socket

    module.handler = handler_class()
    global service
    service = module


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.bind(addr)
    sock.listen(1024)


    def thread_run():
        # do_trans_all_logger()

        def run(obj, client, addr):
            return handle(client, addr)

        t = ThreadPool(max_thread)
        t.start()

        while True:
            try:
                client, addr = sock.accept()
                t.add(Task(run, client=client, addr=addr))
                print t.queue.qsize()
            except KeyboardInterrupt:
                os.kill(os.getpid(), 9)
            #except Queue.Full:
            #    client.close()
            except:
                client.close()
                log.debug(traceback.format_exc())

    def _start_process(index):
        server_name = 'process%02d' % index
        process = multiprocessing.Process(target=thread_run, name=server_name)
        process.start()

        return process

    # 创建工作进程
    processes = [
        _start_process(index)
        for index in range(0, max_proc)
    ]

    # 等待所有的子进程结束
    map(
        lambda p: p.join(),
        processes
    )


class ThriftServer:
    def __init__(self, module, handler_class, addr, max_process=1, max_conn=1000):
        module.handler = handler_class()
        global service
        service = module

        self.proc = None
        self.workers = []
        self.running = True

        pool = Pool(max_conn)

        self.server = StreamServer(addr, handle, spawn=pool)
        self.server.reuse_addr = 1
        self.server.start()

        def signal_master_handler(signum, frame):
            log.warn("signal %d catched in master %d, wait for kill all worker", signum, os.getpid())
            self.running = False
            for p in self.workers:
                p.terminate()

        def signal_worker_handler(signum, frame):
            log.warn("worker %d will exit after all request handled", os.getpid())
            self.server.close()

        def server_start():
            signal.signal(signal.SIGTERM, signal_worker_handler)
            log.warn('server started addr=%s:%d pid=%d', addr[0], addr[1], os.getpid())
            self.server.serve_forever()

        def _start_process(index):
            server_name = 'proc-%02d' % index
            p = multiprocessing.Process(target=server_start, name=server_name)
            p.start()
            return p

        def signal_child_handler(signum, frame):
            time.sleep(1)
            if self.running:
                log.warn("master recv worker exit, fork one")
                try:
                    pinfo = os.waitpid(-1, 0)
                    pid = pinfo[0]

                    index = -1
                    for i in range(0, len(self.workers)):
                        p = self.workers[i]
                        if p.pid == pid:
                            index = i
                            break

                    if index >= 0:
                        self.workers[index] = _start_process(index)
                except OSError:
                    log.info('waitpid error:')



        if max_process == 1:
            signal.signal(signal.SIGTERM, signal_worker_handler)
            gevent.spawn(self.forever)
            server_start()
        else:
            for i in range(0, max_process):
                self.workers.append(_start_process(i))

            signal.signal(signal.SIGTERM, signal_master_handler)
            signal.signal(signal.SIGCHLD, signal_child_handler)

    def forever(self):
        try:
            while self.running:
                if len(self.workers) > 0:
                    time.sleep(60)
                else:
                    gevent.sleep(60)
                log.debug('report ...')
            log.warn('master exit')
        except Exception, e:
            log.warn('master exception: %s', str(e))
        finally:
            self.running = False
            time.sleep(3)
            for p in self.workers:
                p.terminate()

    def stop(self):
        pass

class RunGeventServer:
    def __init__(self, module, handler_class, addr, max_conn=1000, max_process=1):
        self.my_process = []
        self.module = module
        self.handler_class = handler_class
        self.addr = addr
        self.max_conn = max_conn
        self.max_process = max_process


    def run(self):
        start_gevent(self.module, self.handler_class, self.my_process, self.addr, self.max_conn, self.max_process)

    def stop(self):
        for p in self.my_process:
            p.terminate()
