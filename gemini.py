from google import genai
from dotenv import load_dotenv
import os
import ffmpeg

# Load environment variables from a .env file
load_dotenv()
# Retrieve the Google GenAI API key from the environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

# ffmpeg.input('input.mp4').output("input.mp3").run()

myfile = client.files.upload(file='input.mp3')
print('uploaded file')

response = client.models.generate_content(
  # model='gemini-2.0-flash',
  model='gemini-2.5-flash-preview-04-17',
  contents=['Generate a transcript with timestamps in the format: [MM:SS] [text]', myfile]
)

print(response.text)
