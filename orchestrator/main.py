import asyncio
import uvicorn
import random
from fastapi import FastAPI, WebSocket
from audioPlayer.audioPlayer import playAudio
from personalities.base_personality import start_conversation, handle_ai_response, get_context, generate_prompt, update_context
from script_Tap.tapPipe import tapPipe
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
            initial_message = ("Welcome to the AI Radio Show! Today, our topic is 'Nepal, The country of mountains'. "
                               "humanGPT, please start by introducing yourself briefly and then prompt humanClaude for their thoughts on the day's topic.")
            print(f"Sending initial message to first client: {initial_message}")
            await websocket.send_text(initial_message)
            handle_ai_response(context_id, initial_message, "system")
        
        # Main loop for conversation handling
        while True:
            await natural_pause()
            
            # Only proceed if it's this client's turn
            if client_index == current_turn:
                try:
                    # Receive message from this client
                    data = await websocket.receive_text()
                    print(data)
                    dialouge = tapPipe(data) 
                    playAudio(dialouge)
                    # Determine the speaker name based on turn
                    speaker = "humanGPT" if current_turn == 0 else "humanClaude"
                    handle_ai_response(context_id, data, speaker)

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
        "your_app_file:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        timeout_keep_alive=300,  # Increase the keep-alive timeout
        log_level="info"
    )
