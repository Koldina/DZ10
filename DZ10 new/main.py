# рабочий файл - создание файла работы с погодой

import requests
import datetime
from pprint import pprint
from config import open_weather_token

import requests
#name = input('Введите название города: ')
def get_weather(city, open_weather_token):

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облочно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снес \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru") #4321a3d417b53045aa1b6617c529c910
        data = response.json()
        #pprint(data)

        city = data['name']
        temp = data['main']['temp']

        weather_description = data['weather'][0]['main'] #смайлы на погоду
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Не пойму что за погода, посмотри сам в окно'

        weather = data['weather'][0]['description']
        temp_feels = data['main']['feels_like']
        wind = data['wind']['speed']
        print(f'погода в городе {city}:\n{weather}, температура воздуха - {temp} {wd}, ощущается как {temp_feels}, скорость ветра {wind}')

    except Exception as ex:
        print(ex)
        print("Проверьте название города")

def main():
    city = input('Введите название города: ')
    get_weather(city, open_weather_token)
if __name__ == '__main__':
    main()

