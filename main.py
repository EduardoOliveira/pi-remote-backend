
import asyncio
from aiohttp import web, WSMsgType
import json
import os
from trilobot import *
 
tbot = Trilobot()
connCounter = 0

white = (255,255,255)
leds = {
    'front_leds':{
        'state': False,
        'color': white
    }
}

async def handleMove(ws, command):
    if 'lx' in command and 'ly' in command:
        lx = command['lx']
        ly = 0 - command['ly']
        tbot.set_left_speed(ly + lx)
        tbot.set_right_speed(ly - lx)

async def handleFrontLeds(ws, command):
    
    if command == 'toggle':
        if leds['front_leds']['state'] == True:
            tbot.set_underlights(LIGHTS_FRONT, (0,0,0))
        else:
            tbot.set_underlights(LIGHTS_FRONT, leds['front_leds']['color'])
        leds['front_leds']['state'] = not leds['front_leds']['state']
    
    await ws.send_str(json.dumps(leds))

        
def handleConnection(new):
    global connCounter
    if new:
        connCounter += 1
        print(f"New connection! {connCounter} active connections")
        tbot.set_button_led(BUTTON_B, 1)
    else:
        connCounter -= 1
        print(f"Connection closed! {connCounter} active connections")
    
    if connCounter > 0:
        tbot.set_button_led(BUTTON_B, 1)
    else:
        tbot.set_button_led(BUTTON_B, 0)
        tbot.disable_motors()
    

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    handleConnection(True)
    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            command = json.loads(msg.data)
            print(command)
            if 'move' in command:
                await handleMove(ws, command['move'])
            if 'front_leds' in command:
                await handleFrontLeds(ws, command['front_leds'])
                
        elif msg.type == WSMsgType.ERROR:
            handleConnection(False)
            print('ws connection closed with exception %s' %  ws.exception())

    handleConnection(False)
    print('websocket connection closed')

    return ws

async def handleShutdown():
    counter = 0
    tbot.set_button_led(BUTTON_A, 1)
    while True:
        await asyncio.sleep(1)
        
        if tbot.read_button(BUTTON_A):
            print("Button A pressed")
            tbot.disable_motors()
            print("Motors disabled")
            counter += 1
        else:
            counter = 0
            
        if counter > 5:
            print("Shutting down")
            for i in range(5):
                tbot.set_button_led(BUTTON_A, 1)
                await asyncio.sleep(0.5)
                tbot.set_button_led(BUTTON_A, 0)
                await asyncio.sleep(0.5)
            os.system("poweroff")
            
        tbot.set_button_led(BUTTON_A, max(1-(counter*0.2),0))

async def root_handler(request):
    print('qweqwe')
    return web.HTTPFound('/index.html')

async def run_web_server():
    app = web.Application()
    app.add_routes([web.get('/ws', websocket_handler)])
    app.router.add_route('*', '/', root_handler)
    app.router.add_static('/', './www')
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()

def main():
    try:
        asyncio.get_event_loop().create_task(run_web_server())
        asyncio.get_event_loop().run_until_complete(handleShutdown())
    finally:
        print("bye bye")
        tbot.disable_motors()
        tbot.set_button_led(BUTTON_A, 0)
        
if __name__=='__main__':
    main()