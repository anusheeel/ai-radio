import asyncio
import websockets

async def send_message():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        message = "Hello from test client!"
        print(f"Sending message: {message}")
        await websocket.send(message)

        # Optionally wait for a response
        response = await websocket.recv()
        print(f"Received response: {response}")

asyncio.run(send_message())
