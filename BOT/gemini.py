from google import genai
from dotenv import load_dotenv
import os
import ffmpeg

def generate_transcript(input_video):
    """
    Generate a transcript with timestamps from a video file using Gemini API.
    
    Args:
        input_video (str): Path to input video file
        
    Returns:
        str: Transcript text with timestamps in [MM:SS] format
    """
    # Load environment variables from a .env file
    load_dotenv()
    # Retrieve the Google GenAI API key from the environment variables 
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Convert video to audio
    audio_file = "videos/temp_audio.mp3"
    ffmpeg.input(input_video).output(audio_file).run()

    # Upload audio file to Gemini
    myfile = client.files.upload(file=audio_file)

    # Generate transcript
    response = client.models.generate_content(
        model='gemini-2.5-flash-preview-04-17',
        contents=['Generate a transcript with timestamps in the format: [MM:SS] [text]', myfile]
    )

    # Clean up temporary audio file
    os.remove(audio_file)

    return response.text
