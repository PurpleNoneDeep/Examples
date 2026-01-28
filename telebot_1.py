import telebot
from telebot import types
bot = telebot.TeleBot('TOKEN')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Help")
    button2 = types.KeyboardButton("Other")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Выберите тип:", reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Задать вопрос")
    btn2 = types.KeyboardButton("Вернуться к началу")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Сейчас бот умеет это:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message)
    if message.text == "1":
        bot.reply_to(message, "1")
    elif message.text == "2":
        bot.send_message(message.chat.id, text="2")
    elif message.text == "игра":
        bot.send_dice(message.chat.id, emoji='🎲')
    elif message.text == "Help":
        bot.send_message(message.chat.id, text="Чем вам помочь?")
    else:
        with open("alienYellow_walk2.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo)

bot.infinity_polling()