from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from create_bot import telegram_bot

from utils.youtube import *
from utils.db_new import db


# Класс состояний
class Form(StatesGroup):
    ann_text_message = State()
    ann_confirm_spam = State()


async def spam(message: types.Message):
    admins = db.show_all_from_table('admins')
    if message.chat.type == 'private':
        for item in admins:
            if message['from']['id'] == item[0]:
                await message.answer('Сообщение для рассылки \nДля отмены /cancel')
                await Form.ann_text_message.set() # Устанавливаем состояние
                db.stats(message['from']['id'], message['text'], message['date'])


async def start_spam_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['text_message'] = message.caption
        proxy['content'] = message.photo[0].file_id
        proxy['type'] = 'send_photo'
    await Form.ann_confirm_spam.set() # Переход состояния
    await message.answer('Для подтверждения /confirm\nДля отмены /cancel')


async def start_spam_text(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['text_message'] = message.text
        proxy['type'] = 'send_message'
    await Form.ann_confirm_spam.set() # Переход состояния
    await message.answer('Для подтверждения /confirm\nДля отмены /cancel')
    

async def start_spam_document(message: types.Document, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['text_message'] = message.caption
        proxy['content'] = message.document.file_id
        proxy['type'] = 'send_document' 
    await Form.ann_confirm_spam.set() # Переход состояния
    await message.answer('Для подтверждения /confirm\nДля отмены /cancel')


async def start_spam_video(message: types.Document, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['text_message'] = message.caption
        proxy['content'] = message.video.file_id
        proxy['type'] = 'send_video'
    await Form.ann_confirm_spam.set() # Переход состояния
    await message.answer('Для подтверждения /confirm\nДля отмены /cancel')


async def start_spam_audio(message: types.Document, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['text_message'] = message.caption
        proxy['content'] = message.audio.file_id
        proxy['type'] = 'send_audio'
    await Form.ann_confirm_spam.set() # Переход состояния
    await message.answer('Для подтверждения /confirm\nДля отмены /cancel')


async def start_spam_voice(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['content'] = message.voice.file_id
        proxy['type'] = 'send_voice'
    await Form.ann_confirm_spam.set() # Переход состояния 
    await message.answer('Для подтверждения /confirm\nДля отмены /cancel')
    

async def confirm_send_spam (message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        pass
    sub_list = db.annonce_sub_spam_allow('1')
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


# Регистрация хендлеров
def handlers_annonce_spam(dp: Dispatcher):
    # Начало
    dp.register_message_handler(spam, commands=['annonce_spam'])
    dp.register_message_handler(spam, Text(equals = 'Рассылка(анонс)', ignore_case = True))
    # Подтверждение
    dp.register_message_handler(confirm_send_spam, state=Form.ann_confirm_spam, commands='confirm')
    # Типы контента для рассылки
    dp.register_message_handler(start_spam_text, state=Form.ann_text_message)
    dp.register_message_handler(start_spam_photo, content_types=['photo'], state=Form.ann_text_message)
    dp.register_message_handler(start_spam_document, content_types=['document'], state=Form.ann_text_message)
    dp.register_message_handler(start_spam_voice, content_types=['voice'], state=Form.ann_text_message)
    dp.register_message_handler(start_spam_video, content_types=['video'], state=Form.ann_text_message)
    dp.register_message_handler(start_spam_audio, content_types=['audio'], state=Form.ann_text_message)
