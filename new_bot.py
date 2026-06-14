import os
import telebot
import sqlite3
from telebot import types
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
name = None

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('melsi.db')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), pass VARCHAR(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Hello! Enter your name please: ')
    bot.register_next_step_handler(message, user_name)
    

def user_name(message):
    global name
    name = message.text.strip()

    bot.send_message(message.chat.id, 'Enter password: ')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('melsi.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES (?, ?)", (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('list users', callback_data='users'))
    bot.send_message(message.chat.id, 'The users has been registered.', reply_markup=markup)
    #bot.register_next_step_handler(message, user_pass)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('melsi.db')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Name: {el[1]}, password: {el[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


print('hello')
bot.polling(none_stop=True)

