import asyncio
import websockets

async def connect_to_ws():
    uri = "ws://127.0.0.1:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to Websocket!")
            message="Who are you"
            await websocket.send(message)
            print("Sent:",message)
            #Await and print the response
            response = await websocket.recv()
            print(f"Response from server: {response}")
    except Exception as e:
        print(f"Failed to connect: {e}")
if __name__ == "__main__":
    asyncio.run(connect_to_ws())
