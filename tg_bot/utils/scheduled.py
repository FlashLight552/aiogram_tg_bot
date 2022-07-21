from datetime import datetime
import asyncio
from aiogram.utils.markdown import hlink
import html
from time import sleep


from utils.youtube import youtube_last, youtube_popular
from data.config import yt_channel_id
# from utils.db import youtube_video, youtube_video_search_url, subscribers_id_list
from utils.db_new import db
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
            check_new_video = db.youtube_video_search_url(url[i])
            if not check_new_video:
                hyperlink = '<a href="'+url[i]+'">'+title[i]+'</a>'
                sub_list = db.sub_spam_allow('1')
                for item in sub_list:
                    try:
                        await telegram_bot.send_message(item[0], 'Новое видео!\n'+hyperlink, parse_mode='HTML')   
                    except: 
                        db.update_sub_allow_spam(item[0],'0','0')
            db.youtube_video_to_db(url[i], title[i],'last_video', str(data))
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
            db.youtube_video_to_db(url[i], html.unescape(title[i]),'popular_video', str(data))
        await asyncio.sleep(wait_for)    
    except:
        pass         