import telebot
import requests

bot = telebot.TeleBot('AAGDq_LCIjDItzQ8CNJiq72gUpSK0OkSSWQ')

# Создаем словарь с возможными командами и стейтами
commands = {
    'start': 'start',
    'help': 'help',
    'weather': 'weather',
    'exchange': 'exchange',
    'hello': 'hello',
}

states = {
    'start': 0,
    'help': 1,
    'weather': 2,
    'exchange': 3,
}

# При старте бота выводим приветственное сообщение
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Укажите команду /help, чтобы узнать, что я могу для вас сделать.")

# Выводим список команд и описание
@bot.message_handler(commands=['help'])
def send_help(message):
    response = "Я могу помочь вам узнать текущую погоду и курсы валют. Вот список доступных команд:\n\n"
    for cmd, desc in commands.items():
        response += "/{} - {}\n".format(cmd, desc)
    bot.reply_to(message, response)

# Обрабатываем запрос на погоду
@bot.message_handler(commands=['weather'])
def get_weather(message):
    bot.send_message(message.chat.id, "Введите название города, чтобы узнать погоду:")

# Обрабатываем введенный город и выводим информацию о погоде
@bot.message_handler(func=lambda message: True, state=states['weather'])
def get_city_weather(message):
    city_name = message.text
    weather_api_key = 'insert_your_weather_api_key_here'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city_name, weather_api_key)
    response = requests.get(url).json()
    if response.get('cod') != 200:
        bot.send_message(message.chat.id, "Не удалось получить информацию о погоде. Попробуйте еще раз.")
    else:
        temp = round(response['main']['temp'] - 273.15)
        description = response['weather'][0]['description'].capitalize()
        bot.send_message(message.chat.id, "Сейчас в {} {}°C, {}\n".format(city_name, temp, description))

# Обрабатываем запрос на курсы валют
@bot.message_handler(commands=['exchange'])
def get_exchange(message):
    bot.send_message(message.chat.id, "Введите валюту, которую нужно перевести (например: USD), а затем валюту, в которую нужно перевести (например: EUR):\n")

# Обрабатываем введенные валюты и выводим информацию о курсе
@bot.message_handler(func=lambda message: True, state=states['exchange'])
def get_exchange_rate(message):
    currencies = message.text.split()
    exchange_api_key = 'insert_your_exchange_api_key_here'
    url = 'https://api.exchangeratesapi.io/latest?base={}&symbols={}'.format(currencies[0], currencies[1])
    response = requests.get(url).json()
    if 'error' in response:
        bot.send_message(message.chat.id, "Не удалось получить информацию о курсе. Попробуйте еще раз.")
    else:
        rate = response['rates'][currencies[1]]
        bot.send_message(message.chat.id, "Курс {} к {} – {}".format(currencies[0], currencies[1], rate))

# Обрабатываем команду /hello
@bot.message_handler(commands=['hello'])
def say_hello(message):
    bot.send_message(message.chat.id, "Привет {0.first_name}! Я бот, который может помочь вам узнать текущую погоду и курсы валют. "
                                      "Введите команду /help, чтобы узнать, что я умею.".format(message.from_user))

if __name__ == '__main__':
    bot.polling(none_stop=True)