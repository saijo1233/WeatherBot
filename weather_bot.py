import requests
from pprint import pprint
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
token = "708d835ee990d21933313dc478326808"
token_telegram = '5995380969:AAGUxAj5XJsAaQtS0RJVXYQvgaBXFUnIKys'

bot = Bot(token = token_telegram)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Приветствую, напиши свой город!')

@dp.message_handler()
async def get_weather(message: types.Message):
    smiles_weather = {
        'Clear': "Ясная погода \U00002600",
        'Clouds': "Облачно \U00002601",
        'Rain': "Дождь \U00002614",
        'Drizzle': "Моросистый дождь \U00002614",
        'Thunderstorm': "Гроза \U000026A1",
        'Snow': "Снег \U0001F328",
        'Mist': "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={token}&units=metric'
        )
        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']

        weather_discription = data['weather'][0]['main']
        if weather_discription in smiles_weather:
            wd = smiles_weather[weather_discription]
        else:
            print ('Неизвестная погода')

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        dawn_time = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        await message.reply(f'{datetime.datetime.now().strftime("%Y-%m-%d %H-%M")}\n'
              '\n'
              f'Погода в городе: {city}\nТемпература: {cur_weather}°C - {wd},\n'
              f'Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\n'
              f'Скорость ветра: {wind}м/с\nРассвет: {dawn_time}\n'
              '\n'
              'Хорошего дня!'
              )
    except:
        await message.reply('\U00002620 Проверьте название города')


def main():
    city = input('Введите ваш город - ')
    get_weather(city, token)

if __name__ == '__main__':
    executor.start_polling(dp)
