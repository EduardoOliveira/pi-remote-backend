
import asyncio
import json
import websockets
from trilobot import *
 
tbot = Trilobot()

async def handler(websocket, path):
    try:
        while True:
            data = await websocket.recv()
            command = json.loads(data)
            
            reply = f"Data recieved as:  {command}!"
            print(reply)
            lx = command['lx']
            ly = 0 - command['ly']
            tbot.set_left_speed(ly + lx)
            tbot.set_right_speed(ly - lx)
            await websocket.send(reply)
    except Exception as e:
        print(e)
        # Cannot find 'LX', 'LY', or 'RY' on this controller
        tbot.disable_motors()
   

start_server = websockets.serve(handler, "0.0.0.0", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
tbot.disable_motors()