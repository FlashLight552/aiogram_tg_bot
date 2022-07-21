from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text


from utils.db_new import db
from keys import *
from create_bot import telegram_bot
from data.text import *


class Form(StatesGroup):
    text_review = State()


async def start_feedback(message: types.Message):
    await message.answer(start_feedback_text, reply_markup=cancel_kb, disable_notification=True)
    await Form.text_review.set()
     

async def get_feedback(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['text'] = message.text
        await state.finish()
        db.feedback_to_db(message['from']['id'], proxy['text'])
        await message.answer(get_feedback_text, reply_markup=main_btn, disable_notification=True)
        
        db.stats(message['from']['id'], 'Оставить отзыв', message['date'])
       
        admins = db.show_all_from_table('admins')
        for item in admins:
            if item[1] != 'owner':
                try:
                    await telegram_bot.send_message(item[0],'Новый отзыв записан')
                except: pass


def register_feedback(dp: Dispatcher):   
    dp.register_message_handler(start_feedback, Text(equals = start_feedback_cmd, ignore_case = True))        
    dp.register_message_handler(get_feedback, state=Form.text_review)