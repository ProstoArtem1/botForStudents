import os
import telebot
from currency_converter import CurrencyConverter
from telebot import types
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
currency = CurrencyConverter()

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id, 
        ' Привет! Я бот для конвертации валют.\n **Введите сумму:**', 
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(message, process_sum)

def process_sum(message):
    try:
        amount = float(message.text.strip().replace(',', '.')) 
    except ValueError:
        bot.send_message(message.chat.id, ' Ошибка! Пожалуйста, введите число (сумму):')
        bot.register_next_step_handler(message, process_sum)
        return

    if amount <= 0:
        bot.send_message(message.chat.id, ' Число должно быть больше нуля. Попробуйте ещё раз:')
        bot.register_next_step_handler(message, process_sum)
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('USD / EUR', callback_data=f'convert:USD/EUR:{amount}')
    btn2 = types.InlineKeyboardButton('EUR / USD', callback_data=f'convert:EUR/USD:{amount}')
    btn3 = types.InlineKeyboardButton('USD / GBP', callback_data=f'convert:USD/GBP:{amount}')
    btn4 = types.InlineKeyboardButton(' Другая валюта', callback_data=f'else:{amount}')
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, f' Вы выбрали сумму: *{amount}*.\nВыберите пару валют:', reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    bot.answer_callback_query(call.id)
    
    data_split = call.data.split(':')
    action = data_split[0]
    amount = float(data_split[-1]) 

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    if action == 'convert':
        pair = data_split[1]
        from_val, to_val = pair.split('/')
        try:
            res = currency.convert(amount, from_val, to_val)
            bot.send_message(
                call.message.chat.id, 
                f' **Результат:** {amount} {from_val} = *{round(res, 2)}* {to_val}\n\n Если хотите конвертировать снова, просто введите новую сумму:'
            )
            bot.register_next_step_handler(call.message, process_sum)
        except Exception:
            bot.send_message(call.message.chat.id, ' Произошла ошибка при конвертации. Введите сумму заново:')
            bot.register_next_step_handler(call.message, process_sum)
            
    elif action == 'else':
        bot.send_message(
            call.message.chat.id, 
            ' Введите код валют через косую черту.\nПример: `USD/UAH` или `EUR/PLN`:', 
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(call.message, process_custom_currency, amount)

def process_custom_currency(message, amount):
    try:
        values = message.text.upper().strip().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(
            message.chat.id, 
            f' **Результат:** {amount} {values[0]} = *{round(res, 2)}* {values[1]}\n\n Введите новую сумму для следующего расчёта:'
        )
        bot.register_next_step_handler(message, process_sum)
    except Exception:
        bot.send_message(message.chat.id, ' Неверный формат или валюта не поддерживается. Попробуйте ввести сумму заново:')
        bot.register_next_step_handler(message, process_sum)

if __name__ == '__main__':
    print('bot ready')
    bot.polling(none_stop=True)
