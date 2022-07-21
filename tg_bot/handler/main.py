from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types.web_app_info import WebAppInfo

from utils.youtube import *
from utils.db_new import db
from utils.wrappers import log

from keys import *
from data.text import *


@log 
async def start(message: types.Message):
    if message.chat.type == 'private':
        await message.answer(welcome_text, reply_markup=main_btn, disable_notification=True)
        check_list = db.subscribers_search_by_id(message['from']['id'])

        if not check_list :
            db.subscribers_to_db(message['from']['id'],message['from']['first_name'],message['from']['username'])
            db.add_to_active_sub_table(message['from']['id'], '1', '0', '0')
        db.stats(message['from']['id'], message['text'], message['date'])
        db.update_sub_on_start(message['from']['id'], '1')


# О нас
async def start_inline(call : types.CallbackQuery):
    await call.message.answer(start_message_after_back, reply_markup=main_btn, disable_notification=True)
    

@log
async def about_us(message: types.Message):
    await message.answer(about_us_text, disable_notification=True, reply_markup=social_net_inl)
    db.stats(message['from']['id'], message['text'], message['date'])   

@log
async def subscribe_answer(message: types.Message):
    sub = db.sub_spam_allow_serch_by_id(message['from']['id'])
    if not sub :
        db.add_to_active_sub_table(message['from']['id'], '1', '0', '0')
    await message.answer(get_video_answer, reply_markup=sub_inl_bnt, disable_notification=True)
    await message.answer(annonce_sub_answer_text, reply_markup=annonce_sub_inl_bnt, disable_notification=True)
    db.stats(message['from']['id'], message['text'], message['date'])
#  Подписка на новые видео на YT

@log
async def sub_yt_last_video(call: types.CallbackQuery):
    db.update_sub_allow_spam(call['from']['id'],'1','1')
    await call.message.answer(sub_text, disable_notification=True)

@log
async def unsub_yt_last_video(call: types.CallbackQuery):
    db.update_sub_allow_spam(call['from']['id'],'1','0')    
    await call.message.answer(unsub_text, disable_notification=True)

#  анонсы онлайн лекций
@log
async def sub_annonce(call: types.CallbackQuery):
    db.update_annonce_sub(call['from']['id'],'1','1')
    await call.message.answer(sub_text, disable_notification=True)

@log
async def unsub_annonce(call: types.CallbackQuery):
    db.update_annonce_sub(call['from']['id'],'1','0')    
    await call.message.answer(unsub_text, disable_notification=True)


async def hitas_def(message: types.Message):
    await message.answer(hitas_cmd, reply_markup=hitas_btn)

async def date_conversion_def(message: types.Message):
    await message.answer(date_conversion_cmd, reply_markup=date_conversion_btn)


def handlers_main(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    
    dp.register_message_handler(about_us, commands=['about'])
    dp.register_message_handler(about_us, Text(equals = 'О нас', ignore_case = True))

    dp.register_message_handler(subscribe_answer, commands=['subscribe_answer'])
    dp.register_message_handler(subscribe_answer, Text(equals = 'Подписаться на рассылку', ignore_case = True))

    dp.register_callback_query_handler(sub_yt_last_video, text='sub')
    dp.register_callback_query_handler(unsub_yt_last_video, text='unsub')

    dp.register_callback_query_handler(sub_annonce, text='ann_sub')
    dp.register_callback_query_handler(unsub_annonce, text='ann_unsub')

    dp.register_callback_query_handler(start_inline, text='start')
    
    dp.register_message_handler(hitas_def, Text(equals = hitas_cmd, ignore_case = True))
    dp.register_message_handler(date_conversion_def, Text(equals = date_conversion_cmd, ignore_case = True))