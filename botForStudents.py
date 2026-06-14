import os
import telebot
from telebot import types
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

days_map = {
    0: "Понеділок", 1: "Вівторок", 2: "Середа", 
    3: "Четвер", 4: "П'ятниця", 5: "Субота", 6: "Неділя"
}

schedule = {
    "Чисельник": {
        "Понеділок": "1. Географ. (8:15 - 9:00)\n2. Зар. літ (9:10 - 9:55)\n3. Історія (10:05 - 10:50)\n4. - (11:05 - 11:50)\n5. Англ. мова (12:00 - 12:45)\n6. Хімія (12:55 - 13:40)\n7. Технології (13:50 - 14:35)\n8. Фіз-ра (14:40 - 15:25)",
        "Вівторок": "1. - (8:15 - 9:00)\n2. Укр літ (9:10 - 9:55)\n3. Алгебра (10:05 - 10:50)\n4. Фіз-ра (11:05 - 11:50)\n5. Зар. літ (12:00 - 12:45)\n6. Геометрія (12:55 - 13:40)\n7. Укр мова (13:50 - 14:35)\n8. Інформатика (14:40 - 15:25)",
        "Середа": "1. - (8:15 - 9:00)\n2. Фізика (9:10 - 9:55)\n3. Англ. мова (10:05 - 10:50)\n4. - (11:05 - 11:50)\n5. Алгебра (12:00 - 12:45)\n6. Мистецтво (12:55 - 13:40)\n7. Укр мова (13:50 - 14:35)\n8. Геометрія (14:40 - 15:25)",
        "Четвер": "1. ГроС (8:15 - 9:00)\n2. ЗБД (9:10 - 9:55)\n3. Укр літ (10:05 - 10:50)\n4. - (11:05 - 11:50)\n5. Історія (12:00 - 12:45)\n6. Укр мова (12:55 - 13:40)\n7. Біологія (13:50 - 14:35)\n8. Алгебра (14:40 - 15:25)",
        "П'ятниця": "1. Год Спілк. (8:00 - 8:30)\n2. Фіз-ра (8:35 - 9:20)\n3. Хімія (9:30 - 10:15)\n4. - (10:25 - 11:10)\n5. Інформатика (11:25 - 12:10)\n6. Біологія (12:20 - 13:05)\n7. Географія (13:15 - 14:00)\n8. Англ. мова (14:05 - 14:50)\n9. Фізика (14:55 - 15:40)"
    },
    "Знаменник": {
        "Понеділок": "1. Хімія (8:15 - 9:00)\n2. Алгебра (9:10 - 9:55)\n3. Англ. мова (10:05 - 10:50)\n4. Фіз-ра (11:05 - 11:50)\n5. Історія (12:00 - 12:45)\n6. Географія (12:55 - 13:40)\n7. Технології (13:50 - 14:35)",
        "Вівторок": "1. Фізика (8:15 - 9:00)\n2. Англ. мова (9:10 - 9:55)\n3. Укр мова (10:05 - 10:50)\n4. Зар. літ (11:05 - 11:50)\n5. Укр літ (12:00 - 12:45)\n6. Алгебра (12:55 - 13:40)\n7. - (13:50 - 14:35)",
        "Середа": "1. Алгебра (8:15 - 9:00)\n2. Мистецтво (9:10 - 9:55)\n3. Біологія (10:05 - 10:50)\n4. Фізика (11:05 - 11:50)\n5. Укр мова (12:00 - 12:45)\n6. Фіз-ра (12:55 - 13:40)\n7. Англ. мова (13:50 - 14:35)",
        "Четвер": "1. Географія (8:15 - 9:00)\n2. Геометрія (9:10 - 9:55)\n3. Укр літ (10:05 - 10:50)\n4. Історія (11:05 - 11:50)\n5. Фін. Грамотність (12:00 - 12:45)\n6. Біологія (12:55 - 13:40)\n7. Інформатика (13:50 - 14:35)",
        "П'ятниця": "1. Год Спілк. (8:00 - 8:30)\n2. Укр мова (8:35 - 9:20)\n3. Хімія (9:30 - 10:15)\n4. Біологія (10:25 - 11:10)\n5. Інформатика (11:25 - 12:10)\n6. Геометрія (12:20 - 13:05)\n7. - (13:15 - 14:00)"
    }
}

user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🔼 Чисельник")
    btn2 = types.KeyboardButton("🔽 Знаменник")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Привіт! Який зараз тиждень?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["🔼 Чисельник", "🔽 Знаменник"])
def select_week(message):
    clean_week = message.text.replace("🔼 ", "").replace("🔽 ", "")
    user_states[message.chat.id] = clean_week
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton(" Розклад на сьогодні"))
    
    markup.add(
        types.KeyboardButton("Понеділок"), types.KeyboardButton("Вівторок"),
        types.KeyboardButton("Середа"), types.KeyboardButton("Четвер"),
        types.KeyboardButton("П'ятниця")
    )
    markup.add(types.KeyboardButton("⬅️ Назад"))
    
    bot.send_message(message.chat.id, f" Вибрано: *{clean_week}*.\nОбери потрібний день:", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == "⬅️ Назад")
def go_back(message):
    start(message)

@bot.message_handler(func=lambda message: message.text == " Розклад на сьогодні")
def send_today_schedule(message):
    week = user_states.get(message.chat.id)
    if not week:
        bot.send_message(message.chat.id, "⚠️ Будь ласка, спочатку вибери тип тижня за допомогою команди /start")
        return

    today_index = datetime.now().weekday()
    day_name = days_map[today_index]

    if day_name in ["Субота", "Неділя"]:
        bot.send_message(message.chat.id, f" Сьогодні *{day_name}*, уроків немає. Відпочивай на повну! 😎", parse_mode='Markdown')
    else:
        text = schedule[week][day_name]
        bot.send_message(message.chat.id, f" **Розклад на сьогодні** ({day_name}, {week}):\n\n{text}", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text in ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця"])
def send_schedule(message):
    week = user_states.get(message.chat.id)
    if not week:
        bot.send_message(message.chat.id, "⚠️ Спочатку вибери тип тижня. Напиши /start")
        return
        
    day = message.text
    text = schedule[week][day]
    bot.send_message(message.chat.id, f" **Розклад на {day}** ({week}):\n\n{text}", parse_mode='Markdown')

if __name__ == '__main__':
    print('bot ready')
    bot.polling(none_stop=True)
