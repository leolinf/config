# -*- coding: utf-8 -*-
# WS client example
import asyncio
import websockets


async def hello():
    uri = "ws://127.0.0.1:8181/node/sdfsfd"
    async with websockets.connect(uri) as websocket:
        a = {'userid': 123}
        await websocket.send(a)
        while True:
            greeting = await websocket.recv()
            print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
