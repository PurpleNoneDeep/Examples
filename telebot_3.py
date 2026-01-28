import telebot
from telebot import types

# Вставьте ваш токен
API_TOKEN = 'TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# Словарь для изучения языка
words = {
    "apple": "яблоко",
    "banana": "банан",
    "orange": "апельсин",
    "grape": "виноград",
    "strawberry": "клубника"
}


print(words["1"])
current_word_index = 0
score = 0
word_list = list(words.keys())


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Напишите /learn, чтобы начать изучение слов.")


@bot.message_handler(commands=['learn'])
def send_word(message):
    global current_word_index
    global score
    current_word_index = 0
    score = 0
    send_next_word(message)


def send_next_word(message):
    global current_word_index
    global score
    if current_word_index < len(word_list):
        english_word = word_list[current_word_index]
        bot.send_message(message.chat.id, f"Как переводится слово '{english_word}'?")
    else:
        bot.send_message(message.chat.id, f"Вы прошли все слова и набрали {score} баллов!")
        if score < 2:
            bot.send_message(message.chat.id, "Это новые слова, в следующий раз обязательно будет лучше! Нажмите /learn, чтобы повторить попытку.")
        elif score <= 4:
            bot.send_message(message.chat.id,
                             "Неплохой результат! Нажмите /learn, чтобы повторить попытку.")
        else:
            bot.send_message(message.chat.id,
                             "Отлично! Эти слова выучены!")
        offer_to_save(message)


def offer_to_save(message):
    markup = types.InlineKeyboardMarkup()
    save_button = types.InlineKeyboardButton("Сохранить слова и счет", callback_data="save_scores")
    markup.add(save_button)
    bot.send_message(message.chat.id, "Хотите сохранить свои слова и счет?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "save_scores")
def save_scores(call):
    global score
    with open('scores.txt', 'w', encoding='utf-8') as f:
        for word in word_list:
            f.write(f"{word}: {words[word]}\n")
        f.write(f"Счет: {score}\n")

    bot.answer_callback_query(call.id, "Ваши слова и счет сохранены в файл scores.txt")

@bot.message_handler(func=lambda m: True)
def check_answer(m):
    global current_word_index
    global score
    english_word = word_list[current_word_index]

    if m.text.lower() == words[english_word]:
        bot.reply_to(m, "Правильно! Молодец!")
        score += 1
        current_word_index += 1
        send_next_word(m)
    else:
        bot.reply_to(m, f"Неправильно. Правильный ответ: {words[english_word]}.")
        current_word_index += 1
        send_next_word(m)



    # Запускаем бота
bot.polling()