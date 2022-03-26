from cgitb import text
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from utils.youtube import *
from utils.db_new import db
from aiogram.utils.markdown import hlink
from utils.geo import shabbat_times
from keys import *
from data.text import *
import requests



# Команда старт и вывод наэкранных кнопок 
async def send_welcome(message: types.Message):
    if message.chat.type == 'private':
        #await message.delete()

        photo = open(f'img/logo.png', 'rb')
        welcome_text = 'Добро пожаловать! Брухим аБаим!\n' \
                        'Наш бот постоянно пополняется новыми функциями. Например, Вы можете узнать время Шаббата, получить ссылки на уроки Торы и т.д.\n' \
                        'Все, что доступно в данный момент Вы можете увидеть нажав на кнопку "меню".\n' \
                        'Будем рады Вашему отзыву или пожеланиям - кнопка "Отзыв"'
        await message.answer_photo(photo, caption=welcome_text, reply_markup=main_btn)
        check_list = db.subscribers_search_by_id(message['from']['id'])

        if not check_list :
            # print ('Добавил новую, ', check_list)
            db.subscribers_to_db(message['from']['id'],message['from']['first_name'],message['from']['username'])
            db.add_to_active_sub_table(message['from']['id'], '1', '0')
        db.stats(message['from']['id'], message['text'], message['date'])
# О нас
async def about_us(message: types.Message):
    text = 'Колель Тора - сеть ежедневного изучения Торы в странах СНГ и Европы\n' \
            'Мы работаем при еврейских общинах во множестве городов и онлайн.\n\n'   \
            'Наши страницы в соцсетях\n'  \
            'https://www.facebook.com/KolelToraRu/\n'  \
            'https://www.youtube.com/KolelTora'  
    await message.answer(text)
    db.stats(message['from']['id'], message['text'], message['date'])


async def subscribe_answer(message: types.Message):
    await message.answer('Хотите получать нашу рассылку с новыми видео и интересными новостями?', reply_markup=sub_inl_bnt)

async def sub(call: types.CallbackQuery):
    db.update_sub(call['from']['id'],'1','1')
    await call.message.answer('Подписка оформлена, спасибо!')

async def unsub(call: types.CallbackQuery):
    db.update_sub(call['from']['id'],'1','0')    
    await call.message.answer('Подписка отключена! Возвращайтесь к нам как можно скорее!')


# Проверка локации в бд и создание новой
async def location_checker(message: types.Message):
    if message.chat.type == 'private':

        status = db.check_location(message['from']['id'])
        # shabbat_list = []
        # print(status)
        if status:
            # print('+')
            request_shabbat_time = requests.get('https://www.hebcal.com/shabbat?cfg=json&geonameid='+str(status[5])+'M=on&leyning=off&lg=ru')
            shabbat_time = (request_shabbat_time.json())
            # for item in (shabbat_time['items']):
            #     shabbat_list.append(item['title'])
            #     start = shabbat_list[0]
            #     stop = shabbat_list[len(shabbat_list) - 1]


            for item in shabbat_time['items']:
                if "Зажигание свечей:" in item['title']:
                    start = item['title']
                    start_date = item['date'].split("T")[0].replace('-','/') 
                
                if "Авдала:" in item['title']:
                    stop = item['title'].replace('Авдала:', 'Авдала (исход Шаббата):')
                    stop_date = item['date'].split("T")[0].replace('-','/')      
                
            await message.answer(str(status[4]) + ' ' + str(status[3]) +'\n' + start + '\nДата: ' + start_date + '\n\n' + stop + '\nДата: ' + stop_date +'\n\nНаходитесь в другом месте? Обновите свою геолокацию \n/update', reply_markup=main_btn)
            await message.answer('Хотите получить инструкцию, как зажигать свечи или проводить Авдалу?', reply_markup=inl_bnt)    
        else:
            # print('-') 
            text = 'Тут Вы можете узнать время наступления Субботы (Шаббата) в Вашем городе. ' \
                    'Для определения местоположения нужно воспользоваться этой функцией на мобильном телефоне (с компьютера эта функция не работает).\n'\
                    'Пожалуйста, нажмите кнопку "Геолокация" в меню и дайте разрешение на отправку геоданных. '\
                    'Обратите внимание, точное время Шаббата доступно не для всех городов/сел, поэтому в результате поиска Вам может быть показано время Шаббата в ближайшем к Вам населенном пункте.\n'\
                    'Вернуться в главное меню? \nнажмите /start'   
            await message.answer(text, reply_markup=markup_request)
        db.stats(message['from']['id'], message['text'], message['date'])

# Обновление локации
async def location_update(message : types.Message):
    if message.chat.type == 'private':
        text =  'Пожалуйста, нажмите кнопку "Геолокация" в меню и дайте разрешение на отправку геоданных.\n' \
                'Обратите внимание, точное время Шаббата доступно не для всех городов/сел, поэтому в результате поиска Вам может быть показано время Шаббата в ближайшем к Вам населенном пункте.\n'\
                'Вернуться в главное меню? \nнажмите /start'
        await message.answer(text,reply_markup=markup_request)
        db.stats(message['from']['id'], message['text'], message['date'])



# Получение локации и отправка времени шаббата
async def handle_location(message: types.Message):
    if message.chat.type == 'private':
        lat = message.location.latitude
        lon = message.location.longitude
        # print(lat, lon)
        await message.delete()
        sb_times, geo = shabbat_times(lat,lon)
        await message.answer(str(geo.city) + ' ' + str(geo.country) +'\n' + str(sb_times.start) + '\nДата: ' +str(sb_times.start_date) + '\n\n' + str(sb_times.stop) + '\nДата: ' + str(sb_times.stop_date), reply_markup=main_btn)
        await message.answer('Хотите получить инструкцию, как зажигать свечи или проводить Авдалу?', reply_markup=inl_bnt)
        db.subscribers_to_db(message['from']['id'],message['from']['first_name'],message['from']['username'],geo.country, geo.city, geo.id, geo.latitude, geo.longitude)
        db.stats(message['from']['id'], message['text'], message['date'])


async def callback_shabbat_light(call: types.CallbackQuery):
    await call.message.answer(shabbat_light,  parse_mode='HTML')
    

async def callback_avdala(call: types.CallbackQuery):
    await call.message.answer(avdala , parse_mode='HTML')


def handlers_main(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    # dp.register_message_handler(subscribers, commands=['subscribe'])
    dp.register_message_handler(handle_location, content_types=['location'])
    
    dp.register_message_handler(location_checker, commands=['shabbat'])
    dp.register_message_handler(location_checker, Text(equals = 'Время Шаббата', ignore_case = True))
    
    dp.register_message_handler(location_update, commands=['update'])
    
    dp.register_message_handler(about_us, commands=['about'])
    dp.register_message_handler(about_us, Text(equals = 'О нас', ignore_case = True))

    dp.register_message_handler(subscribe_answer, commands=['subscribe_answer'])
    dp.register_message_handler(subscribe_answer, Text(equals = 'Подписаться на рассылку', ignore_case = True))
    # Инлайн кнопи и их коллбеки
    dp.register_callback_query_handler(callback_shabbat_light, text='shabbat_light_callbk')
    dp.register_callback_query_handler(callback_avdala, text='avdala_btn_callbk')

    dp.register_callback_query_handler(sub, text='sub')
    dp.register_callback_query_handler(unsub, text='unsub')
  