from aiogram import Router, types, Dispatcher
from aiogram.dispatcher.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import html
from aiogram.dispatcher.filters import CommandObject
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from for_questions import get_yes_no_kb
from config import open_weather_token
import requests
import main

router = Router()  # [1]


@router.message(Text(text="Привет", text_ignore_case=True))
async def answer_no(message: Message):
    await message.answer(
        "Мы рады видеть вас, для начала общения введите /start",
        reply_markup=ReplyKeyboardRemove()
    )
@router.message(Text(text="Пока", text_ignore_case=True))
async def answer_no(message: Message):
    await message.answer(
        "Спасибо, что воспользовались ботом!",
        reply_markup=ReplyKeyboardRemove()
    )
@router.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Здравствуйте! Примите, пожалуйста, участие в опросе, посвященном исследованию оценки удовлетворенности покупкой. Ваши ответы и пожелания помогут исправить имеющиеся ошибки и улучшить качество товаров! Введите /name")
@router.message(Text(text="Режим работы", text_ignore_case=True))
async def answer_no(message: Message):
    await message.answer(
        "Ежедневно с 9:00 до 20:00",
        reply_markup=ReplyKeyboardRemove()
    )

#@router.message(Text(text="Погода", text_ignore_case=True))
@router.message(commands=["weather"])
async def cmd_weather(message: types.Message):
    await message.reply("Введите город и я вам покажу погоду")

@router.message()
async def get_weather(message: types.Message):
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
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric&lang=ru")  # 4321a3d417b53045aa1b6617c529c910
        data = response.json()

        city = data['name']
        temp = data['main']['temp']

        weather_description = data['weather'][0]['main']  # смайлы на погоду
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Не пойму что за погода, посмотри сам в окно'

        weather = data['weather'][0]['description']
        temp_feels = data['main']['feels_like']
        wind = data['wind']['speed']
        await message.reply(
            f'погода в городе {city}:\n{weather}, температура воздуха - {temp} {wd}, ощущается как {temp_feels}, скорость ветра {wind}')

    except:
        await message.reply("Проверьте название города")




@router.message(Text(text="Адрес", text_ignore_case=True))
async def answer_no(message: Message):
    await message.answer(
        "город Москва улица дом",
        reply_markup=ReplyKeyboardRemove()
    )
@router.message(commands=["name"])
async def cmd_name(message: types.Message, command: CommandObject):
    if command.args:
        await message.answer(f"Привет, {html.bold(html.quote(command.args))}, введите /next", parse_mode="HTML")
    else:
        await message.answer("Пожалуйста, укажи своё имя после команды /name!")


@router.message(commands=["next"])  # [2]
async def cmd_start(message: Message):
    await message.answer(
        "Вы делали покупки в нашем интернет магазине?",
        reply_markup=get_yes_no_kb()
    )

#ветка нет
@router.message(Text(text="Нет"))
async def cmd_opros_net(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Режим работы"),
            types.KeyboardButton(text="Адрес")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Оцените работу интернет магазина"
    )
    await message.answer("Будем рады видить Вас в МАГАЗИНЕ", reply_markup=keyboard)

#ветка да
@router.message(lambda message: message.text == "Да")
async def reply_da(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 10):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(3)
    await message.answer(
        "Оцените, пожалуйста, купленный Вами товар по 9-балльной шкале, где 1 соответствует очень низкому качеству, 9 – максимально высокому качеству:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

@router.message(Text(text=["1", "2", "3", "4", "5", "6", "7", "8", "9"]))
async def cmd_size(message: types.Message):
    kb1 = [
            [types.KeyboardButton(text="Цена должна быть выше за товар такого качества")],
            [types.KeyboardButton(text="Цена соответствует качеству")],
            [types.KeyboardButton(text="Цена должна быть ниже за товар такого качества")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb1,
        resize_keyboard=True,
        input_field_placeholder="Оцените работу интернет магазина"
    )
    await message.answer("Если говорить о сочетании цены и качества, то как Вы оцените купленный Вами продукт?", reply_markup=keyboard)

@router.message(lambda message: message.text == "Цена должна быть выше за товар такого качества")
async def with_puree(message: types.Message):
    await message.reply("Спасибо, за высокую оценку")
@router.message(lambda message: message.text == "Цена соответствует качеству")
async def with_pur(message: types.Message):
    await message.reply("Спасибо, мы рады за ваше доверие")
@router.message(lambda message: message.text =="Цена должна быть ниже за товар такого качества")
async def with_pure(message: types.Message):
    await message.reply("Спасибо, будем стараться")

