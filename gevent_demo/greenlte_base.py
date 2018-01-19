# -*- encoding: utf-8 -*-

import threading
from greenlet import greenlet


def test1():
    print(threading.currentThread().getName())
    gr2.switch()
    print(1)


def test2():
    print(2)
    print(threading.currentThread().getName())
    gr1.switch()


gr1 = greenlet(test1)
gr2 = greenlet(test2)
gr1.switch()
