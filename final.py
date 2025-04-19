import os
import re
from TRANSLAtor import translate_to_english_deepl
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
            translated_text = translate_to_english_deepl(text, target_language='EN')
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
                ss_int += 2
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
                vf=f"subtitles={subtitle_file}:force_style='FontSize=24,FontName=Arial,PrimaryColour=&H00FFFFFF,OutlineColour=&H000000FF,BackColour=&H80000000,Outline=2,Shadow=1'",
                codec='copy', 
                acodec='copy'
            )
            .run(overwrite_output=True)
        )
        print(f"Successfully created video with subtitles: {output_file}")
    except Exception as e:
        print(f"Error burning subtitles: {e}")

def main():
    # Get input video file
    input_video = input("Enter the path to the input video file: ")
    
    # Get transcript text
    transcript_text = """
[00:00] (Bird sounds)
[00:06] صوت صفير البلبل
[00:08] هيج قلبي الثمل
[00:10] الماء والزهر معا
[00:12] مع زاري لحظ المقل
[00:14] وأنت يا سيد لي
[00:16] وسيدي ومولى لي
[00:18] فكم فكم تيممني
[00:20] غزيل عقيقلي
[00:21] قطفته من وجنة
[00:24] من لثم ورد الخجل
[00:25] فقال لا لا لا لا لا لا
[00:27] وقد غدا مهرولي
[00:29] والخود قالت لي
[00:30] لا تأثر بذا الرجل
[00:33] فولولت وولولت
[00:35] ولي ولي يا ويللي
[00:37] فقلت لا تولولي
[00:39] وبين اللؤلؤ لي
[00:40] قالت له حين كذا
[00:42] انهض وجد بالنقلي
[00:44] وفتية سقونني
[00:46] قهوة كالعسل لي
[00:48] شممتها بأنافي
[00:50] أزكى من القرنفلي
[00:52] في وسط بستان حلي
[00:54] بالزهر والسرور لي
[00:55] والعود دندن دن دن لي
[00:57] والطبل طب طب طب طب لي
[00:59] طبطب طبطب طبطب
[01:02] طبطب طبطب لي
[01:03] والسقف سق سق سق سق لي
[01:05] والرقص قد طاب لي
[01:06] شوى شوى وشاهشوا
[01:08] على ورق سفرجلي
[01:10] وغرد القمري
[01:12] يصيح ملال في ملال
[01:15] ولو تراني راكبا
[01:17] على حمار اهزل لي
[01:18] يمشي على ثلاثة
[01:20] كمشية العرنجلي
[01:22] والناس ترجم جملي
[01:24] في السوق بالقلقل لي
[01:26] والكل كع كع كع كعي
[01:28] خلفي ومن حويللي
[01:30] لكن مشيت هاربا
[01:32] من خشية العقعقلي
[01:34] إلى لقاء ملك
[01:35] معظم مبجلي
[01:38] يأمر لي بخلعة
[01:40] حمراء كالدم دملي
[01:41] أجر فيها ماشيا
[01:43] مبغددا للذيل لي
[01:45] أنا الأديب الألمعي
[01:47] من حي أرض الموصل
[01:49] نظمت قطعا زخرفت
[01:51] يعجز عنها الأدبلي
[01:52] أقول في مطلعها
[01:54] صوت صفير البلبل
[01:57] (Bird sounds)
"""
    
    # Process transcript
    subtitle_entries = parse_transcript(transcript_text)
    
    # Translate transcript
    print("Translating transcript...")
    translated_entries = translate_transcript(subtitle_entries)
    
    # Create SRT files
    original_srt = "original_subtitles.srt"
    translated_srt = "translated_subtitles.srt"
    
    create_srt_file(subtitle_entries, original_srt)
    create_srt_file(translated_entries, translated_srt)
    
    # Ask user which subtitle file to use
    use_translated = input("Do you want to use translated subtitles? (y/n): ").lower() == 'y'
    subtitle_file = translated_srt if use_translated else original_srt
    
    # Create output file path
    output_video = os.path.splitext(input_video)[0] + "_with_subtitles" + os.path.splitext(input_video)[1]
    
    # Burn subtitles into video
    print(f"Burning subtitles into video...")
    burn_subtitles(input_video, subtitle_file, output_video)

if __name__ == "__main__":
    main()
