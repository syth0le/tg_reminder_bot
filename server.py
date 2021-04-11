import logging
import os

# import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv


from middleware import AccessMiddleware
import reminders
import exceptions

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
ACCESS_ID = os.getenv("ACCESS_ID")

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
        "очистка от выполненных: /clean"
        "удаление: /del идентификатор")


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
    """Clean db and delete reminders which were done later"""
    answer_message = reminders.delete_done_reminders()
    await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Delete only 1 reminder by identificator"""
    try:
        row_id = int(message.text[4:])
    except ValueError:
        await message.answer("Дядь, ну айдишник то передай а...")
        return
    answer_message = reminders.delete_reminder(row_id)
    await message.answer(answer_message)


@dp.message_handler()
async def add_reminder_route(message: types.Message):
    """Add new reminder or send message "NO ROUTE" information"""
    # await message.answer("такого пути нет")

    try:
        reminder = reminders.add_reminder(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    # answer_message = (
    #     f"Added reminder {reminder.name}.\n\n"
    #     f"{reminder.get_all()}")
    await message.answer(reminder)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
