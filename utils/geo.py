
from geopy.geocoders import Nominatim
import json
import requests


def shabbat_times(latitude,longitude):
    class geo:
        city = ''
        country = ''
        country_code = ''
        state = ''
        # latitude = latitude
        # longitude = longitude
        id = ''
        latitude = ''
        longitude = ''
    
    geo.latitude = latitude
    geo.longitude = longitude
    
    
    class shabbat:
        start = ''
        stop = ''
        start_date = ''
        stop_date = ''
    shabbat_list = []

    geolocator = Nominatim(user_agent="shabbat_time_api")
    location = geolocator.reverse(str(latitude)+','+str(longitude), language='en')

    # print(location.raw)
    geo.city = location.raw['address']['city']
    geo.country = location.raw['address']['country']
    geo.country_code = location.raw['address']['country_code']
    geo.state = location.raw['address']['state']


    f = open('./data/cities.json')
    data = json.load(f)


    for item in data[geo.city]:
        geo.id = item['id']
        request_shabbat_time = requests.get('https://www.hebcal.com/shabbat?cfg=json&geonameid='+str(geo.id)+'M=on&leyning=off&lg=ru')
        shabbat_time = (request_shabbat_time.json())
        
        
        lat = shabbat_time['location']['latitude']
        lon = shabbat_time['location']['longitude']
        
        
        if (int(lat) <= int(latitude) + 0.6) and (int(lat) >= int(latitude - 0.6)):
            if (int(lon) <= int(longitude) + 0.6) and (int(lon) >= int(longitude - 0.6)):
                # print('Координаты совпали!')
                true_shabbat_time = shabbat_time
                break
        # else:
        #     print('Координаты не совпали!')
    
    
    # print(shabbat_time)
    # for item in (true_shabbat_time['items']):
    #     shabbat_list.append(item['title'])

        
    for item in true_shabbat_time['items']:
        if "Зажигание свечей:" in item['title']:
            shabbat.start = item['title']
            shabbat.start_date = item['date'].split("T")[0].replace('-','/') 
            # print(shabbat.start, shabbat.start_date)
        if "Авдала:" in item['title']:
            shabbat.stop = item['title']
            shabbat.stop_date = item['date'].split("T")[0].replace('-','/')  
            # print(shabbat.stop, shabbat.stop)
    return(shabbat, geo)
# print (shabbat.start)
# print (shabbat.stop)