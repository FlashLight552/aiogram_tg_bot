from aiogram.utils import executor
import logging
import asyncio

from create_bot import dp
from handler import main, spam, youtube, admin
from utils.scheduled import scheduled_last_video, scheduled_popular_video
from utils.db import admins  
from data.config import owner

   
# Логи
logging.basicConfig(level=logging.INFO)

# Коннект хендлеров
main.handlers_main(dp)
youtube.handlers_youtube(dp)
spam.handlers_spam(dp)
admin.admin(dp)


if __name__ == '__main__':
    admins(owner, 'owner', 'Господин')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(scheduled_popular_video(24 * 60 * 60)) # Таймер 24 часа
    loop.create_task(scheduled_last_video(60)) # Таймер 1 минута

    executor.start_polling(dp, skip_updates=True)
    