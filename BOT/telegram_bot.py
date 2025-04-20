import os
import telebot
from dotenv import load_dotenv
from final import Translate_video

# Load environment variables
load_dotenv()

# Initialize bot with your token
bot = telebot.TeleBot("7748224908:AAEOhyv51_zcQWwbj3w-CBPqBNj78-3gJ98")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me a video and I'll translate it for you with subtitles.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    try:
        # Send a processing message
        processing_msg = bot.reply_to(message, "Processing your video... This may take a few minutes.")
        
        # Get file info
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Save the video temporarily in videos folder
        input_video = os.path.join('videos', 'temp_video.mp4')
        with open(input_video, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Process the video
        output_video = Translate_video(input_video)
        
        # Send the processed video
        with open(output_video, 'rb') as video:
            bot.send_video(message.chat.id, video)
        # Clean up temporary files
        # os.remove(input_video)
        # os.remove(output_video)
        # os.remove("translated_subtitles.srt")
        
        # Delete the processing message
        bot.delete_message(message.chat.id, processing_msg.message_id)
        
    except Exception as e:
        bot.reply_to(message, f"Sorry, an error occurred: {str(e)}")
        # Clean up any remaining files
        for file in [input_video, output_video, "translated_subtitles.srt"]:
            if os.path.exists(file):
                os.remove(file)

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling() 
    