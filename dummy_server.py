import asyncio
from typing import List
import websockets
import traceback

connections: List[websockets.WebSocketServerProtocol] = []

async def event_loop():
    while True:
        print("Start event loop.")
        for ws in connections:
            try:
                await ws.send("date")
                print(f"{ws=}: Message sent.")
            except:
                traceback.print_exception()
        print("Finished event loop.")
        await asyncio.sleep(3)


async def handle_client(websocket: websockets.WebSocketServerProtocol, path):
    connections.append(websocket)
    try:
        while True:
            # クライアントからのメッセージを受信
            received_message = await websocket.recv()
            print(f"Received from client: {received_message}")

            # 10秒待機
            asyncio.sleep(10)
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
        connections.remove(websocket)

async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        print("WebSocket server started at ws://localhost:8765")
        # await asyncio.Future()  # サーバーを永続的に動作させる
        await event_loop()

asyncio.run(main())