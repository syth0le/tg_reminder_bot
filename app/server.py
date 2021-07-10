from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import MessageNotModified
import app.buttons.inline_btns as i_btn
import app.buttons.reply_btns as r_btn
from app import dp, bot, reminders, storage, db
from app.settings.tokens import ACCESS_ID
from app.utility.forms import FormTemp, FormPerm, FormBookmark
from app.utility.stickers import stickers_recognize, STICKER_DONE


@dp.message_handler(lambda message: message.text.startswith('Create'))
async def process_command_1(message: types.Message):
    await message.delete()
    await message.answer("Choose type of reminder:", reply_markup=i_btn.inline_kb1)


@dp.callback_query_handler(lambda c: c.data == 'btn_cancel')
async def process_callback_btn_cancel(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.message.chat.id,
                           text="Cancel",
                           reply_markup=r_btn.mainMenu)


@dp.callback_query_handler(lambda c: c.data == 'cancel_adding', state='*')
async def cancel_handler(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.message.chat.id,
                           text="Canceled",
                           reply_markup=r_btn.mainMenu)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'btn_temp')
async def process_callback_btn_temp(callback_query: types.CallbackQuery):
    await FormTemp.title.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text="Enter title of reminder:",
                                reply_markup=i_btn.inline_kb2)


@dp.message_handler(state=FormTemp.title)
async def process_title_temp(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text

    await FormTemp.next()
    await bot.send_message(
        chat_id=message.chat.id,
        text="Enter date/time of reminder:",
        reply_markup=i_btn.inline_kb2
    )
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id - 1
    )


@dp.message_handler(state=FormTemp.date)
async def process_date_temp(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text

        answer = reminders.add_reminder(title=data['title'],
                                        date=data['date'],
                                        category='temp')
        stick_done, stick_type = stickers_recognize(answer.is_done, answer.type)

        answer_message = f'{stick_done} {stick_type} - {answer.title}:\n{answer.date}\n id:{answer.id}'

        await bot.send_message(
            message.chat.id,
            answer_message,
            reply_markup=i_btn.inline_kb_edit1
        )
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id - 1
        )

    await state.finish()


##############################################################################


@dp.callback_query_handler(lambda c: c.data == 'btn_perm')
async def process_callback_btn_perm(callback_query: types.CallbackQuery):
    await FormPerm.title.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text="Enter title of reminder:",
                                reply_markup=i_btn.inline_kb2)


@dp.message_handler(state=FormPerm.title)
async def process_title_perm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text

    await FormPerm.next()
    await bot.send_message(
        chat_id=message.chat.id,
        text="Enter date/time of repeated reminder:",
        reply_markup=i_btn.inline_kb2
    )
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id - 1
    )


@dp.message_handler(state=FormPerm.date)
async def process_date_perm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text

    await FormPerm.next()
    await bot.send_message(
        chat_id=message.chat.id,
        text="Enter frequency of repeated reminder:",
        reply_markup=i_btn.inline_kb2
    )
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id - 1
    )


@dp.message_handler(state=FormPerm.frequency)
async def process_frequency_perm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['frequency'] = message.text

        answer = reminders.add_reminder(title=data['title'],
                                        date=data['date'],
                                        category='perm',
                                        frequency=data['frequency'])
        stick_done, stick_type = stickers_recognize(answer.is_done, answer.type)

        answer_message = f'{stick_done} {stick_type} - {answer.title}:\n{answer.date}\n id:{answer.id}'

        await bot.send_message(
            message.chat.id,
            answer_message,
            reply_markup=i_btn.inline_kb_edit1
        )
        # await bot.edit_message_text(
        #     chat_id=message.chat.id,
        #     message_id=message.message_id - 1,
        #     text="Enter frequency of repeated reminder:",
        #     reply_markup=btn.inline_kb2
        # ) СДЕЛАТЬ ИНЛАЙНОМ ПОСЛЕДНЕЕ ДЕЙСТВИЕ ТИПА ПОДТВЕРДИТЬ ИЛИ ЧЕ ТО ТИПА ТАКОГО ИЛИ ВООБЩЕ ВЫВЕСТИ ЗАМЕТКУ ТИП РЕДАКТИРОВАТЬ И ТЛ И ТП
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id - 1
        )

    await state.finish()


#################################################################


@dp.callback_query_handler(lambda c: c.data == 'btn_book')
async def process_callback_btn_book(callback_query: types.CallbackQuery):
    await FormBookmark.title.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text="Enter title of bookmark:",
                                reply_markup=i_btn.inline_kb2)


@dp.message_handler(state=FormBookmark.title)
async def process_title_book(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text

        answer = reminders.add_reminder(title=data['title'],
                                        date=None,
                                        category='book')
        stick_done, stick_type = stickers_recognize(answer.is_done, answer.type)

        answer_message = f'{stick_done} {stick_type} - {answer.title}\n id:{answer.id}'

        await bot.send_message(
            message.chat.id,
            answer_message,
            reply_markup=i_btn.inline_kb_edit1
        )
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id - 1
        )

    await state.finish()


