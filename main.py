import telebot
import os
from datetime import datetime
from random import choice
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from threading import Thread
from kivy.uix.textinput import TextInput

bot = telebot.TeleBot("Your API")

class BotApp(App):
    def build(self):
        self.command = "None"
        self.window = BoxLayout(orientation="vertical")
        
        self.label = Label(text="message")
        self.window.add_widget(self.label)
        
        self.text = TextInput(size_hint=(1, 0.15), font_size="30sp", multiline=False, on_text_validate=self.enter)
        
        self.window.add_widget(Button(text="Рассылка", size_hint=(1, 0.3), on_press=self.shares))
        
        self.window.add_widget(Button(text="Вопрос", size_hint=(1, 0.3)))
        
        self.window.add_widget(Button(text="Регистрации", size_hint=(1, 0.3), on_press=self.reg))
        
        self.window.add_widget(Button(text="Старт", size_hint=(1, 0.3), on_press=self.start_bot, color=(0, 0, 1, 1)))
        
        return self.window
        
        
    
    def start_bot(self, start):
        Thread(target=bot.polling).start()
    
    
    def shares(self, button):
        if self.command == "None":
            self.window.add_widget(self.text)
        self.command = "shares"
        self.label.text = "Рассылка"
    
    
    def enter(self, text):
        if self.command == "shares":
            file = open("users.app", "r").read()
            numbers = file.split("\n")
            for number in numbers:
                bot.send_message(number, self.text.text)
    
    
    def reg(self, button):
        if os.path.exists("users.app"):
            self.label.text = open("users.app", "r").read()
        else:
            self.label.text = "None"
        self.window.remove_widget(self.text)
        self.command = "None"


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, str("Привет, " + message.from_user.first_name + "!"))
    open("users.app", "a").write(f"{message.chat.id}\n")

    
@bot.message_handler(content_types=["photo"])
def photo(message):
    bot.reply_to(message, choice(["О прикольное фото 👍", "О крутое фото 😎", "Прикольная Картинка"]))

@bot.message_handler(func=lambda message: True)
def reply_to(message):
    now = datetime.now()
    answer = ""
    message_text = message.text
    names = ["ДЕН", "ПОГОД", "ДЕЛ"]
    message_text = message_text.upper()
    message_text = message_text.split(" ")
    for word in names:
        for text in message_text:
            if text > word:
                text = text[:len(word)-len(text)]
                if text == word:
                    if word == "ДЕН":
                        answer = now.strftime("Сегодня %d.%m.%Y")
                    if word == "ДЕЛ":
                        answer = "Хорошо\n\nА у вас как?"
                    elif word == "ПОГОД":
                        weather = open("Weather/sunny.png", "rb")
                        bot.send_photo(message.chat.id, weather, """Сегодня солнечно
+26C""")
                    else:
                        #answer = "Я вас не понимаю 😭!"
                        pass
    if len(answer) >= 1:
        bot.reply_to(message, answer)

BotApp().run()
