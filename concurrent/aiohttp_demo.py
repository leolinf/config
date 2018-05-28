import aiohttp
import asyncio
import threading
import async_timeout


loop = asyncio.get_event_loop()


async def fetch(session, url):
#    with async_timeout.timeout(10):
    async with session.get(url, timeout=1) as response:
        print(dict(response.headers))
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        a = await fetch(session, 'https://www.baidu.com')
        print(threading.currentThread())

async def main1():
    async with aiohttp.ClientSession() as session:
        a = await fetch(session, 'https://www.python.org')
        print(threading.currentThread())


if __name__ == '__main__':
    tasks = [main(), main1()]
    loop.run_until_complete(asyncio.gather(*tasks))
    print(loop)
