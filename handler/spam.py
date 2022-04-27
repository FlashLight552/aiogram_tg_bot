from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.utils.markdown import hlink
from aiogram.dispatcher.filters import Text
# from aiogram.types import InputFile
# import os

# from pyparsing import conditionAsParseAction

from create_bot import telegram_bot
# from create_bot import dp
# from data.config import yt_channel_id, owner
from utils.youtube import *
from utils.db_new import db


# Класс состояний
class Form(StatesGroup):
    text_message = State()
    confirm_spam = State()
    
async def spam(message: types.Message):
    admins = db.show_all_from_table('admins')
    if message.chat.type == 'private':
        for item in admins:
            if message['from']['id'] == item[0]:
                await message.answer('Сообщение для рассылки \nДля отмены /cancel')
                await Form.text_message.set() # Устанавливаем состояние

async def cancel_spam(message: types.Message, state: FSMContext):
    current_stage = await state.get_state()
    if current_stage is None:
        return
    await state.finish() # Выключаем состояние
    await message.answer('Охрана, отмена')


async def start_spam_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['text_message'] = message.caption
        proxy['content'] = message.photo[0].file_id
        proxy['type'] = 'send_photo'
    await Form.confirm_spam.set() # Переход состояния
    await message.answer('Для подтверждения /confirm\nДля отмены /cancel')

async def start_spam_text(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['text_message'] = message.text
        proxy['type'] = 'send_message'
    await Form.confirm_spam.set() # Переход состояния
    await message.answer('Для подтверждения /confirm\nДля отмены /cancel')
    
async def start_spam_document(message: types.Document, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['text_message'] = message.caption
        proxy['content'] = message.document.file_id
        proxy['type'] = 'send_document' 
    await Form.confirm_spam.set() # Переход состояния
    await message.answer('Для подтверждения /confirm\nДля отмены /cancel')

async def start_spam_video(message: types.Document, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['text_message'] = message.caption
        proxy['content'] = message.video.file_id
        proxy['type'] = 'send_video'
    await Form.confirm_spam.set() # Переход состояния
    await message.answer('Для подтверждения /confirm\nДля отмены /cancel')

async def start_spam_audio(message: types.Document, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['text_message'] = message.caption
        proxy['content'] = message.audio.file_id
        proxy['type'] = 'send_audio'
    await Form.confirm_spam.set() # Переход состояния
    await message.answer('Для подтверждения /confirm\nДля отмены /cancel')

async def start_spam_voice(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['content'] = message.voice.file_id
        proxy['type'] = 'send_voice'
    await Form.confirm_spam.set() # Переход состояния 
    await message.answer('Для подтверждения /confirm\nДля отмены /cancel')
    
async def confirm_send_spam (message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        pass
    sub_list = db.show_all_from_table('subscribers')
    for item in sub_list:
        try:
            if proxy['type'] == 'send_document':
                await telegram_bot.send_document(item[0], proxy['content'], caption=proxy['text_message'])
                db.update_sub(item[0], '1')
            if proxy['type'] == 'send_photo':
                await telegram_bot.send_photo(item[0],proxy['content'], caption=proxy['text_message'])
                db.update_sub(item[0], '1')
            if proxy['type'] == 'send_video':
                await telegram_bot.send_video(item[0], proxy['content'], caption=proxy['text_message'])
                db.update_sub(item[0], '1')
            if proxy['type'] == 'send_audio':
                await telegram_bot.send_audio(item[0], proxy['content'], caption=proxy['text_message'])   
                db.update_sub(item[0], '1')             
            if proxy['type'] == 'send_voice':
                await telegram_bot.send_voice(item[0],proxy['content']) 
                db.update_sub(item[0], '1')
            if proxy['type'] == 'send_message': 
                await telegram_bot.send_message(item[0],proxy['text_message']) 
                db.update_sub(item[0], '1')      
        except:
            db.add_to_active_sub_table(item[0], '0','0','0')   
    await message.answer('Спам окончен, хи-хи-хи')
    await state.finish()


# async def spam_video_from_group(message: types.Document):
#     print(message)
#     caption = message.caption
#     video_file = message.video.file_id
#     await telegram_bot.send_video(330663508, video_file, caption=caption)

# Регистрация хендлеров
def handlers_spam(dp: Dispatcher):
    # Начало
    dp.register_message_handler(spam, commands=['spam'])
    dp.register_message_handler(spam, Text(equals = 'Рассылка(всем)', ignore_case = True))
    # Отмена    
    dp.register_message_handler(cancel_spam, state="*", commands='cancel')
    dp.register_message_handler(cancel_spam, Text(equals = 'cancel', ignore_case = True), state="*" )
    # Подтверждение
    dp.register_message_handler(confirm_send_spam, state=Form.confirm_spam, commands='confirm')
    # Типы контента для рассылки
    dp.register_message_handler(start_spam_text, state=Form.text_message)
    dp.register_message_handler(start_spam_photo, content_types=['photo'], state=Form.text_message)
    dp.register_message_handler(start_spam_document, content_types=['document'], state=Form.text_message)
    dp.register_message_handler(start_spam_voice, content_types=['voice'], state=Form.text_message)
    dp.register_message_handler(start_spam_video, content_types=['video'], state=Form.text_message)
    dp.register_message_handler(start_spam_audio, content_types=['audio'], state=Form.text_message)
    
    # Парсинг с тг групп и каналов
    # dp.register_message_handler(spam_video_from_group, content_types=['video'])
    # dp.register_channel_post_handler(spam_video_from_group, content_types=['video'])
