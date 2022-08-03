from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import hlink, link
from aiogram.dispatcher.filters import Text

from create_bot import dp
from utils.youtube import *
from utils.db_new import db
from data.config import yt_channel_id, yt_last_video_count, yt_popular_video_count, URL_PLAYLIST_YT
from data.text import *
from keys import *

from pytube import Playlist, YouTube
import random


# Класс состояний
class Form(StatesGroup):
    video_name = State()


# Поиск видео по имени на канале
async def start_search(message: types.Message):
    await message.answer(yt_video_search, reply_markup=cancel_kb, disable_notification=True)
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
        await message.answer(hyperlink + promo_text, parse_mode='HTML', reply_markup=main_btn, disable_notification=True)
    else:
            await message.answer(yt_video_not_found + promo_text, reply_markup=main_btn, disable_notification=True)
    
    db.stats(message['from']['id'], 'Поиск уроков', message['date'])


# Последнее видео на канале
async def last_video_yt(message: types.Message):
    list = db.youtube_video_show_all('last_video', yt_last_video_count)
    hyperlink = ''
    num = 0

    for item in list:
        num += 1
        hyperlink = hyperlink + '\n' + str(num) + '. ' + str(hlink(item[1],item[0]))   
                
    await message.answer(hyperlink + promo_text, parse_mode='HTML', disable_notification=True)
    db.stats(message['from']['id'], message['text'], message['date'])


# Популярные видео на канале
async def popular_video_yt(message: types.Message):
    list = db.youtube_video_show_all('popular_video', yt_popular_video_count)
    hyperlink = ''
    num = 0
    
    for item in list:
        num += 1
        hyperlink = hyperlink + '\n' + str(num) + '. ' + str(hlink(item[1],item[0]))   
                 
    await message.answer(hyperlink + promo_text, parse_mode='HTML', disable_notification=True)
    db.stats(message['from']['id'], message['text'], message['date'])


# Случайное видео с плейлиста
async def random_video(message: types.Message):
    url = URL_PLAYLIST_YT
    p = Playlist(url)
    url_list = []

    for url in p.video_urls:
        url_list.append(url)

    video = random.choice(url_list)
    await message.answer(hlink(YouTube(video).title, video), parse_mode='HTML')


# Регистрация хендлеров
def handlers_youtube(dp: Dispatcher):
    dp.register_message_handler(last_video_yt, commands=['last'])
    dp.register_message_handler(last_video_yt, Text(equals = last_video_yt_cmd, ignore_case = True))
    dp.register_message_handler(popular_video_yt, commands=['popular'])
    dp.register_message_handler(popular_video_yt, Text(equals = popular_video_yt_cmd, ignore_case = True))
    dp.register_message_handler(start_search, commands=['search'])
    dp.register_message_handler(start_search, Text(equals = start_search_cmd, ignore_case = True))
    dp.register_message_handler(start_search_pars, state=Form.video_name)
    dp.register_message_handler(random_video, Text(equals = random_video_cmd, ignore_case = True))
