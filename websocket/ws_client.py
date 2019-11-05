# -*- coding: utf-8 -*-
# WS client example
import asyncio
import websockets


async def hello():
    uri = "wss://wohuishou-sit.unicompayment.com/pushcore/"
    #uri = "ws://192.168.0.187"
    #uri = "ws://172.18.171.35:18010/pushcore/"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")
        a = {'userid': 123}
        await websocket.send(a)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
