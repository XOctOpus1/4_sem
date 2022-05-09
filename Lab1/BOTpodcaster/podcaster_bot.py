import dataclasses
from aiogram import Bot, Dispatcher, executor, types
import pafy
from pydub import AudioSegment
import os

# bot = Bot(token="token")
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("Hey bro!")
    
    
@dp.message_handler(content_types=["text"])
async def send_audio(message: types.Message):
    try:
        pafy_obj = pafy.new(url=message.text)
        await message.answer("Please waiting...")
        
        title = pafy_obj.title
        best_audio = pafy_obj.getbestaudio()
        audio_ext = pafy_obj.getbestaudio().extension
        audio_file_name = f"{title}.{audio_ext}"
        
        # download audio
        best_audio.download()
        
        if audio_ext == "mp3":
            await bot.send_audio(message.chat.id, audio=open(audio_file_name, "rb"))
        else:
            audio = AudioSegment.from_file(audio_file_name)
            audio.export(f"{title}.mp3", format="mp3")
            await bot.send_audio(message.chat.id, audio=open(f"{title}.mp3", "rb"))
            
            os.remove(os.path.abspath(f"{title}.mp3"))
        os.remove(os.path.abspath(audio_file_name))
        
    except Exception as _ex:
        await message.answer("Please check the URL!")
    
    
def main():
    executor.start_polling(dp)
    
    
if __name__ == "__main__":
    main()
