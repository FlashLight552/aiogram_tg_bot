from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo

from data.text import *
from data.config import HOST


# Наэкранные кнопки 

# Геолокация
markup_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Геолокация', request_location=True))


# Отмена
cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel = KeyboardButton('Отмена')
cancel_kb.add(cancel)


social_net_inl = InlineKeyboardMarkup()
social_net_inl_fb = InlineKeyboardButton(text='Facebook', url='https://www.facebook.com/KolelToraRu/')
social_net_inl_yt = InlineKeyboardButton(text='YouTube', url='https://www.youtube.com/KolelTora')
social_net_inl.add(social_net_inl_fb,social_net_inl_yt)

# update
update_inl = InlineKeyboardMarkup()
update_inl_btn = InlineKeyboardButton(text='Обновить геопозицию', callback_data='update')
update_inl.add(update_inl_btn)

# start
start_inl = InlineKeyboardMarkup()
start_inl_btn = InlineKeyboardButton(text='На главную', callback_data='start')
start_inl.add(start_inl_btn)

# Админ кнопки для выбора роли
adm_btn_ch = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin = KeyboardButton('Администратор')
moderator = KeyboardButton('Модератор')
adm_btn_ch.add(admin,moderator)



# Основной блок клавиш
main_btn = ReplyKeyboardMarkup(resize_keyboard=True)
about = KeyboardButton(about_us_cmd)
last_video = KeyboardButton(last_video_yt_cmd)
popular_video = KeyboardButton(popular_video_yt_cmd)
search_video = KeyboardButton(start_search_cmd)
hebcal_api = KeyboardButton(check_or_request_location_cmd)
feedback_btn = KeyboardButton(start_feedback_cmd)
subscribe = KeyboardButton(subscribe_answer_cmd)
hitas = KeyboardButton(hitas_cmd, web_app=WebAppInfo(url=f"{HOST}"))
date_conversion = KeyboardButton(date_conversion_cmd, web_app=WebAppInfo(url=f"{HOST}/conversion_start/"))
translate_btn =  KeyboardButton(translate_btn_cmd)
main_btn.add(hebcal_api, about, last_video, popular_video, search_video, hitas, date_conversion,translate_btn, feedback_btn,subscribe)


# Выбор языка
lang_btn = ReplyKeyboardMarkup(resize_keyboard=True)
lang_eng = KeyboardButton('English')
lang_ua = KeyboardButton('Ukrainian')
lang_ru = KeyboardButton('Russian')
lang_he = KeyboardButton('Hebrew')
lang_de = KeyboardButton('Deutsch')
lang_yi = KeyboardButton('Yiddish')
lang_btn.add(lang_eng, lang_ua, lang_he, lang_yi, lang_de, lang_ru, cancel)

translate_again_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(reply), KeyboardButton(go_start_cmd))


# админ блок клавиш 
adm_btn = ReplyKeyboardMarkup(resize_keyboard=True)
set_admin = KeyboardButton('Добавить админа')
del_admin = KeyboardButton('Удалить админа')
admins_list = KeyboardButton('Список адм')
sub_list = KeyboardButton('Список подсписчиков')
userid = KeyboardButton('ID пользователя')
feed_list = KeyboardButton('Список отзывов')
stats_list = KeyboardButton('Статистика')
active_list = KeyboardButton('Список активных')
spam = KeyboardButton('Рассылка(всем)')
ann_span = KeyboardButton('Рассылка(анонс)')

adm_btn.add(set_admin,del_admin,admins_list,sub_list,userid,feed_list,stats_list, active_list, spam, ann_span)



# inline
inl_bnt = InlineKeyboardMarkup(row_width=1)
shabbat_light = InlineKeyboardButton(text='Как зажечь субботние свечи?', callback_data='shabbat_light_callbk')
avdala = InlineKeyboardButton(text='Как провести Авдалу?', callback_data='avdala_btn_callbk')
# pesah_seder = InlineKeyboardButton(text='Как проводить пасхальный седер?', url='https://youtu.be/3Q-NeCrwnaA')
inl_bnt.add(shabbat_light, avdala)


# sub inline
sub_inl_bnt = InlineKeyboardMarkup()
sub_yt_last_video = InlineKeyboardButton(text='Подписаться', callback_data='sub')
unsub_yt_last_video = InlineKeyboardButton(text='Отписаться ', callback_data='unsub')
sub_inl_bnt.add(sub_yt_last_video, unsub_yt_last_video)

# annonce sub inline
annonce_sub_inl_bnt = InlineKeyboardMarkup()
sub_annonce = InlineKeyboardButton(text='Подписаться', callback_data='ann_sub')
unsub_annonce = InlineKeyboardButton(text='Отписаться ', callback_data='ann_unsub')
annonce_sub_inl_bnt.add(sub_annonce, unsub_annonce)


hebcal_inl = InlineKeyboardMarkup()
hebcal_shabbat_time = InlineKeyboardButton(text='Время Шаббата', callback_data='hebcal_shabbat_time')
hebcal_zmanim = InlineKeyboardButton(text='Зманим', callback_data='hebcal_zmanim')
hebcal_yahrzeit = InlineKeyboardButton(text='Yahrzeit', callback_data='hebcal_yahrzeit')
hebcal_inl.add(hebcal_shabbat_time,hebcal_zmanim,hebcal_yahrzeit, update_inl_btn, start_inl_btn)
