import pafy
from pydub import AudioSegment
import os


def get_audio(url):
    try:
        pafy_obj = pafy.new(url=url)
    except Exception as _ex:
        return "Please check the URL!"
    
    author = pafy_obj.author
    title = pafy_obj.title
    # print(author, title)
    
    # for audio_stream in pafy_obj.audiostreams:
    #     print(audio_stream)

    best_audio = pafy_obj.getbestaudio()
    audio_ext = pafy_obj.getbestaudio().extension
    # print(best_audio, audio_ext)
    audio_file_name = f"{title}.{audio_ext}"
    
    # download audio
    best_audio.download()
    
    if audio_ext == "mp3":
        return f"{audio_file_name} downloaded successfully!"
    else:
        audio = AudioSegment.from_file(audio_file_name)
        audio.export(f"{title}.mp3", format="mp3")
        os.remove(os.path.abspath(audio_file_name))
        return f"{title}.mp3 downloaded successfully!"


def main():
    # print(get_audio(url="https://www.youtube.com/watch?v=ozSPlNDar3A"))
    url = input("Please enter a URL: ")
    # https://www.youtube.com/watch?v=_Yhyp-_hX2s
    print(get_audio(url=url))
    
    
if __name__ == "__main__":
    main()
