# -*- coding: utf-8 -*-

import asyncio
#@asyncio.coroutine
#def hello():
#
#    print("hello world")
#    r = yield from asyncio.sleep(1)
#    print("hello again")
#
#
#loop = asyncio.get_event_loop()
#loop.run_until_complete(hello())

#loop.close()

import threading
import requests


@asyncio.coroutine
def task():
    print("threading %s" % threading.current_thread())
    r = yield from connect()
    print("Threading %s" % threading.current_thread())
    print(r)


async def connect():
    a = requests.get("http://www.baidu.com", timeout=1)
    return a.content


loop = asyncio.get_event_loop()
tasks = [task(), task()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
