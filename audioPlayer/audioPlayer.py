# Optional: Play the audio using pydub or any other audio library
from pydub import AudioSegment
from pydub.playback import play

def playAudio():
    audio = AudioSegment.from_mp3("anusheel.wav")
    play(audio)

