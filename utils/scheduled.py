from datetime import datetime
import asyncio
from aiogram.utils.markdown import hlink
import html
from time import sleep


from utils.youtube import youtube_last, youtube_popular
from data.config import yt_channel_id
from utils.db import youtube_video, youtube_video_search_url, subscribers_id_list
from data.config import yt_last_video_count, yt_popular_video_count
from create_bot import telegram_bot





# Функция по таймеру последние видео
async def scheduled_last_video(wait_for):
  while True:
    try:
        await asyncio.sleep(wait_for) 
        url, title = youtube_last(yt_channel_id, yt_last_video_count)  
        for i in reversed(range(0, len(url))):
            today = datetime.now()
            data = today.strftime("%d/%m/%Y %H:%M:%S:%f")

            check_new_video = youtube_video_search_url(url[i])
            if not check_new_video:
                # print('Новое видео!')
                # print(url[i], title[i])
                hyperlink = '<a href="'+url[i]+'">'+title[i]+'</a>'
                # print(hyperlink)
                
                sub_list = subscribers_id_list()
                for item in sub_list:
                    await telegram_bot.send_message(item[0], 'Новое видео!\n'+hyperlink, parse_mode='HTML')   

            youtube_video(url[i], title[i],'last_video', str(data))
        # print('Работаю!')      
    except:
        pass 

# Функция по таймеру последние видео
async def scheduled_popular_video(wait_for):
  while True:
    try:
        url, title = youtube_popular(yt_channel_id, yt_popular_video_count, 'viewCount')  
        for i in reversed(range(0, len(url))):
            today = datetime.now()
            data = today.strftime("%d/%m/%Y %H:%M:%S:%f")
            youtube_video(url[i], html.unescape(title[i]),'popular_video', str(data))
            # print(url[i], html.unescape(title[i]))
        await asyncio.sleep(wait_for)    
    except:
        pass         