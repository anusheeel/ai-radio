import asyncio
import websockets
import json
import traceback  # Import traceback to print the full error details
from api_clients.connectGpt import connect_ChatGPTViaOpenRouter
from api_clients.elevenlabsTransformer import textSpeech
from script_Tap.cleanApiResponse import extract_relevant_information


async def connect_to_server():
    uri = "ws://127.0.0.1:8000/ws"
    print("Attempting to connect to WebSocket server...")
    try:
        async with websockets.connect("ws://127.0.0.1:8000/ws", ping_interval=20, ping_timeout=30) as websocket:
            print("Connected to WebSocket server.")
            # Send client type upon connecting
            await websocket.send("humanGPT")
            print("Waiting for message from server...")
            while True:
                # Receive message from orchestrator
                message = await websocket.recv()
                print(f"Received message: {message}")        
                # Generate response using OpenAI or other LLM API
                response = connect_ChatGPTViaOpenRouter(message)
                #Check Response Type
                print(f"Generated response: {response}, type: {type(response)}")
                #cleanDictionary = extract_relevant_info(response)
                #content = response["choices"][0]["message"]["content"].strip()
                #audio = textSpeech(content,"9BWtsMINqrJLrRacOk9x")
                # Send response back to the orchestrator
                print("This is the raw type coming out from gpt client---------------")
                print(type(response))
                await websocket.send(json.dumps(response))
                print("Response sent back to server.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Full traceback:")
        traceback.print_exc()

def main():
    asyncio.run(connect_to_server())
main()
