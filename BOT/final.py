import os
import re
from TRANSLAtor import translate_to_english_deepl
from gemini import generate_transcript
import ffmpeg

def parse_transcript(transcript_text):
    """Parse the transcript with timestamps into a list of subtitle entries."""
    pattern = r'\[(\d+:\d+)\] (.*?)(?=\[\d+:\d+\]|$)'
    matches = re.findall(pattern, transcript_text, re.DOTALL)
    
    subtitle_entries = []
    for timestamp, text in matches:
        if text.strip():  # Skip empty lines
            subtitle_entries.append((timestamp, text.strip()))
    
    return subtitle_entries

def translate_transcript(subtitle_entries):
    """Translate each line of the subtitle from Arabic to English."""
    translated_entries = []
    
    for timestamp, text in subtitle_entries:
        # Skip translation for sound effects in parentheses
        if '(' in text and ')' in text:
            translated_text = text
        else:
            translated_text = translate_to_english_deepl(text)
            if translated_text is None:  # If translation fails, keep original
                translated_text = text
        
        translated_entries.append((timestamp, translated_text))
    
    return translated_entries

def create_srt_file(subtitle_entries, output_file):
    """Create an SRT subtitle file from the entries."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, (timestamp, text) in enumerate(subtitle_entries, 1):
            # Convert MM:SS format to SRT format (HH:MM:SS,mmm --> HH:MM:SS,mmm)
            parts = timestamp.split(':')
            if len(parts) == 2:
                mm, ss = parts
                start_time = f"00:{mm}:{ss},000"
                
                # Calculate end time (add 2 seconds)
                mm_int, ss_int = int(mm), int(ss)
                ss_int += 3
                if ss_int >= 60:
                    mm_int += 1
                    ss_int -= 60
                end_time = f"00:{mm_int:02d}:{ss_int:02d},000"
                
                # Write SRT entry
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")

def burn_subtitles(video_file, subtitle_file, output_file):
    """Burn subtitles into the video using ffmpeg."""
    try:
        (
            ffmpeg
            .input(video_file)
            .output(
                output_file,
                vf=f"subtitles={subtitle_file}:force_style='FontSize=24,FontName=Ubuntu Arabic,PrimaryColour=&H00FFFFFF,OutlineColour=&H000000FF,BackColour=&H80000000,Outline=1,Shadow=1'"
            )
            .run(overwrite_output=True)
        )
        print(f"Successfully created video with subtitles: {output_file}")
    except Exception as e:
        print(f"Error burning subtitles: {e}")

def Translate_video(input_video):
    
    # Get transcript text
    transcript_text = generate_transcript(input_video)
    
    # Process transcript
    subtitle_entries = parse_transcript(transcript_text)
    
    # Translate transcript
    print("Translating transcript...")
    translated_entries = translate_transcript(subtitle_entries)
    
    # Create SRT file for translated subtitles
    translated_srt = "translated_subtitles.srt"
    create_srt_file(translated_entries, translated_srt)
    
    # Create output file path
    output_video = os.path.splitext(input_video)[0] + "_with_subtitles" + os.path.splitext(input_video)[1]
    
    # Burn subtitles into video
    print(f"Burning translated subtitles into video...")
    burn_subtitles(input_video, translated_srt, output_video)

    return output_video
