from geopy.geocoders import Nominatim
import json
import requests

from utils.db_new import db

def get_geo_user(latitude,longitude, message_user_id, message_first_name, message_username):
    class geo:
        city = ''
        country = ''
        country_code = ''
        state = ''
        id = ''
        latitude = ''
        longitude = ''
    

    geo.latitude = latitude
    geo.longitude = longitude
    
    
    # class shabbat:
    #     start = ''
    #     stop = ''
    #     start_date = ''
    #     stop_date = ''
    shabbat_list = []


    geolocator = Nominatim(user_agent="shabbat_time_api")
    location = geolocator.reverse(str(latitude)+','+str(longitude), language='en')


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

                db.subscribers_to_db(message_user_id,message_first_name,message_username,geo.country, geo.city, geo.id, geo.latitude, geo.longitude)
                break

        
    # for item in true_shabbat_time['items']:
    #     if "Зажигание свечей:" in item['title']:
    #         shabbat.start = item['title']
    #         shabbat.start_date = item['date'].split("T")[0].replace('-','/') 
          
    #     if "Авдала:" in item['title']:
    #         shabbat.stop = item['title'].replace('Авдала:', 'Авдала (исход Шаббата):')
    #         shabbat.stop_date = item['date'].split("T")[0].replace('-','/')  

    # return(shabbat, geo)
