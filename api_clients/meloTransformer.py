from MeloTTS.melo.api import TTS

from MeloTTS.melo.api import TTS

def speaker1(dialouge):   
    speed = 1.0
    device = 'auto'  # Automatically use GPU if available

    # Text to synthesize
    text = dialouge

    # Initialize the TTS model
    model = TTS(language='EN', device=device)
    
    # Check available speaker IDs
    speaker_ids = model.hps.data.spk2id
    print("Available speaker IDs:", speaker_ids)

    # Check if 'EN-INDIA' exists in speaker_ids
    if 'EN_INDIA' in speaker_ids:
        speaker_id = speaker_ids['EN_INDIA']
    else:
        print("EN-INDIA not available. Using a default speaker.")
        speaker_id = list(speaker_ids.values())[0]  # Use the first available speaker as default

    # Generate audio
    output_path = 'anusheel.wav'
    model.tts_to_file(text, speaker_id, output_path, speed=speed)
