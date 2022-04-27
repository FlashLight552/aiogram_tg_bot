from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text


from utils.db_new import db
from keys import main_btn
from create_bot import telegram_bot


class Form(StatesGroup):
    text_review = State()

async def start_feedback(message: types.Message):
    await message.answer('Будем рады услышать отзывы и пожелания! Напишите в чат Ваше сообщение \nДля отмены /cancel')
    await Form.text_review.set() # Устанавливаем состояни
     

async def get_feedback(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['text'] = message.text
        await state.finish() # Выключаем состояние
        db.feedback_to_db(message['from']['id'], proxy['text'])
        await message.answer('Cпасибо за Ваш отзыв.', reply_markup=main_btn)
        db.stats(message['from']['id'], 'Оставить отзыв', message['date'])
       
        admins = db.show_all_from_table('admins')
        # print (admins)
        for item in admins:
            # if message['from']['id'] == item[0]:
            if item[1] != 'owner':
                try:
                    await telegram_bot.send_message(item[0],'Новый отзыв записан')
                    # print(item)
                except: pass

def register_feedback(dp: Dispatcher):   
    dp.register_message_handler(start_feedback, commands=['start_feedback']) 
    dp.register_message_handler(start_feedback, Text(equals = 'Отзыв', ignore_case = True))        

    dp.register_message_handler(get_feedback, state=Form.text_review)