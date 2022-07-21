from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from data.config import token
from pathlib import Path


telegram_bot = Bot(token=token)
storage = JSONStorage(Path.cwd() / "resources/fsm_data.json")
dp = Dispatcher(telegram_bot, storage=storage)
    