#################################################################


@dp.callback_query_handler(lambda c: c.data == 'btn_done')
async def process_callback_btn_perm(callback_query: types.CallbackQuery):
    """Done only 1 reminder by identificator"""
    await bot.answer_callback_query(callback_query.id, text="Reminder was done.")
    text = str(callback_query.message.text)
    row_id = int(text.split('id:')[1])
    reminder = reminders.done_reminder(row_id)
    if text[1] == '*':
        text = text.split('**NOTIFICATION**\n\n')[1]
    if reminder.is_done == 0:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=callback_query.message.text,
                                    reply_markup=callback_query.message.reply_markup)
    else:
        done_text = text[1:]
        result_string = STICKER_DONE + done_text
        try:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=result_string,
                                        reply_markup=callback_query.message.reply_markup)
        except MessageNotModified:
            pass


@dp.callback_query_handler(lambda c: c.data == 'btn_delete')
async def process_callback_btn_perm(callback_query: types.CallbackQuery):
    """Delete only 1 reminder by identificator"""
    text = str(callback_query.message.text)
    row_id = int(text.split('id:')[1])
    reminder = reminders.delete_reminder(row_id)
    # print(reminder)
    if isinstance(reminder, str):
        result_string = reminder
    else:
        result_string = f'Reminder "{reminder.title}" was deleted'
    await bot.answer_callback_query(callback_query.id, text=result_string)
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.message.chat.id,
                           text="Choose in menu:",
                           reply_markup=r_btn.mainMenu)
    # Доделать появление списка при удалении


@dp.callback_query_handler(lambda c: c.data == 'btn_edit')
async def process_callback_btn_perm(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await storage.set_data(chat=ACCESS_ID, data={"text": callback_query.message.text,
                                                 "markup": i_btn.inline_kb_edit1_back})
    ## cделать проверку и переадрессацию на кнопку реплая исходя из темп или перм
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=callback_query.message.text,
                                reply_markup=i_btn.inline_kb_edit2)


@dp.callback_query_handler(lambda c: c.data == 'btn_back')
async def process_callback_btn_perm(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=callback_query.message.text,
                                reply_markup=i_btn.inline_kb_edit1)


@dp.callback_query_handler(lambda c: c.data == 'btn_edit_text')
async def process_callback_btn_perm(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text="EDIT TEXT",
                                reply_markup=i_btn.inline_kb_edit1)


@dp.callback_query_handler(lambda c: c.data == 'btn_edit_date')
async def process_callback_btn_perm(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text="EDIT DATE/TIME",
                                reply_markup=i_btn.inline_kb_edit1)


@dp.callback_query_handler(lambda c: c.data == 'btn_edit_type')
async def process_callback_btn_perm(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text="EDIT TYPE",
                                reply_markup=i_btn.inline_kb_edit1)


@dp.callback_query_handler(lambda c: c.data == 'btn_edit_frq')
async def process_callback_btn_perm(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text="EDIT FREQUENCY",
                                reply_markup=i_btn.inline_kb_edit1)


@dp.callback_query_handler(lambda c: c.data == 'btn_back_list')
async def process_callback_btn_perm(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    data = await storage.get_data(chat=ACCESS_ID)
    try:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=data['text'],
                                    reply_markup=data['markup'])
    except KeyError:
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text='Choose in menu:',
                               reply_markup=r_btn.mainMenu)


