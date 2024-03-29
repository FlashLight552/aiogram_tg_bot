from aiogram.utils import executor
import logging
import asyncio

from create_bot import dp
from handler import hebcal_api, main, spam, youtube, admin, get_feedback, annonce_spam, translate, webapp, shazam
from utils.scheduled import scheduled_last_video, scheduled_popular_video
from utils.db_new import db
from data.config import owner


# Логи
logging.basicConfig(level=logging.INFO)

# Коннект хендлеров
spam.handlers_spam(dp)
main.handlers_main(dp)
youtube.handlers_youtube(dp)
admin.admin(dp)
get_feedback.register_feedback(dp)
annonce_spam.handlers_annonce_spam(dp)
hebcal_api.handlers_shabbat_time(dp)
translate.handlers_translate(dp)
webapp.handlers_webapp(dp)
shazam.handlers_shazam(dp)


if __name__ == '__main__':
    db.create_tables()
    db.admins_to_db(owner, 'owner', 'Господин')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(scheduled_popular_video(24 * 60 * 60)) # Таймер 24 часа
    loop.create_task(scheduled_last_video(60)) # Таймер 1 минута

    executor.start_polling(dp, skip_updates=True)
    