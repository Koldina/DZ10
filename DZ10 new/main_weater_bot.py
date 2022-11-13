import requests
import datetime
from config import tg_bot_token, open_weather_token
import asyncio
from aiogram import Bot, Dispatcher
import questions, different_types

# Запуск бота
async def main():
    bot = Bot(token=tg_bot_token)
    dp = Dispatcher()

    dp.include_router(questions.router)
    dp.include_router(different_types.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

