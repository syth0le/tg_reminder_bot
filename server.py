import logging
# import os

# import aiohttp
from aiogram import Bot, Dispatcher, executor, types


from middleware import AccessMiddleware
import reminders

API_TOKEN = '1710520708:AAFA2N96qphf4sGCUIzOxzblk4GYNCfNVQI'
ACCESS_ID = '276209120'
# API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
# ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(middleware=AccessMiddleware(ACCESS_ID))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(
        "Reminder bot\n\n"
        "Добавить короткое напоминание: тип название время\n"
        "список временных: /temp\n"
        "список постоянных: /permanent\n"
        "список полный: /all\n"
        "удаление: /del")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


@dp.message_handler(commands=['temp'])
async def temporary_reminders(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    answer_message = reminders.get_temporary_reminders()
    await message.answer(answer_message)


@dp.message_handler(commands=['permanent'])
async def permanent_reminders(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    answer_message = reminders.get_permanent_reminders()
    await message.answer(answer_message)


@dp.message_handler(commands=['all'])
async def all_reminders(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    answer_message = reminders.get_all_reminders()
    await message.answer(answer_message)


@dp.message_handler(commands=['clean'])
async def delete_done_reminders(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    answer_message = reminders.delete_done_reminders()
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
