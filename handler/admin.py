from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

import json

from create_bot import telegram_bot
# from create_bot import dp
from utils.youtube import *
from utils.db_new import db
from keys import adm_btn, adm_btn_ch


# Класс состояний (FSM)
class Form(StatesGroup):
    id_user = State()
    role = State()
    memo = State()
    del_admin_id = State() 

# Старт добавление админа (FSM)
async def set_admin(message: types.Message):
    admins = db.show_all_from_table('admins')
    if message.chat.type == 'private':
        for item in admins:
            if message['from']['id'] == item[0]:
                if item[1] == 'owner' or item[1] == 'Администратор':
                    await message.answer('Введите ID пользователя \nДля отмены /cancel')
                    await Form.id_user.set() # Устанавливаем состояние
        

# Ввод ид юзера (FSM)
async def id_user(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['id_user'] = message.text
    await Form.role.set() # Переход состояния
    await message.answer('Роль пользователя.', reply_markup=adm_btn_ch)

# Выбор роли (FSM)
async def role (message: types.Message, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['role'] = message.text
    await message.answer('Введите коментарий для пользователя', reply_markup=adm_btn)
    await Form.memo.set()
  
# Коментарий для стафа (FSM)
async def memo (message: types.Message, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['memo'] = message.text
    await message.answer('Готово')
    await state.finish()   
    db.admins_to_db(proxy['id_user'], proxy['role'], proxy['memo'])
   


# Список админов
async def admins_list(message: types.Message):
    admins = db.show_all_from_table('admins')
    if message.chat.type == 'private':
        for item in admins:
            if message['from']['id'] == item[0]:
                with open('export/adm_list.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(admins, ensure_ascii=False))
                await message.answer_document(open('export/adm_list.json', 'rb'))
               

# Список подписчиков
async def subscribers_list(message: types.Message):
    admins = db.show_all_from_table('admins')
    if message.chat.type == 'private':
        for item in admins:
            if message['from']['id'] == item[0]:
                subs = db.show_all_from_table('subscribers')
                with open('export/subs_list.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(subs, ensure_ascii=False))
                await message.answer_document(open('export/subs_list.json', 'rb'))
              

# Отзывы
async def feedback_list(message: types.Message):
    admins = db.show_all_from_table('admins')
    if message.chat.type == 'private':
        for item in admins:
            if message['from']['id'] == item[0]:
                feedback = db.show_all_from_table('feedback')        
                with open('export/feedback_list.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(feedback, ensure_ascii=False))
                await message.answer_document(open('export/feedback_list.json', 'rb'))                
              

async def stats_list(message: types.Message):
    admins = db.show_all_from_table('admins')
    if message.chat.type == 'private':
        for item in admins:
            if message['from']['id'] == item[0]:
                stats = db.show_all_from_table('stats')        
                with open('export/stats_list.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(stats, ensure_ascii=False))
                await message.answer_document(open('export/stats_list.json', 'rb'))                
               

async def drop_and_add(message: types.Message):
    admins = db.show_all_from_table('admins')
    if message.chat.type == 'private':
        for item in admins:
            if message['from']['id'] == item[0]:
                db.drop_table_and_create()           

async def sub_active_list(message: types.Message):
    admins = db.show_all_from_table('admins')
    if message.chat.type == 'private':
        for item in admins:
            if message['from']['id'] == item[0]:
                active_sub = db.show_all_from_table('active_sub')
                active_sub.insert(0, '["ID","Активен","Подписка на видео","Подписка на анонсы"]')        
                with open('export/active_sub.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(active_sub, ensure_ascii=False))
                await message.answer_document(open('export/active_sub.json', 'rb'))                


# Удалить админа (FSM)
async def del_admin(message: types.Message):
    admins = db.show_all_from_table('admins')
    if message.chat.type == 'private':
        for item in admins:
            if message['from']['id'] == item[0]:
                if item[1] == 'owner' or item[1] == 'Администратор':
                    await message.answer('Введите ID для удаления \nДля отмены /cancel')
                    await Form.del_admin_id.set() # Устанавливаем состояние
                    

# Удалить админа. Ввод ид (FSM)
async def del_id_user(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy: # Устанавливаем состояние ожидания
        proxy['id_user'] = message.text
    await state.finish() # Переход состояния
    db.adm_del_from_db(proxy['id_user'])
    await message.answer('Готово')

# Получение ид тг юзера
async def get_id_user(message: types.Message):
    if message.chat.type == 'private':
        await message.answer('Ваш ID: ' + str(message['from']['id']))


async def get_adm_btn(message: types.Message):
    admins = db.show_all_from_table('admins')
    if message.chat.type == 'private':
        for item in admins:
            if message['from']['id'] == item[0]:
                await message.answer('Адм панель', reply_markup=adm_btn)


def admin(dp: Dispatcher):
    # Начало
    dp.register_message_handler(set_admin, commands=['set_admin'])
    dp.register_message_handler(set_admin, Text(equals = 'Добавить админа', ignore_case = True))
    
    dp.register_message_handler(del_admin, commands=['del_admin'])
    dp.register_message_handler(del_admin, Text(equals = 'Удалить админа', ignore_case = True))
    # Рега стафа
    dp.register_message_handler(id_user, state=Form.id_user)
    dp.register_message_handler(role, state=Form.role)
    dp.register_message_handler(memo, state=Form.memo)
    #Удаление стафа
    dp.register_message_handler(del_id_user, state=Form.del_admin_id)
    # Остальные адм команды
    dp.register_message_handler(admins_list, commands=['admins_list'])
    dp.register_message_handler(admins_list, Text(equals = 'Список адм', ignore_case = True))
    dp.register_message_handler(subscribers_list, commands=['sub_list'])
    dp.register_message_handler(subscribers_list, Text(equals = 'Список подсписчиков', ignore_case = True))
    # Отзывы
    dp.register_message_handler(feedback_list, commands=['feedback_list'])
    dp.register_message_handler(feedback_list, Text(equals = 'Список отзывов', ignore_case = True))
    # Статистика
    dp.register_message_handler(stats_list, commands=['stats_list'])
    dp.register_message_handler(stats_list, Text(equals = 'Статистика', ignore_case = True))
    # ид пользователя
    dp.register_message_handler(get_id_user, commands=['userid'])
    dp.register_message_handler(get_id_user, Text(equals = 'ID пользователя', ignore_case = True))

    dp.register_message_handler(sub_active_list, commands=['sub_active_list'])
    dp.register_message_handler(sub_active_list, Text(equals = 'Список активных', ignore_case = True))


    # Админ панель
    dp.register_message_handler(get_adm_btn, commands=['adm'])
    dp.register_message_handler(drop_and_add, commands=['drop_and_add'])

