import logging
import os

# import aiohttp
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from dotenv import load_dotenv
import aioschedule
import asyncio
import datetime

from middleware import AccessMiddleware
import reminders
import exceptions
import db
import buttons as btn

load_dotenv(override=True)

API_TOKEN = os.getenv("API_TOKEN")
ACCESS_ID = os.getenv("ACCESS_ID")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(middleware=AccessMiddleware(ACCESS_ID))


@dp.callback_query_handler(lambda c: c.data == 'btn_temp')
async def process_callback_btn_temp(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    try:
        reminder = reminders.add_reminder('temp.test.12:00')
    except exceptions.NotCorrectMessage as e:
        await bot.send_message(callback_query.from_user.id, str(e))
        return
    await bot.send_message(callback_query.from_user.id, reminder)


@dp.callback_query_handler(lambda c: c.data == 'btn_perm')
async def process_callback_btn_perm(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    try:
        reminder = reminders.add_reminder('perm.test.12:00')
    except exceptions.NotCorrectMessage as e:
        await bot.send_message(callback_query.from_user.id, str(e))
        return
    await bot.send_message(callback_query.from_user.id, reminder)


@dp.message_handler(lambda message: message.text.startswith('Create'))
async def process_command_1(message: types.Message):
    await message.answer("Choose type of reminder:", reply_markup=btn.inline_kb1)
    await message.delete()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(
        "Reminder bot\n\n"
        "Добавить короткое напоминание: тип.название.ремя\n"
        "список полный: /all\n"
        "список временных: /temp\n"
        "список постоянных: /perm\n"
        "удаление напоминания: /del[rem_id]\n"
        "выполнено напоминание: /done[rem_id]\n"
        "очистка от выполненных: /clean",
        reply_markup=btn.mainMenu)


@dp.message_handler(commands=['temp'])
async def temporary_reminders(message: types.Message):
    """doc"""
    answer_message = reminders.get_temporary_reminders()
    await message.answer(answer_message)


@dp.message_handler(commands=['perm'])
async def permanent_reminders(message: types.Message):
    """doc"""
    answer_message = reminders.get_permanent_reminders()
    await message.answer(answer_message)


@dp.message_handler(commands=['all'])
async def all_reminders(message: types.Message):
    """doc"""
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


@dp.message_handler(lambda message: message.text.startswith('/done'))
async def add_task_to_done(message: types.Message):
    """Delete only 1 reminder by identificator"""
    try:
        row_id = int(message.text[5:])
    except ValueError:
        await message.answer("Дядь, ну айдишник то передай а...")
        return
    answer_message = reminders.done_reminder(row_id)
    await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('Show reminders'))
async def start(message: types.Message):
    await message.delete()
    await message.answer(message.text, reply_markup=btn.remindersMenu)


@dp.message_handler(lambda message: message.text.startswith('All'))
async def start(message: types.Message):
    await message.delete()
    await message.answer(reminders.get_all_reminders(), reply_markup=btn.anyRemindersMenu)


@dp.message_handler(lambda message: message.text.startswith('Permanent'))
async def start(message: types.Message):
    await message.delete()
    await message.answer(reminders.get_permanent_reminders(), reply_markup=btn.anyRemindersMenu)


@dp.message_handler(lambda message: message.text.startswith('Temporary'))
async def start(message: types.Message):
    await message.delete()
    await message.answer(reminders.get_temporary_reminders(), reply_markup=btn.anyRemindersMenu)


@dp.message_handler(lambda message: message.text.startswith('Clean'))
async def start(message: types.Message):
    await message.delete()
    await message.answer(reminders.delete_done_reminders(), reply_markup=btn.mainMenu)


@dp.message_handler(lambda message: message.text.startswith('Back'))
async def start(message: types.Message):
    await message.delete()
    await message.answer(message.text, reply_markup=btn.mainMenu,
                         allow_sending_without_reply=True)
    # else:
    #     reminder = reminders.add_reminder(message.text)
    #     await message.answer(reminder)


@dp.message_handler()
async def add_reminder_route(message: types.Message):
    """Add new reminder or send message "NO ROUTE" information"""

    try:
        reminder = reminders.add_reminder(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    await message.answer(reminder)


async def job():
    local_time = str(datetime.datetime.now())[:-9] + "00"
    reminders = db.find_by_date('reminder', local_time)

    if reminders:
        print("notification", local_time)

        last_reminders_rows = [
            f"{reminder[1]} ({reminder[3]}) — нажми "
            f"/done{reminder[0]} чтобы завершить "
            for reminder in reminders]
        answer_message = f"**NOTIFICATION**\n\n* " + "\n\n* " \
            .join(last_reminders_rows)

        await bot.send_message(chat_id=ACCESS_ID, text=answer_message)


async def scheduler():
    aioschedule.every(1).minutes.do(job)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
