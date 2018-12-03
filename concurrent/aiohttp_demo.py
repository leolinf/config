import aiohttp
import asyncio
import threading
import async_timeout
import logging


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(process)d,%(thread)d %(threadName)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
loop = asyncio.get_event_loop()


async def fetch(session, url):
#    with async_timeout.timeout(10):
    async with session.get(url, timeout=1) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        a = await fetch(session, 'https://www.baidu.com')
        logger.info('succ')

async def main1():
    async with aiohttp.ClientSession() as session:
        a = await fetch(session, 'https://www.python.org')
        logger.info('succ')


if __name__ == '__main__':
    tasks = [main(), main1()]
    loop.run_until_complete(asyncio.gather(**tasks))
