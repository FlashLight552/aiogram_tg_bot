from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.config import token


telegram_bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(telegram_bot, storage=storage)
    