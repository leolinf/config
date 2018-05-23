# -*- coding: utf-8 -*-

import threading
import requests
import asyncio

loop = asyncio.get_event_loop()


@asyncio.coroutine
def hello():

    print("hello world")
    r = yield from asyncio.sleep(1)
    print("hello again")


#@asyncio.coroutine
async def task():
    print("threading %s" % threading.current_thread())
    r = await connect()
    print("Threading %s" % threading.current_thread())


async def connect():
    a = requests.get("http://www.baidu.com", timeout=1)
    return a.content[:10]


loop.run_until_complete(hello())

tasks = [task(), task()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
