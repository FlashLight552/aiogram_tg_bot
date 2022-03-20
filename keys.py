from re import search
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


# Наэкранные кнопки 

# Геолокация
markup_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Геолокация', request_location=True))

# Админ кнопки для выбора роли
adm_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin = KeyboardButton('Администратор')
moderator = KeyboardButton('Модератор')
adm_btn.add(admin,moderator)



# Основной блок клавиш
main_btn = ReplyKeyboardMarkup(resize_keyboard=True)
about = KeyboardButton('О нас')
last_video = KeyboardButton('Последние видео')
popular_video = KeyboardButton('Популярные видео')
search_video = KeyboardButton('Поиск')
shabbat = KeyboardButton('Зажигание свечей')
main_btn.add(about, last_video, popular_video, search_video, shabbat)



# админ блок клавиш 
adm_btn = ReplyKeyboardMarkup(resize_keyboard=True)
set_admin = KeyboardButton('Добавить админа')
del_admin = KeyboardButton('Удалить админа')
admins_list = KeyboardButton('Список адм')
sub_list = KeyboardButton('Список подсписчиков')
userid = KeyboardButton('ID пользователя')
adm_btn.add(set_admin,del_admin,admins_list,sub_list,userid)





