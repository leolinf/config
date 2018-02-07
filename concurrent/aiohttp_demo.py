import aiohttp
import asyncio
import async_timeout


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            await response.text()
            return

async def main():
    async with aiohttp.ClientSession() as session:
        await fetch(session, 'http://www.baidu.com')
        return

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(dir(loop))
