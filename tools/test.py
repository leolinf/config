# -*- coding: utf-8 -*-
import redis
from flask import Flask
import asyncio
import logging
from log.logger_color_3 import logger


client = redis.from_url('redis://192.168.0.7:6379')


async def getValue(i):
    ret = client.get(i)
    logger.info('$$$$$$$')
    logger.info(ret)
    logger.debug(ret)
    logger.warn(ret)
    logger.info('哇哦')
    return ret


def runEpool():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [getValue(i) for i in range(10)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


app = Flask(__name__)


@app.route('/asyncio')
def hello():
    runEpool()
    return 'success'
