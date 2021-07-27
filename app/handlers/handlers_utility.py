from typing import Tuple

from aiogram.types import InlineKeyboardMarkup, Message, InlineKeyboardButton

from app import reminders
from app.buttons.reply_btns import remindersMenu, anyRemindersMenu
from app.utility.answer_forms import answer_forms


async def handler_show_all(message: Message, show_header: bool = True) -> Tuple[str, InlineKeyboardMarkup]:
    inline_kb_to_choose = InlineKeyboardMarkup(row_width=6)
    data = reminders.get_all_reminders()
    temp = 1
    result_string = ''
    await message.delete()
    if data:
        if show_header:
            await message.answer("All reminders:", reply_markup=anyRemindersMenu)
        for elem in data:
            inline_btn = InlineKeyboardButton(temp, callback_data=f"edit_{elem[0]}")
            inline_kb_to_choose.insert(inline_btn)
            result_string += answer_forms(element=elem, position=temp, adding=True)
            temp += 1

        await message.answer(result_string, reply_markup=inline_kb_to_choose)
    else:
        await message.answer("No reminders in system.", reply_markup=remindersMenu)

    return result_string, inline_kb_to_choose


async def handler_show_permanent(message: Message, show_header: bool = True) -> Tuple[str, InlineKeyboardMarkup]:
    inline_kb_to_choose = InlineKeyboardMarkup(row_width=6)
    data = reminders.get_permanent_reminders()
    temp = 1
    result_string = ''

    await message.delete()
    if data:
        if show_header:
            await message.answer("Permanent reminders:", reply_markup=anyRemindersMenu)
        for elem in data:
            inline_btn = InlineKeyboardButton(temp, callback_data=f"edit_{elem[0]}")
            inline_kb_to_choose.insert(inline_btn)
            result_string += answer_forms(element=elem, position=temp, adding=True)
            temp += 1

        await message.answer(result_string, reply_markup=inline_kb_to_choose)
    else:
        await message.answer("No permanent reminders in system.", reply_markup=remindersMenu)

    return result_string, inline_kb_to_choose


async def handler_show_temporary(message: Message, show_header: bool = True) -> Tuple[str, InlineKeyboardMarkup]:
    inline_kb_to_choose = InlineKeyboardMarkup(row_width=6)
    data = reminders.get_temporary_reminders()
    temp = 1
    result_string = ''

    await message.delete()
    if data:
        if show_header:
            await message.answer("Temporary reminders:", reply_markup=anyRemindersMenu)
        for elem in data:
            inline_btn = InlineKeyboardButton(temp, callback_data=f"edit_{elem[0]}")
            inline_kb_to_choose.insert(inline_btn)
            result_string += answer_forms(element=elem, position=temp, adding=True)
            temp += 1

        await message.answer(result_string, reply_markup=inline_kb_to_choose)
    else:
        await message.answer("No temporary reminders in system.", reply_markup=remindersMenu)

    return result_string, inline_kb_to_choose


async def handler_show_bookmarks(message: Message, show_header: bool = True) -> Tuple[str, InlineKeyboardMarkup]:
    inline_kb_to_choose = InlineKeyboardMarkup(row_width=6)
    data = reminders.get_bookmarks()
    temp = 1
    result_string = ''

    await message.delete()
    if data:
        if show_header:
            await message.answer("Bookmarks:", reply_markup=anyRemindersMenu)
        for elem in data:
            inline_btn = InlineKeyboardButton(temp, callback_data=f"edit_{elem[0]}")
            inline_kb_to_choose.insert(inline_btn)
            result_string += answer_forms(element=elem, position=temp, adding=True)
            temp += 1

        await message.answer(result_string, reply_markup=inline_kb_to_choose)
    else:
        await message.answer("No bookmarks in system.", reply_markup=remindersMenu)

    return result_string, inline_kb_to_choose
