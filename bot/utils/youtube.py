from googleapiclient.discovery import build
from data.config import yt_token
from youtube_search import YoutubeSearch
from data.config import yt_channel_name


# Поиск по названию
def search_pars(name):
    results = YoutubeSearch(yt_channel_name + ' - ' + name, max_results=10).to_dict()
    # results = YoutubeSearch(name, max_results=1000).to_dict()
    url_list = []
    title_list = []

    for item in results:
        if item['channel'] == yt_channel_name:
            # print (item)
            url_list.append('https://www.youtube.com/watch?v='+item['id'])
            title_list.append(item['title'])
    return(url_list, title_list)


# Топ по популярности
def youtube_popular(channelId,maxResults, order):
    youtube = build('youtube', 'v3', developerKey=yt_token, cache_discovery=False)
    request = youtube.search().list(
        part='snippet',
        channelId = channelId,
        maxResults = maxResults,
        order = order
        )
    url_list = []
    title_list = [] 
    # description_list = []
    response = request.execute()
    # print(response['items'])
    for item in response['items']:
        url_list.append('https://www.youtube.com/watch?v='+item['id']['videoId'])
        title_list.append(item['snippet']['title'])
        # description_list.append(['description']) 
    return(url_list, title_list)


# Последнее видео на канале
def youtube_last(channelId,maxResults):
    youtube = build('youtube', 'v3', developerKey=yt_token, cache_discovery=False)
    request = youtube.activities().list(
        part='contentDetails, snippet',
        channelId = channelId,
        maxResults = maxResults,
        )
    url_list = []
    title_list = [] 
    response = request.execute()
    for item in response['items']:
        url_list.append('https://www.youtube.com/watch?v='+item['contentDetails']['upload']['videoId'])
        title_list.append(item['snippet']['title'])
    return(url_list, title_list)

