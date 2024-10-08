from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
def playAudio(dialouge):
    # Create a BytesIO object to hold the audio in memory
    mp3_fp = BytesIO()

    # Convert text to speech and write it to the memory stream
    tts = gTTS(dialouge[:20], lang='en')
    tts.write_to_fp(mp3_fp)

    # Move the BytesIO pointer to the beginning of the stream
    mp3_fp.seek(0)

    # Load the MP3 audio from the memory stream using pydub
    audio = AudioSegment.from_file(mp3_fp, format="mp3")

    # Play the audio
    play(audio)
