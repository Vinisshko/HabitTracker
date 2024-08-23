import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.models import async_main


async def main():
    await async_main()
    bot = Bot(token="7423564706:AAEpmqrRipgBIPPSZgbOV-bEcmtV9zwCeNQ")  # Хранится бот
    dp = Dispatcher()  # обработка сообщений(хэндлеры(обновления))
    dp.include_router(router)
    await dp.start_polling(
        bot
    )  # скрипт обращается к тг и спрашивает не пришло ли сообщение
    # посмотреть webhook и как с ними работать (+ ngrock)
    # black [путь до файла]
    # .venv\scripts\activate


if (
    __name__ == "__main__"
):  # будет запускаться если я запустила файл, если импорт то нет
    try:
        print("Bot has been started")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
