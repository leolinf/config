# -*- coding: utf-8 -*-

import asyncio
import aiohttp


host = 'https://www.baidu.com'
urls_todo = ['/', '/1', '/2']


loop = asyncio.get_event_loop()


async def fetch(url):
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(url) as response:
            return await response.read()


if __name__ == "__main__":
    import time
    a = time.time()
    tasks = [fetch(host) for i in urls_todo]
    loop.run_until_complete(asyncio.gather(*tasks))
    print(time.time() - a)
