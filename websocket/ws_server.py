# -*- coding: utf-8 -*-
import asyncio
import websockets
import time
import json


global client_dict
client_dict = {}


async def hello(websocket, path):
    while True:
        name = await websocket.recv()
        try:
            print('path {} recived {}'.format(path, name))
            client_dict[path] = websocket
            data = json.loads(name)
            cmd = data['cmd']
            if cmd == 1:
                continue
            if cmd == 1001:
                if data['data']['task'].get('executeState'):
                    pass
                else:
                    await websocket.send(name)
        except:
            print('send {}'.format(name))
            await websocket.send(name)

start_server = websockets.serve(hello, "0.0.0.0", 8181)
print('start 0.0.0.0:8181')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
