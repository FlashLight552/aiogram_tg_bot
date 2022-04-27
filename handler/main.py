from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from utils.youtube import *
from utils.db_new import db
from utils.wrappers import log


from keys import *
from data.text import *



# Команда старт и вывод наэкранных кнопок
@log 
async def send_welcome(message: types.Message):
    if message.chat.type == 'private':
        #await message.delete()

        # photo = open(f'img/logo.png', 'rb')
        await message.answer(welcome_text, reply_markup=main_btn)
        # await message.answer_photo(photo, caption=welcome_text, reply_markup=main_btn)
        check_list = db.subscribers_search_by_id(message['from']['id'])



        if not check_list :
            # print ('Добавил новую, ', check_list)
            db.subscribers_to_db(message['from']['id'],message['from']['first_name'],message['from']['username'])
            db.add_to_active_sub_table(message['from']['id'], '1', '0', '0')
        db.stats(message['from']['id'], message['text'], message['date'])
        db.update_sub_on_start(message['from']['id'], '1')
# О нас

@log
async def about_us(message: types.Message):
 
    await message.answer(about_us_text)
    db.stats(message['from']['id'], message['text'], message['date'])   
    return int(message['from']['id'])

@log
async def subscribe_answer(message: types.Message):
    sub = db.sub_spam_allow_serch_by_id(message['from']['id'])
    if not sub :
        db.add_to_active_sub_table(message['from']['id'], '1', '0', '0')
    await message.answer('Хотите получать нашу рассылку с новыми видео и интересными новостями?', reply_markup=sub_inl_bnt)
    await message.answer(annonce_sub_answer_text, reply_markup=annonce_sub_inl_bnt )
    db.stats(message['from']['id'], message['text'], message['date'])
#  Подписка на новые видео на YT

@log
async def sub(call: types.CallbackQuery):
    db.update_sub_allow_spam(call['from']['id'],'1','1')
    await call.message.answer('Подписка оформлена, спасибо!')

@log
async def unsub(call: types.CallbackQuery):
    db.update_sub_allow_spam(call['from']['id'],'1','0')    
    await call.message.answer('Подписка отключена! Возвращайтесь к нам как можно скорее!')

#  анонсы онлайн лекций
@log
async def ann_sub(call: types.CallbackQuery):
    db.update_annonce_sub(call['from']['id'],'1','1')
    await call.message.answer('Подписка оформлена, спасибо!')

@log
async def ann_unsub(call: types.CallbackQuery):
    db.update_annonce_sub(call['from']['id'],'1','0')    
    await call.message.answer('Подписка отключена! Возвращайтесь к нам как можно скорее!')


def handlers_main(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    
    dp.register_message_handler(about_us, commands=['about'])
    dp.register_message_handler(about_us, Text(equals = 'О нас', ignore_case = True))

    dp.register_message_handler(subscribe_answer, commands=['subscribe_answer'])
    dp.register_message_handler(subscribe_answer, Text(equals = 'Подписаться на рассылку', ignore_case = True))

    dp.register_callback_query_handler(sub, text='sub')
    dp.register_callback_query_handler(unsub, text='unsub')

    dp.register_callback_query_handler(ann_sub, text='ann_sub')
    dp.register_callback_query_handler(ann_unsub, text='ann_unsub')
  