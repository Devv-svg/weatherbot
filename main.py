import telebot
import requests

API_b = ''
bot = telebot.TeleBot(API_b)
API = ''


@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id, '👨‍💻 Яку допомогу ви потребуєте?'
                                          '\n\n📍 Як потрібно ввести інформацію про місто - /probleminput'
                                          '\n🪫 Проблема з ботом - /problem'
                                          '\n\n========================================================'
                                          '\n🌍 Виберіть проблему та натисніть на синє поле!')


@bot.message_handler(commands=['problem'])
def error(message):
    bot.send_message(message.chat.id, '👀 Зверніться до тех.адміна! @невідомо')


@bot.message_handler(commands=['probleminput'])
def error(message):
    bot.send_message(message.chat.id, '💻 Приклад надання інформації про місто!: {Ваше місто}')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'🌴 Привіт, {message.from_user.first_name}!\n\n🌍 Мене звати Forecaster. Я допомагаю дізнатися, яка погода у світі!\n\nЩоб перевірити погоду, напиши своє місто нижче.')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    try:
        city = message.text.strip().lower()
        weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
        data = weather.json()  # Используем метод .json() напрямую для получения данных
        if weather.status_code == 200:  # Проверяем статус ответа
            country = data.get("sys", {}).get("country", "Невідома країна")
            temp = data["main"]["temp"]
            temp_min = data["main"]["temp_min"]
            temp_max = data["main"]["temp_max"]

            bot.reply_to(message, f'📫 Місто: {city.capitalize()}'
                                  f'\n🌍 Країна: {country}'
                                  f'\n🌴 Температура зараз: {temp}°C'
                                  f"\n❄️ Найменша температура: {temp_min}°C \n☀️ Найбільша: {temp_max}°C")
        else:
            bot.reply_to(message, f"‼️ Не вдалося знайти місто '{city}'.👀 Перевірте правильність назви і спробуйте ще раз.")
    except KeyError:
        bot.reply_to(message, '🚨 Не вдалося отримати інформацію про погоду. Спробуйте ще раз пізніше.')
    except Exception as e:
        bot.reply_to(message, f'🚧 Виникла помилка: {str(e)}. Зверніться до тех. підтримки.')


bot.polling(none_stop=True)
