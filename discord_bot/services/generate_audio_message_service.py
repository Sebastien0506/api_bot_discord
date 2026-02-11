from gtts import gTTS
import uuid
import os 

AUDIO_DIR = "audio"

os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_audio_message_service(message: str) :
    print("🎧 Génération de audio :" , message)
    filname = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_DIR, filname)

    tts = gTTS(text=message, lang="fr")
    tts.save(filepath)

    return filepath