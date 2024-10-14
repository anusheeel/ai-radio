import asyncio
import uvicorn
import random
from fastapi import FastAPI, WebSocket
from audio_player.audio_player import play_audio_sync
from personalities.base_personality import start_conversation, handle_ai_response, get_context, generate_prompt, update_context
from script_Tap.tapPipe import tapPipe
from script_Tap.cleanApiResponse import extract_relevant_information

from orchestrator.initializer import initialize
app = FastAPI()
connected_clients = []
context_id = None
current_turn = 0

async def natural_pause():
    """Introduce a natural pause to simulate thinking time."""
    pause_duration = random.uniform(0.5, 2.0)  # Random pause between 0.5 and 2 seconds
    await asyncio.sleep(pause_duration)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global context_id, current_turn
    await websocket.accept()
    connected_clients.append(websocket)
    client_index = len(connected_clients) - 1  # Index of the newly connected client
    print(f"Connected Clients: {connected_clients}")  # Debugging line
    
    try:
        # Expect the client to send its type when connecting
        personality_name = await websocket.receive_text()
        print(f"Personality Name: {personality_name}")
        
        # Create context with personality name if it's the first client
        if context_id is None:
            context_id = start_conversation(personality_name)
        
        # Ensure the first message goes to the first client
        if client_index == 0:
            initial_message = ("Welcome to the AI Radio Show! Today, our topic is AI Radio. We will talk about How we can make this technology a revolutionary 360 audio entertainment platform.  "
                               "humanGPT, please start by introducing yourself briefly and then prompt humanClaude for their thoughts on the day's topic. Make sure you dont hallucinate and pretend yourself to be next speaker")
            #trigger_message = initialize()
            print(f"Sending initial message to first client: {initial_message}")
            await websocket.send_text(initial_message)
            handle_ai_response(context_id,initial_message,"system")
        
        # Main loop for conversation handling
        while True:
            await natural_pause()
            
            # Only proceed if it's this client's turn
            if client_index == current_turn:
                try:
                    # Receive message from this client
                    data = await websocket.receive_json()
                    relevantInfo = extract_relevant_information(data)
                    print(f"this is the type returned by{personality_name}")
                    print(relevantInfo)
                    #dialogue = tapPipe(data) 
                    # Wait for the current dialogue to be fully played
                    #await play_and_wait(dialogue)
                    # Determine the speaker name based on turn
                    speaker = "humanGPT" if current_turn == 0 else "humanClaude"
                    handle_ai_response(context_id, relevantInfo, speaker)

                    # Move to the next client's turn
                    current_turn = (current_turn + 1) % len(connected_clients)
                    
                    # Get the updated conversation context and generate a prompt for the next speaker
                    current_context = get_context(context_id)
                    guidance = {}  # Assume no special guidance
                    prompt = generate_prompt(current_context, guidance)
                    
                    # Send the prompt to the next client in line
                    await broadcast_message(prompt)
                except Exception as e:
                    print(f"Receive error: {e}")
                    break
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        connected_clients.remove(websocket)
        print(f"Client disconnected. Remaining clients: {len(connected_clients)}")
async def play_and_wait(dialogue):
    """
    Play the dialogue and wait for it to complete before proceeding to the next.
    """
    try:
        print(f"Playing dialogue: {dialogue}")
        await asyncio.to_thread(play_audio_sync, dialogue)  # Ensures playAudio runs synchronously and we wait for completion
        print("Finished playing audio")
    except Exception as e:
        print(f"Error playing audio: {e}")

async def broadcast_message(message):
    global current_turn
    
    if connected_clients:
        # Determine the index of the client to send the message to
        next_client_index = current_turn
        
        print(f"Next turn set to client index {next_client_index}, sending message...")
        
        # Send the message to the appropriate client
        await connected_clients[next_client_index].send_text(message)

if __name__ == "__main__":
    uvicorn.run(
        "orchestrator.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        timeout_keep_alive=300,  # Increase keep-alive timeout
        log_level="info"
    )