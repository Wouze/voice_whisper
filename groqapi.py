
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# filename = os.path.dirname(__file__) + "/audio.m4a"

filename = "input.mp3"

with open(filename, "rb") as file:
    transcription = client.audio.transcriptions.create(
      file=(filename, file.read()),
      model="whisper-large-v3",
      response_format="verbose_json",
      timestamp_granularities=["segment"]
      
    )
    print(transcription)
      