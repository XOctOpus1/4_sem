import os
import random
import sys
import speech_recognition
import pyttsx3
from selenium import webdriver

commands_dict = {
    'commands': {
        'greeting': ['привет', 'приветствую'],
        'create_task': ['добавить задачу', 'создать задачу', 'заметка'],
        'play_music': ['включить музыку', 'дискотека'],
        'restart_pc': ['перезагрузить компьютер'],
        'shutdown_pc': ['выключить компьютер'],
        'cancel_restart_pc': ['отмена перезагрузки'],
        'cancel_shutdown_pc': ['отмена выключения'],
        'open_browser': ['браузер'],
        'exit': ['выйти', 'завершить работу', 'выход']
    }
}


class Denys():
    def __init__(self):
        self.speaker = pyttsx3.init()
        self.speaker.setProperty('voice', 'russian')
        self.speaker.setProperty('rate', 150)
        self.sr = speech_recognition.Recognizer()
        self.sr.pause_threshold = 0.5
        
    def listen_command(self):
        """The function will return the recognized command"""
    
        try:
            with speech_recognition.Microphone() as mic:
                self.sr.adjust_for_ambient_noise(source=mic, duration=0.5)
                audio = self.sr.listen(source=mic)
                query = self.sr.recognize_google(audio_data=audio, language='ru-RU').lower()
                
            return query
        except speech_recognition.UnknownValueError:
            self.speaker.say('Пожалуйста повтори команду')
            self.speaker.runAndWait()
    
    def greeting(self):
        """Greeting function"""
    
        self.speaker.say('Привет друг')
        self.speaker.runAndWait()
        
    def create_task(self):
        """Create a todo task"""
        
        self.speaker.say('Что добавим в список дел?')
        self.speaker.runAndWait()
        
        query = self.listen_command()
            
        with open('todo-list.txt', 'a') as file:
            file.write(f'❗️ {query}\n')

        self.speaker.say(f'Задача {query} добавлена в todo-list!')
        self.speaker.runAndWait()
        
    def play_music(self):
        """Play a random mp3 file"""
        
        files = os.listdir('music')
        random_file = f'music/{random.choice(files)}'
        os.system(f'xdg-open {random_file}')
        
        self.speaker.say(f'Танцуем под {random_file.split("/")[-1]} 🔊🔊🔊')
        self.speaker.runAndWait()
        
    def restart_pc(self):
        os.system('shutdown -r +5')
        
        self.speaker.say('Компьютер будет перезагружен через 5 минут. Для отмены введите shutdown -c')
        self.speaker.runAndWait()
        
    def cancel_restart_pc(self):
        os.system('shutdown -c')
        
        self.speaker.say('Перезагрузка компьютера успешно отменена')
        self.speaker.runAndWait()    
        
    def shutdown_pc(self):
        os.system('shutdown +5')
        
        self.speaker.say('Компьютер будет выключен через 5 минут. Для отмены введите shutdown -c')
        self.speaker.runAndWait()
        
    def cancel_shutdown_pc(self):
        os.system('shutdown -c')
        
        self.speaker.say('Выключение компьютера успешно отменено')
        self.speaker.runAndWait()
        
    def open_browser(self):
        self.speaker.say('Какую страницу вы хотите открыть?')
        self.speaker.runAndWait()
        
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(
            executable_path='driver_path',
            chrome_options=self.options
        )
        self.driver.implicitly_wait(1)
        self.driver.maximize_window()
        
        query = self.listen_command()
        
        if 'google' in query:
            self.speaker.say('Что будем искать?')
            self.speaker.runAndWait()
            
            query = self.listen_command()
            query = query.split()
            
            self.driver.get('https://www.google.com/search?q=' + '+'.join(query))
            self.speaker.say(f'Поиск по {query} успешно запущен')
            self.speaker.runAndWait()
            
            return
            
        elif 'youtube' in query:
            self.speaker.say('Что будем смотреть?')
            self.speaker.runAndWait()
            
            query = self.listen_command()
            query = query.split()
            
            self.driver.get('https://www.youtube.com/results?search_query=' + '+'.join(query))
            self.speaker.say(f'Приятного просмотра!')
            self.speaker.runAndWait()
            
            return
        
        else:
            self.speaker.say('Не понял тебя')
            self.speaker.runAndWait()
            
            return
        
    def exit(self):
        self.speaker.say('See you soon! Goodbye!')
        self.speaker.runAndWait()
        sys.exit()
        
        
def main():
    bot_1 = Denys()
    sr = speech_recognition.Recognizer()
    
    while True:
        try:
            with speech_recognition.Microphone() as mic:
                sr.adjust_for_ambient_noise(source=mic, duration=0.5)
                audio = sr.listen(source=mic)
                query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
                
            for k, v in commands_dict['commands'].items():
                if query in v:
                    execute = getattr(bot_1, k)
                    execute()
        except Exception as _ex:
            print(_ex, 'Команда не распознана')
            sys.exit()
            

if __name__ == '__main__':
    main()
