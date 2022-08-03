from utils.wrappers import log
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from data.text import *
from utils.youtube import *
from utils.db_new import db
from utils.geo import get_geo_user
from keys import *
from data.text import *
import requests

from datetime import datetime


def shabbat_time_request(user_id):
    status = db.check_location(user_id)
    if status[5] != '-':
        request_shabbat_time = requests.get(
            'https://www.hebcal.com/shabbat?cfg=json&geonameid='+str(status[5])+'M=on&leyning=off&lg=ru')
        text = str(status[4]) + ' ' + str(status[3]) + '\n\n'

    else:
        lat = str(status[6])
        lon = str(status[7])
        request_shabbat_time = requests.get(
            f'https://www.hebcal.com/shabbat?cfg=json&latitude={lat}&longitude={lon}&M=on&leyning=off&lg=ru')
        text = request_shabbat_time.json()['location']['tzid'] + '\n\n'

    shabbat_time = (request_shabbat_time.json())

    for item in shabbat_time['items']:
        if item['category'] == 'parashat':
            text += item['title'] + '\n\n'

    for item in shabbat_time['items']:
        if item['category'] == 'candles' or item['category'] == 'zmanim' or item['category'] == 'havdalah' or item['category'] == 'holiday':
            title = item['title']
            date = datetime.fromisoformat(item['date']).date()
            time = datetime.fromisoformat(item['date']).time()
            if str(time) == '00:00:00':
                time = ''
            if "Авдала:" in title:
                title = title.replace('Авдала:', 'Авдала (исход Шаббата):')

            text = text + title + '\nДата: ' + \
                str(date) + ' ' + str(time).replace(':00', '', 1) + '\n\n'
    return(text)


def zmanim(user_id):
    status = db.check_location(user_id)
    if status[5] != '-':
        request_zmanim_time = requests.get(
            'https://www.hebcal.com/zmanim?cfg=json&geonameid='+str(status[5]))
        location_name = str(status[4]) + ' ' + str(status[3]) + '\n\n'

    else:
        lat = str(status[6])
        lon = str(status[7])
        request_zmanim_time = requests.get(
            f'https://www.hebcal.com/zmanim?cfg=json&latitude={lat}&longitude={lon}')
        location_name = request_zmanim_time.json()['location']['tzid'] + '\n\n'

    zmanim = (request_zmanim_time.json())

    title_list = {
        'chatzotNight': 'Midnight – Chatzot',
        'alotHaShachar': 'Dawn – Alot haShachar',
        'misheyakir': 'Earliest talis & tefillin – Misheyakir',
        'misheyakirMachmir': 'Earliest talis & tefillin – Misheyakir Machmir',
        'dawn': 'Civil dawn', 
        'sunrise': 'Sunrise',
        'sofZmanShma': 'Latest Shema (Gra)',
        'sofZmanShmaMGA': 'Latest Shema (MGA)',
        'sofZmanTfilla': 'Latest Shacharit (Gra)',
        'sofZmanTfillaMGA': 'Latest Shacharit (MGA)',
        'chatzot': 'Midday – Chatzot',
        'minchaGedola': 'Earliest Mincha – Mincha Gedola',
        'minchaKetana': 'Preferable earliest time to recite Minchah – Mincha Ketana',
        'plagHaMincha': 'Plag haMincha',
        'sunset': 'Sunset', 
        'dusk': 'Civil dusk',
        'tzeit7083deg': 'Nightfall (3 medium stars) – Tzeit 7.083°',
        'tzeit85deg': 'Nightfall (3 small stars) – Tzeit 8.5°',
        'tzeit42min': 'Nightfall (3 medium stars) – Tzeit 42 minutes',
        'tzeit50min': 'Nightfall (3 small stars) – Tzeit 50 minutes',
        'tzeit72min': 'Nightfall (Rabbeinu Tam) – Tzeit 72 minutes'
        }
    results = ''

    for item in zmanim['times']:
        if item in title_list:
            title = title_list[item]
            time = str(datetime.fromisoformat(
                zmanim['times'][item]).time()).replace(':00', '', 1)
            results += f'{title} - {time}\n'
    return (location_name, results)


async def location_update_btn(call: types.CallbackQuery):
    if call.message.chat.type == 'private':
        await call.message.answer(location_update_text, reply_markup=markup_request)
        await call.message.answer(back_to_main_text_answer, reply_markup=start_inl, disable_notification=True)

        db.stats(call.message['from']['id'],
                 'Обновление геолокации', call.message['date'])


async def check_or_request_location(message: types.Message):
    if message.chat.type == 'private':
        status = db.check_location(message.from_user.id)
        if status:
            await message.answer(location_add_to_db_text, reply_markup=hebcal_inl, disable_notification=True)
        else:
            await message.answer(shabbat_text, reply_markup=markup_request, disable_notification=True)
            await message.answer(back_to_main_text_answer, reply_markup=start_inl, disable_notification=True)

    db.stats(message['from']['id'], message['text'], message['date'])


async def location_add_to_db(message: types.Message):
    get_geo_user(message.location.latitude, message.location.longitude,
                 message.from_user.id, message.from_user.first_name, message.from_user.username)
    await message.answer(location_add_to_db_text, reply_markup=hebcal_inl, disable_notification=True)
    await message.delete()


async def callback_shabbat_time(call: types.CallbackQuery):
    text = shabbat_time_request(call.from_user.id)
    await call.message.answer(text, reply_markup=main_btn, disable_notification=True)
    await call.message.answer(geo_update_text, reply_markup=update_inl, disable_notification=True)
    await call.message.answer(get_instructions_answer, reply_markup=inl_bnt, disable_notification=True)

    db.stats(call.message['from']['id'], 'Вермя шаббата', call.message['date'])


async def callback_zmanim(call: types.CallbackQuery):
    location, text = zmanim(call.from_user.id)
    await call.message.answer(f'{location}{text}', reply_markup=main_btn, disable_notification=True)
    await call.message.answer(geo_update_text, reply_markup=update_inl, disable_notification=True)

    db.stats(call.message['from']['id'], 'Зманим', call.message['date'])


async def callback_yahrzeit(call: types.CallbackQuery):
    await call.message.answer('coming soon "callback_yahrzeit"')


async def callback_shabbat_light(call: types.CallbackQuery):
    await call.message.answer(shabbat_light,  parse_mode='HTML', disable_notification=True)

    db.stats(call.message['from']['id'], 'Как зажечь субботние свечи?', call.message['date'])


async def callback_avdala(call: types.CallbackQuery):
    await call.message.answer(avdala, parse_mode='HTML', disable_notification=True)

    db.stats(call.message['from']['id'], 'Как провести Авдалу?', call.message['date'])


def handlers_shabbat_time(dp: Dispatcher):
    dp.register_message_handler(location_add_to_db, content_types=['location'])
    dp.register_message_handler(check_or_request_location, Text(equals=check_or_request_location_cmd, ignore_case=True))
    dp.register_callback_query_handler(callback_shabbat_light, text='shabbat_light_callbk')
    dp.register_callback_query_handler(callback_avdala, text='avdala_btn_callbk')
    dp.register_callback_query_handler(location_update_btn, text='update')
    dp.register_callback_query_handler(callback_shabbat_time, text='hebcal_shabbat_time')
    dp.register_callback_query_handler(callback_zmanim, text='hebcal_zmanim')
    dp.register_callback_query_handler(callback_yahrzeit, text='hebcal_yahrzeit')
