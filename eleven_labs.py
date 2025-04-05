from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("ELEVEN_LABS")

from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key=key,
)

with open("videoplayback.mp3", "rb") as audio_file:

    resp = client.speech_to_text.convert(
        model_id="scribe_v1",
        file=audio_file
    )
    
    print(resp)
