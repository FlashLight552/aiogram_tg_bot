from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup



# Наэкранные кнопки 

# Геолокация
markup_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Геолокация', request_location=True))

# Админ кнопки для выбора роли
adm_btn_ch = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin = KeyboardButton('Администратор')
moderator = KeyboardButton('Модератор')
adm_btn_ch.add(admin,moderator)



# Основной блок клавиш
main_btn = ReplyKeyboardMarkup(resize_keyboard=True)
about = KeyboardButton('О нас')
last_video = KeyboardButton('Новые уроки Торы')
popular_video = KeyboardButton('Популярные уроки')
search_video = KeyboardButton('Поиск уроков')
shabbat = KeyboardButton('Время Шаббата')
feedback_btn = KeyboardButton('Отзыв')
subscribe = KeyboardButton('Подписаться на рассылку')
main_btn.add(shabbat, about, last_video, popular_video, search_video, feedback_btn,subscribe)



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
pesah_seder = InlineKeyboardButton(text='Как проводить пасхальный седер?', url='https://youtu.be/3Q-NeCrwnaA')
inl_bnt.add(shabbat_light, avdala, pesah_seder)


# sub inline
sub_inl_bnt = InlineKeyboardMarkup()
sub = InlineKeyboardButton(text='Подписаться', callback_data='sub')
unsub = InlineKeyboardButton(text='Отписаться ', callback_data='unsub')
sub_inl_bnt.add(sub, unsub)

# annonce sub inline
annonce_sub_inl_bnt = InlineKeyboardMarkup()
ann_sub = InlineKeyboardButton(text='Подписаться', callback_data='ann_sub')
ann_unsub = InlineKeyboardButton(text='Отписаться ', callback_data='ann_unsub')
annonce_sub_inl_bnt.add(ann_sub, ann_unsub)


