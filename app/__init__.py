from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.settings.middleware import AccessMiddleware
from app.settings.tokens import API_TOKEN, ACCESS_ID

# Initialize bot, local storage and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(middleware=AccessMiddleware(ACCESS_ID))
