# -*- encoding: utf-8 -*-

from gevent import monkey
monkey.patch_all()

import threading
from gevent import Greenlet
from gevent import sleep
import gevent
from greenlet import greenlet

from geventhttpclient import HTTPClient
from geventhttpclient.url import URL
import gevent.pool



def run():
    print(threading.currentThread())
    gevent.sleep(0)

def run_test():
    print(threading.currentThread())
    gevent.sleep(0)

def test1():
    print(threading.currentThread())
    gr2.switch()


def test2():
    print(threading.currentThread())
    gr1.switch()


def print_friend_username(item, http):
    response = http.get('')
    print(response.status_code)
    print(threading.currentThread())


def main1():
    http = HTTPClient.from_url('https://www.baidu.com', concurrency=10)
    pool = gevent.pool.Pool(10000)

    for item in range(1, 10):
        pool.spawn(print_friend_username, item, http)

    pool.join()
    http.close()


def main():

    #grl = Greenlet(run)
    #grl.start()
    #grl.join()

    #start = gevent.spawn(run)
    #start.join()

    gevent.joinall([gevent.spawn(run), gevent.spawn(run_test)])


if __name__ == '__main__':
    gr1 = greenlet(test1)
    gr2 = greenlet(test2)
    gr1.switch()
    main()
    main1()
