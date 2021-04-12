# import aioschedule
# import asyncio
# import datetime

# import db
# from server import bot

# async def job():
#     local_time = str(datetime.datetime.now())[:-9] + "00"
#     reminders = db.find_by_date('reminder', local_time)
#     print("notification", local_time)

#     if reminders:
#         last_reminders_rows = [
#             f"{reminder[1]} ({reminder[3]}) — нажми "
#             f"/done{reminder[0]} чтобы завершить "
#             for reminder in reminders]
#         answer_message = f"**NOTIFICATION**\n\n* " + "\n\n* "\
#                 .join(last_reminders_rows)
        
#         print(answer_message)

#         await bot.send_message(chat_id=ACCESS_ID, text=answer_message)

# async def scheduler():
#     aioschedule.every(1).minutes.do(job)
#     while True:
#         await aioschedule.run_pending()
#         await asyncio.sleep(1)

# async def on_startup(_):
#     asyncio.create_task(scheduler())