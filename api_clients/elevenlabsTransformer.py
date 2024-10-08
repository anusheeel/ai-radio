from elevenlabs import ElevenLabs, VoiceSettings
from audioPlayer.audioPlayer import playAudio
from dotenv import load_dotenv
import os
import requests
#Load openrouter API Key
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
CHUNK_SIZE = 1024
def textSpeech(message,voiceId):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voiceId}"
    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": ELEVENLABS_API_KEY
    }

    data = {
    "text": message,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
    }
    response = requests.post(url, json=data, headers=headers)
    binaryData = response.content
    print(response.text)
    with open('output.mp3', 'wb') as f:
         f.write(binaryData)
    print(f"Audio content size: {len(binaryData)} bytes")
    playAudio()
    return response.content

