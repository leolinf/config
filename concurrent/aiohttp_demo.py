import aiohttp
import asyncio
import async_timeout


loop = asyncio.get_event_loop()


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            a = await response.read()
            print(a[:10])
            try:
                return await response.text()
            except:
                print( await response.content)


async def main():
    async with aiohttp.ClientSession() as session:
        return await fetch(session, 'http://www.baidu.com')


if __name__ == '__main__':
    tasks = [main() for i in range(100)]
    loop.run_until_complete(asyncio.gather(*tasks))
