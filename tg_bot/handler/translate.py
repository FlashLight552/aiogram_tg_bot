from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from googletrans import Translator

from data.text import *
from keys import *

# Класс состояний
class Form(StatesGroup):
    get_phrase = State()
    get_language = State()

async def start_translate(message: types.Message):
    await message.answer(translate_btn_text, reply_markup=cancel_kb, disable_notification=True)
    await Form.get_phrase.set()


async def language_select(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy: 
        proxy['phrase'] = message.text
    await message.answer('На какой язык перевести?', reply_markup=lang_btn)
    await Form.get_language.set()


async def finish_translate(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['language'] = message.text
    await state.finish() 

    lang_list = {lang_eng_caption:'en', lang_ua_caption:'uk', lang_ru_caption:'ru', lang_he_caption:'iw', lang_de_caption:'de', lang_yi_caption:'yi'}
    for item in lang_list.items():
        if proxy['language'] in item:
            lang_code = item[1]
    
    translator = Translator()
    detect_lang = translator.detect(proxy['phrase'])
    translated_text = translator.translate(text= proxy['phrase'], src=detect_lang.lang, dest=lang_code)
    await message.answer(translated_text.text, reply_markup=translate_again_btn)


async def go_start(message: types.message):
    await message.answer(welcome_text, reply_markup=main_btn, disable_notification=True)


def handlers_translate(dp: Dispatcher):
    dp.register_message_handler(start_translate, commands=['translate'])
    dp.register_message_handler(start_translate, Text(equals=[translate_btn_cmd, reply], ignore_case=True))

    dp.register_message_handler(language_select, state=Form.get_phrase)
    dp.register_message_handler(finish_translate, state=Form.get_language)

    dp.register_message_handler(go_start, Text(equals=go_start_cmd, ignore_case=True))