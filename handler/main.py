from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from utils.youtube import *
from utils.db import *
from aiogram.utils.markdown import hlink
from utils.geo import shabbat_times
from keys import *
import requests



# Команда старт и вывод наэкранных кнопок 
async def send_welcome(message: types.Message):
    if message.chat.type == 'private':
        #await message.delete()
        photo = open('img\pig.jpg', 'rb')
        await message.answer_photo(photo, caption='Доброго вечора, ми з України!', reply_markup=main_btn)
        subscribers_create_table()
        check_list = subscribers_search_by_id(message['from']['id'])

        if not check_list :
            # print ('Добавил новую, ', check_list)
            subscribers(message['from']['id'],message['from']['first_name'],message['from']['username'])
        # else: print ('Не добавил новую, ', check_list)
# О нас
async def about_us(message: types.Message):
    await message.answer('***Информация о нас***')

# #Оформление пожписки и запись в бд
# async def subscribers(message: types.Message):
#     await message.answer(subscribe(message['from']['id'],message['from']['first_name'],message['from']['username']))



# Проверка локации в бд и создание новой
async def location_checker(message: types.Message):
    if message.chat.type == 'private':
        status = check_location(message['from']['id'])
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
                    stop = item['title']
                    stop_date = item['date'].split("T")[0].replace('-','/')      
                
            await message.answer(str(status[4]) + ' ' + str(status[3]) +'\n' + start + '\nДата: ' + start_date + '\n' + stop + '\nДата: ' + stop_date +'\nДля обновления герлокации \n/update', reply_markup=main_btn)    
        else:
            # print('-')    
            await message.answer('Ваша геолокация еще не опеределена. Только для мобильных устройст. \nДля вызова кнопочного меню /start', reply_markup=markup_request)
    # print(shabbat_list)
# Обновление локации
async def location_update(message : types.Message):
    if message.chat.type == 'private':
        await message.answer('Для обновления нажмите кнопку ниже. Только для мобильных устройств.\nДля вызова кнопочного меню /start',reply_markup=markup_request)



# Получение локации и отправка времени шаббата
async def handle_location(message: types.Message):
    if message.chat.type == 'private':
        lat = message.location.latitude
        lon = message.location.longitude
        # print(lat, lon)
        await message.delete()
        sb_times, geo = shabbat_times(lat,lon)
        await message.answer(str(geo.city) + ' ' + str(geo.country) +'\n' + str(sb_times.start) + '\nДата: ' +str(sb_times.start_date) + '\n' + str(sb_times.stop) + '\nДата: ' + str(sb_times.stop_date), reply_markup=main_btn)
        subscribers(message['from']['id'],message['from']['first_name'],message['from']['username'],geo.country, geo.city, geo.id, geo.latitude, geo.longitude)






def handlers_main(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    # dp.register_message_handler(subscribers, commands=['subscribe'])
    dp.register_message_handler(handle_location, content_types=['location'])
    
    dp.register_message_handler(location_checker, commands=['shabbat'])
    dp.register_message_handler(location_checker, Text(equals = 'Зажигание свечей', ignore_case = True))
    
    dp.register_message_handler(location_update, commands=['update'])
    
    
    dp.register_message_handler(about_us, commands=['about'])
    dp.register_message_handler(about_us, Text(equals = 'О нас', ignore_case = True))