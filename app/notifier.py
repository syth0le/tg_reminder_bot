import asyncio
import datetime

import aioschedule
from aiogram.types import InlineKeyboardMarkup

from app import db, bot
import app.buttons.inline_btns as i_btn
from app.settings.tokens import ACCESS_ID
from app.utility.stickers import stickers_recognize


async def job():
    local_time = str(datetime.datetime.now())[:-9] + "00"
    print(datetime.datetime.now().timestamp())
    print(datetime.datetime.now())
    inline_kb_to_choose = InlineKeyboardMarkup(row_width=6)
    temp = 1
    result_string = ''
    notifications = db.find_by_date('reminder', local_time)

    if notifications:
        for elem in notifications:
            # print(elem)
            # print(elem[3])
            if elem[2] == 'perm':
                db.extend_by_id(table='reminder', row_id=elem[0], date=elem[3], frequency=elem[5])
            stick_done, stick_type = stickers_recognize(elem[4], elem[2])

            answer_message = f"**NOTIFICATION**\n\n" \
                             + f'{stick_done} {stick_type} - {elem[1]}:\n{elem[3]}\n id:{elem[0]}'
            await bot.send_message(chat_id=ACCESS_ID, text=answer_message, reply_markup=i_btn.inline_kb_edit1)
            # здесь тоже storage подключить


# if notifications:
#     for elem in notifications:
#         inline_btn = InlineKeyboardButton(temp, callback_data=f"edit_{elem[0]}")
#         inline_kb_to_choose.insert(inline_btn)
#         print(elem)
#         if elem[3]:
#             stick = STICKER_DONE
#         else:
#             stick = STICKER_NOT_DONE
#         result_string += f'{temp}) {stick} - {elem[1]}:\n{elem[3]}\n'
#         temp += 1
#
#     answer_message = f"**NOTIFICATION**\n\n* " + "\n\n* " + result_string
#     await bot.send_message(chat_id=ACCESS_ID, text=answer_message, reply_markup=inline_kb_to_choose)


async def scheduler():
    aioschedule.every(58).seconds.do(job)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
