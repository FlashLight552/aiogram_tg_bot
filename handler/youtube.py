from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import hlink
from aiogram.dispatcher.filters import Text

from create_bot import dp
from utils.youtube import *
from utils.db_new import db
from data.config import yt_channel_id, yt_last_video_count, yt_popular_video_count
from data.text import promo_text


# Класс состояний
class Form(StatesGroup):
    video_name = State()

# Поиск видео по имени на канале
async def start_search(message: types.Message):
    await message.answer('Введите название / фрагмент названия видео')
    await Form.video_name.set() 
    

async def start_search_pars(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy: 
        proxy['video_name'] = message.text
    await state.finish() 
    url, title = search_pars(proxy['video_name'])
    hyperlink = ''

    if url:
        count = len(url)
        for  i in range(0, count):
            num = i + 1
            hyperlink = hyperlink + '\n' + str(num) + '. ' + str(hlink(title[i],url[i]))           
        await message.answer(hyperlink + promo_text, parse_mode='HTML')
    else:
            await message.answer('Таких видео не найдено' + promo_text)
    db.stats(message['from']['id'], 'Поиск уроков', message['date'])


# Последнее видео на канале
async def last_video_yt(message: types.Message):
    list = db.youtube_video_show_all('last_video', yt_last_video_count)
    hyperlink = ''
    num = 0

    for item in list:
        num += 1
        hyperlink = hyperlink + '\n' + str(num) + '. ' + str(hlink(item[1],item[0]))   
                
    await message.answer(hyperlink + promo_text, parse_mode='HTML')
    db.stats(message['from']['id'], message['text'], message['date'])

# Популярные видео на канале

async def popular_video_yt(message: types.Message):
    list = db.youtube_video_show_all('popular_video', yt_popular_video_count)
    hyperlink = ''
    num = 0
    
    for item in list:
        num += 1
        hyperlink = hyperlink + '\n' + str(num) + '. ' + str(hlink(item[1],item[0]))   
                 
    await message.answer(hyperlink + promo_text, parse_mode='HTML')
    db.stats(message['from']['id'], message['text'], message['date'])

# Регистрация хендлеров
def handlers_youtube(dp: Dispatcher):
    dp.register_message_handler(last_video_yt, commands=['last'])
    dp.register_message_handler(last_video_yt, Text(equals = 'Новые уроки Торы', ignore_case = True))

    dp.register_message_handler(popular_video_yt, commands=['popular'])
    dp.register_message_handler(popular_video_yt, Text(equals = 'Популярные уроки', ignore_case = True))

    dp.register_message_handler(start_search, commands=['search'])
    dp.register_message_handler(start_search, Text(equals = 'Поиск уроков', ignore_case = True))

    dp.register_message_handler(start_search_pars, state=Form.video_name)