@dp.message_handler(commands=['start', 'help', 'menu'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(
        "Reminder bot",
        reply_markup=r_btn.mainMenu)


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
async def show_reminders(message: types.Message):
    await message.delete()
    await message.answer(message.text, reply_markup=r_btn.remindersMenu)


@dp.message_handler(lambda message: message.text.startswith('All'))
@dp.message_handler(commands=['all'])
async def show_all(message: types.Message):
    """Show all reminders in system."""
    inline_kb_to_choose = InlineKeyboardMarkup(row_width=6)
    data = reminders.get_all_reminders()
    temp = 1
    result_string = ''
    await message.delete()
    if data:
        await message.answer("All reminders:", reply_markup=r_btn.anyRemindersMenu)
        for elem in data:
            inline_btn = InlineKeyboardButton(temp, callback_data=f"edit_{elem[0]}")
            inline_kb_to_choose.insert(inline_btn)

            stick_done, stick_type = stickers_recognize(elem[4], elem[2])

            result_string += f'{temp}) {stick_done} {stick_type} - {elem[1]}:\n{elem[3]}\n'
            temp += 1

        await message.answer(result_string, reply_markup=inline_kb_to_choose)
    else:
        await message.answer("No reminders in system.", reply_markup=r_btn.mainMenu)

    await storage.set_data(chat=ACCESS_ID, data={"text": result_string,
                                                 "markup": inline_kb_to_choose})


@dp.message_handler(lambda message: message.text.startswith('Permanent'))
@dp.message_handler(commands=['perm'])
async def show_permanent(message: types.Message):
    """Show all permanent reminders in system."""
    inline_kb_to_choose = InlineKeyboardMarkup(row_width=6)
    data = reminders.get_permanent_reminders()
    temp = 1
    result_string = ''

    await message.delete()
    if data:
        await message.answer("Permanent reminders:", reply_markup=r_btn.anyRemindersMenu)
        for elem in data:
            inline_btn = InlineKeyboardButton(temp, callback_data=f"edit_{elem[0]}")
            inline_kb_to_choose.insert(inline_btn)

            stick_done, stick_type = stickers_recognize(elem[4], 'temp')

            result_string += f'{temp}) {stick_done} {stick_type} - {elem[1]}:\n{elem[3]}\n{elem[5]}\n'
            temp += 1

        await message.answer(result_string, reply_markup=inline_kb_to_choose)
    else:
        await message.answer("No permanent reminders in system.", reply_markup=r_btn.remindersMenu)

    await storage.set_data(chat=ACCESS_ID, data={"text": result_string,
                                                 "markup": inline_kb_to_choose})


@dp.message_handler(lambda message: message.text.startswith('Temporary'))
@dp.message_handler(commands=['temp'])
async def show_temporary(message: types.Message):
    """Show all temporary reminders in system."""
    inline_kb_to_choose = InlineKeyboardMarkup(row_width=6)
    data = reminders.get_temporary_reminders()
    temp = 1
    result_string = ''

    await message.delete()
    if data:
        await message.answer("Temporary reminders:", reply_markup=r_btn.anyRemindersMenu)
        for elem in data:
            inline_btn = InlineKeyboardButton(temp, callback_data=f"edit_{elem[0]}")
            inline_kb_to_choose.insert(inline_btn)
            stick_done, stick_type = stickers_recognize(elem[4], 'temp')
            result_string += f'{temp}) {stick_done} {stick_type} - {elem[1]}:\n{elem[3]}\n'
            temp += 1

        await message.answer(result_string, reply_markup=inline_kb_to_choose)
    else:
        await message.answer("No temporary reminders in system.", reply_markup=r_btn.remindersMenu)

    await storage.set_data(chat=ACCESS_ID, data={"text": result_string,
                                                 "markup": inline_kb_to_choose})


@dp.message_handler(lambda message: message.text.startswith('Bookmarks'))
@dp.message_handler(commands=['book'])
async def show_permanent(message: types.Message):
    """Show all bookmarks in system."""
    inline_kb_to_choose = InlineKeyboardMarkup(row_width=6)
    data = reminders.get_bookmarks()
    temp = 1
    result_string = ''

    await message.delete()
    if data:
        await message.answer("Bookmarks:", reply_markup=r_btn.anyRemindersMenu)
        for elem in data:
            inline_btn = InlineKeyboardButton(temp, callback_data=f"edit_{elem[0]}")
            inline_kb_to_choose.insert(inline_btn)
            print(elem)
            stick_done, stick_type = stickers_recognize(elem[4], 'book')
            result_string += f'{temp}) {stick_done} {stick_type} - {elem[1]}\n'
            temp += 1

        await message.answer(result_string, reply_markup=inline_kb_to_choose)
    else:
        await message.answer("No bookmarks in system.", reply_markup=r_btn.remindersMenu)

    await storage.set_data(chat=ACCESS_ID, data={"text": result_string,
                                                 "markup": inline_kb_to_choose})


@dp.message_handler(lambda message: message.text.startswith('Clean'))
@dp.message_handler(commands=['clean'])
async def clean(message: types.Message):
    """Clean db and delete reminders which were done later."""
    await message.delete()
    await message.answer(reminders.delete_done_reminders(), reply_markup=r_btn.mainMenu)


@dp.message_handler(lambda message: message.text.startswith('Back'))
async def back(message: types.Message):
    await message.delete()
    await message.answer(message.text, reply_markup=r_btn.mainMenu,
                         allow_sending_without_reply=True)


@dp.message_handler(lambda message: message.text.startswith('Cancel'))
async def cancel(message: types.Message):
    await message.delete()
    await message.answer(message.text, reply_markup=r_btn.mainMenu,
                         allow_sending_without_reply=True)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('edit_'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    id = callback_query.data[5:]
    reminder = db.find_by_id(table='reminder', id=id)
    stick_done, stick_type = stickers_recognize(reminder[4], reminder[2])
    if reminder[2] != 'book':
        result_string = f'{stick_done} {stick_type} - {reminder[1]}:\n{reminder[3]}\n id:{reminder[0]}'
    else:
        result_string = f'{stick_done} {stick_type} - {reminder[1]}\n id:{reminder[0]}'
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=result_string,
                                reply_markup=i_btn.inline_kb_edit1_back)