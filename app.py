import asyncio
import websockets
import json

MOBILE_CLIENTS = set()
TD_CLIENTS = set()

async def handler(ws):
    role = None
    try:
        # primer mensaje = identificación
        msg = await ws.recv()
        data = json.loads(msg)
        role = data.get("role")
        print(msg)  # <-- debug aquí
        if role == "mobile":
            MOBILE_CLIENTS.add(ws)
            print("Mobile connected")
        elif role == "td":
            TD_CLIENTS.add(ws)
            print("TD connected")
        else:
            return

        async for msg in ws:
            # solo reenviamos mensajes de móviles hacia TD
            if role == "mobile":
                print("Mensaje recibido del móvil:", msg)  # <-- debug aquí
                for td in TD_CLIENTS.copy():
                    try:
                        await td.send(msg)
                    except:
                        TD_CLIENTS.discard(td)

    finally:
        MOBILE_CLIENTS.discard(ws)
        TD_CLIENTS.discard(ws)
        print("Client disconnected")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8080):
        print("WebSocket server on ws://localhost:8080")
        await asyncio.Future()  # run forever

asyncio.run(main())