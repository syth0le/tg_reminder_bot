import asyncio
from aiogram.utils import executor

from app.server import dp
from app.notifier import scheduler


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
