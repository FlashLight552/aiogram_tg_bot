import os
from shazamio import Shazam
from youtube_search import YoutubeSearch

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from create_bot import telegram_bot


async def voice_message(message:types.message, state: FSMContext):
        file_id = message.voice.file_id
        file = await telegram_bot.get_file(file_id)
        file_path = file.file_path
        download_path = f'export/{file.file_id}.oga'
        await telegram_bot.download_file(file_path, download_path)

        shazam = Shazam()
        out = await shazam.recognize_song(download_path)

        lyrics = ''
        try: 
            title = out['track']['title']
            subtitle = out['track']['subtitle']
            images = out['track']['images']['coverart']
            try:
                for item in out['track']['sections']:
                    if item['type'] == 'LYRICS':
                        for text in item['text']:
                            lyrics += f'{text}\n'
            except:
                lyrics = 'empty'
        
            result = YoutubeSearch(f'{subtitle} {title}', max_results=1).to_dict()
            for item in result:
                id = item['id']
                yt_url = f'https://www.youtube.com/watch?v={id}'
        except:
            subtitle = title = images = yt_url = lyrics = 'empty'

        if subtitle != 'empty':
            async with state.proxy() as proxy:
                proxy['lyrics'] = lyrics
            if lyrics != 'empty':
                await message.answer_photo(images, caption=f'{subtitle} {title}', reply_markup=InlineKeyboardMarkup().add(
                                                                    InlineKeyboardButton(text='Youtube', url=yt_url),
                                                                    InlineKeyboardButton(text='Lyrics', callback_data='lyrics')))
            else:
                await message.answer_photo(images, caption=f'{subtitle} {title}', reply_markup=InlineKeyboardMarkup().add(
                                                                    InlineKeyboardButton(text='Youtube', url=yt_url)))

        else:
            await message.answer('Увы, ничего не найдено, попробуйте еще раз.')
        
        os.remove(download_path)

async def lyrics(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
       lyrics = proxy['lyrics']
    await call.message.answer(lyrics)


def handlers_shazam(dp: Dispatcher):
    dp.register_message_handler(voice_message, content_types=['voice']) 
    dp.register_callback_query_handler(lyrics, text='lyrics') 
        
        

