# -*- encoding: utf-8 -*-

import threading
from gevent import Greenlet
import gevent


def run():
    print(threading.currentThread().getName())
    gevent.sleep(0)
    print("grevent start")

def run_test():
    print("###########")
    gevent.sleep(0)
    print("*********")

#grl = Greenlet(run)
#grl.start()
#grl.join()
#
#start = gevent.spawn(run)
#start.join()
#
gevent.joinall([gevent.spawn(run), gevent.spawn(run_test)])
