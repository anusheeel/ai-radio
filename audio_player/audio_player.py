from concurrent.futures import ThreadPoolExecutor
import asyncio
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

# Use a thread pool for non-blocking audio playback
executor = ThreadPoolExecutor(max_workers=2)

def play_audio_sync(dialouge):
    mp3_fp = BytesIO()
    tts = gTTS(dialouge[:500], lang='en')
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    audio = AudioSegment.from_file(mp3_fp, format="mp3")
    play(audio)

async def play_audio(dialouge):
    # Run the blocking play_audio_sync in a separate thread
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, play_audio_sync, dialouge)
