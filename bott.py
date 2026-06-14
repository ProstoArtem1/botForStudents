import telebot
import requests

TOKEN = '8634395770:AAFowdr6d9Gq487AW9-tyYQtjzSkt9oY4u0'
bot = telebot.TeleBot(TOKEN)
API_KEY = 'd5ea6e183473f6fbbc6bc8c0e19254b0'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 
        "🌍 **Привет! Я погодный бот.**\n\nОтправь мне название города на любом языке (например: *London* или *Киев*).",
        parse_mode='Markdown'
    )

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip()
    
    # 1. Заворачиваем сетевой запрос в try/except на случай обрыва интернета
    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru'
        res = requests.get(url, timeout=5) # Добавили таймаут, чтобы бот не зависал вечно
    except requests.exceptions.RequestException:
        bot.reply_to(message, "⚠️ Ошибка подключения к серверу погоды. Попробуйте позже.")
        return

    if res.status_code == 200:
        data = res.json() 
        
        # Вытаскиваем расширенные данные (клиенты любят подробности)
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        weather_desc = data["weather"][0]["description"]
        
        # Получаем иконку погоды от самого сервиса OpenWeather
        icon_code = data["weather"][0]["icon"]
        icon_url = f"https://openweathermap.org{icon_code}@2x.png"

        # Формируем красивый текст с эмодзи
        weather_report = (
            f"🏙️ **Погода в городе {city.title()}:**\n\n"
            f"🌡️ Температура: *{round(temp, 1)}°C*\n"
            f"🤔 Ощущается как: *{round(feels_like, 1)}°C*\n"
            f"☁️ На улице: _{weather_desc.capitalize()}_\n"
            f"💧 Влажность: *{humidity}%*\n"
            f"💨 Ветер: *{wind_speed} м/с*"
        )

        # Отправляем красивую карточку: иконка погоды + наш текст
        try:
            bot.send_photo(message.chat.id, icon_url, caption=weather_report, parse_mode='Markdown')
        except Exception:
            # Если ссылка на фото не сработала, просто отправляем текст
            bot.send_message(message.chat.id, weather_report, parse_mode='Markdown')
            
    elif res.status_code == 404:
        bot.reply_to(message, "❌ **Город не найден.** Проверьте правильность написания.")
    else:
        bot.reply_to(message, "⚠️ Произошла ошибка на сервере погоды. Попробуйте другой город.")

if __name__ == '__main__':
    print("Погодный бот успешно запущен!")
    bot.polling(none_stop=True)
