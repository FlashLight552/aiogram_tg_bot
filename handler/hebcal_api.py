from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from utils.youtube import *
from utils.db_new import db
from utils.geo import  get_geo_user
from keys import *
from data.text import *
import requests

from datetime import datetime




def shabbat_time_request(user_id):
        status = db.check_location(user_id)
        request_shabbat_time = requests.get('https://www.hebcal.com/shabbat?cfg=json&geonameid='+str(status[5])+'M=on&leyning=off&lg=ru')
        shabbat_time = (request_shabbat_time.json())

        text = str(status[4]) + ' ' + str(status[3]) +'\n\n'
        for item in shabbat_time['items']:
            if item['category'] == 'candles' or item['category'] == 'zmanim' or item['category'] == 'havdalah' or item['category'] == 'holiday':
                title = item['title']
                date = datetime.fromisoformat(item['date']).date()
                time = datetime.fromisoformat(item['date']).time()
                if str(time) == '00:00:00': time = ''
                if "Авдала:" in title: title = title.replace('Авдала:', 'Авдала (исход Шаббата):')
                
                text = text + title + '\nДата: ' + str(date) + ' ' + str(time).replace(':00','',1) +'\n\n'
        return(text)

def zmanim(user_id):
    status = db.check_location(user_id)
    request_zmanim = requests.get('https://www.hebcal.com/zmanim?cfg=json&geonameid='+str(status[5]))
    zmanim = (request_zmanim.json())
    for item in zmanim['times']:
        print(item)


async def update_location(message : types.Message):
    if message.chat.type == 'private':
        text =  'Пожалуйста, нажмите кнопку "Геолокация" в меню и дайте разрешение на отправку геоданных.\n' \
                'Обратите внимание, точное время Шаббата доступно не для всех городов/сел, поэтому в результате поиска Вам может быть показано время Шаббата в ближайшем к Вам населенном пункте.\n'\
                'Вернуться в главное меню? \nнажмите /start'
        await message.answer(text,reply_markup=markup_request)
        db.stats(message['from']['id'], message['text'], message['date'])

async def check_db_send_time(message: types.Message):
    if message.chat.type == 'private':
        status = db.check_location(message.from_user.id)
        if status: 
            text = shabbat_time_request(message.from_user.id) 
            await message.answer(text + 'Находитесь в другом месте? Обновите свою геолокацию \n/update', reply_markup=main_btn, disable_notification=True)
            await message.answer('Хотите получить инструкцию, как зажигать свечи или проводить Авдалу?', reply_markup=inl_bnt, disable_notification=True)  
        else:
            text = 'Тут Вы можете узнать время наступления Субботы (Шаббата) в Вашем городе. ' \
                    'Для определения местоположения нужно воспользоваться этой функцией на мобильном телефоне (с компьютера эта функция не работает).\n'\
                    'Пожалуйста, нажмите кнопку "Геолокация" в меню и дайте разрешение на отправку геоданных. '\
                    'Обратите внимание, точное время Шаббата доступно не для всех городов/сел, поэтому в результате поиска Вам может быть показано время Шаббата в ближайшем к Вам населенном пункте.\n'\
                    'Вернуться в главное меню? \nнажмите /start'   
            await message.answer(text, reply_markup=markup_request)
    db.stats(message['from']['id'], message['text'], message['date'])

async def get_loc_from_btn(message: types.Message):
    get_geo_user(message.location.latitude, message.location.longitude, message.from_user.id, message.from_user.first_name, message.from_user.username)
    text = shabbat_time_request(message.from_user.id)
    await message.delete() 
    await message.answer(text, reply_markup=main_btn, disable_notification=True)
    await message.answer('Хотите получить инструкцию, как зажигать свечи или проводить Авдалу?', reply_markup=inl_bnt, disable_notification=True)    
    db.stats(message['from']['id'], message['text'], message['date'])

async def callback_shabbat_light(call: types.CallbackQuery):
    await call.message.answer(shabbat_light,  parse_mode='HTML')
    
async def callback_avdala(call: types.CallbackQuery):
    await call.message.answer(avdala , parse_mode='HTML')


def handlers_shabbat_time(dp: Dispatcher):
    dp.register_message_handler(get_loc_from_btn, content_types=['location'])

    dp.register_message_handler(check_db_send_time, commands=['shabbat'])
    dp.register_message_handler(check_db_send_time, Text(equals = 'Время Шаббата', ignore_case = True))
    
    dp.register_message_handler(update_location, commands=['update'])
    
    dp.register_callback_query_handler(callback_shabbat_light, text='shabbat_light_callbk')
    dp.register_callback_query_handler(callback_avdala, text='avdala_btn_callbk')

  