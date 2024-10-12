from concurrent.futures import ThreadPoolExecutor
import asyncio
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

# Use a thread pool for non-blocking audio playback
executor = ThreadPoolExecutor(max_workers=2)

async def play_audio_sync(dialogue):
    """ Synchronously play audio from the given dialogue using gTTS. """
    try:
        print(f"Converting dialogue to audio: {dialogue}")
        mp3_fp = BytesIO()
        tts = gTTS(dialogue[:500], lang='en')
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio = AudioSegment.from_file(mp3_fp, format="mp3")
        play(audio)
        print("Audio finished playing.")
    except Exception as e:
        print(f"Error playing audio: {e}")

async def play_audio(dialogue):
    """ Asynchronously play audio using a thread executor. """
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, play_audio_sync, dialogue)
