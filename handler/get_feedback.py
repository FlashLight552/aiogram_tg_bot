from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text


from utils.db_new import db
from keys import main_btn



class Form(StatesGroup):
    text_review = State()

async def start_feedback(message: types.Message):
    await message.answer('Будем рады услышать отзывы и пожелания! Напишите в чат Ваше сообщение \nДля отмены /cancel')
    await Form.text_review.set() # Устанавливаем состояни
    db.stats(message['from']['id'], message['text'], message['date'])

async def get_feedback(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['text'] = message.text
        await state.finish() # Выключаем состояние
        db.feedback_to_db(message['from']['id'], proxy['text'])
        await message.answer('Cпасибо за Ваш отзыв.', reply_markup=main_btn)


def register_feedback(dp: Dispatcher):   
    dp.register_message_handler(start_feedback, commands=['start_feedback']) 
    dp.register_message_handler(start_feedback, Text(equals = 'Отзыв', ignore_case = True))        

    dp.register_message_handler(get_feedback, state=Form.text_review)