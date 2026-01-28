import telebot
import time
from datetime import datetime

bot = telebot.TeleBot('TOKEN')
user_states = {}

def write_task_to_file(chat_id, task_text, task_time):
    with open('tasks.txt', 'a') as f:
        f.write(f"{chat_id},{task_text},{task_time}\n")

def check_reminders():
    current_time = datetime.now().strftime('%H:%M')
    with open('tasks.txt', 'r') as f:
        tasks = f.readlines()

    remaining_tasks = []
    for line in tasks:
        chat_id, task_text, task_time = line.strip().split(',')
        if task_time == current_time:
            bot.send_message(chat_id, f"Напоминание: {task_text}")
        else:
            remaining_tasks.append(line.strip())

    with open('tasks.txt', 'w') as f:
        for task in remaining_tasks:
            f.write(task + '\n')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Используйте /add для добавления задачи.")

@bot.message_handler(commands=['add'])
def add_task(message):
    user_states[message.chat.id] = {'step': 1}
    bot.send_message(message.chat.id, "Введите текст задачи.")

@bot.message_handler(func=lambda message: message.chat.id in user_states and user_states[message.chat.id]['step'] == 1)
def get_task_text(message):
    user_states[message.chat.id]['text'] = message.text
    user_states[message.chat.id]['step'] = 2
    bot.send_message(message.chat.id, "Введите время в формате 'HH:MM' (24-часовой формат).")

@bot.message_handler(func=lambda message: message.chat.id in user_states and user_states[message.chat.id]['step'] == 2)
def get_task_time(message):
    task_time = message.text
    task_text = user_states[message.chat.id]['text']
    write_task_to_file(message.chat.id, task_text, task_time)
    bot.send_message(message.chat.id, "Задача добавлена!")
    user_states[message.chat.id]['step'] = 0
    something_special(message)

@bot.message_handler(func=lambda message: True)
def something_special(message):
    if message.chat.id in user_states and user_states[message.chat.id]['step'] == 0:
        while True:
            try:
                check_reminders()
                time.sleep(5)
            except Exception as e:
                print(f"Ошибка: {e}")
                time.sleep(5)
bot.polling()