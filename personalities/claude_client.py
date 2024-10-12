import asyncio
import websockets
import traceback  # Import traceback to print the full error details
from api_clients.connectClaude import connect_claude_via_openrouter
from api_clients.elevenlabsTransformer import textSpeech


async def connect_to_server():
    uri = "ws://127.0.0.1:8000/ws"
    print("Attempting to connect to WebSocket server...")
    try:
        async with websockets.connect("ws://127.0.0.1:8000/ws", ping_interval=20, ping_timeout=30) as websocket:
            print("Connected to WebSocket server.")
            # Send client type upon connecting
            await websocket.send("humanClaude")
            print("Waiting for message from server...")
            while True:
                # Receive message from orchestrator
                message = await websocket.recv()
                print(f"Received message: {message}")        
                # Generate response using OpenAI or other LLM API
                response = connect_claude_via_openrouter(message)
                print(f"Generated response: {response}")
                #Check Response Type
                print(f"Generated response: {response}, type: {type(response)}")
                #content = response["choices"][0]["message"]["content"].strip()
                #audio = textSpeech(content,"9BWtsMINqrJLrRacOk9x")
                # Send response back to the orchestrator
                await websocket.send(str(response))
                print("Response sent back to server.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Full traceback:")
        traceback.print_exc()
def main():
    asyncio.run(connect_to_server())
main()
