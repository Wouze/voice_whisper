from google import genai
from dotenv import load_dotenv
import os
# Load environment variables from a .env file
load_dotenv()
# Retrieve the Google GenAI API key from the environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

myfile = client.files.upload(file='videoplayback.mp3')

response = client.models.generate_content(
  model='gemini-2.0-flash',
  contents=['Generate a transcript of the speech', myfile]
)

print(response.text)
