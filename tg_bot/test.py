import requests
from datetime import datetime

request_zmanim = requests.get('https://www.hebcal.com/zmanim?cfg=json&geonameid=706448')
zmanim = (request_zmanim.json())
title_list = {'chatzotNight':'Хацот алайла(Полночь)', 'alotHaShachar':'Аллот Ашахар (Рассвет)', 'misheyakir':'Мишейакир (Самое раннее время надевания талита и тфилин)', 
                'misheyakirMachmir':'misheyakirMachmir', 'dawn':'рассвет', 'sunrise':'восход', 'sofZmanShma':'Соф Зман Шма (самое позднее время чтения Шма)', 
                'sofZmanShmaMGA':'sofZmanShmaMGA', 'sofZmanTfilla':'Соф Зман Тфила (Самое позднее время для Шахарит', 'sofZmanTfillaMGA':'sofZmanTfillaMGA', 
                'chatzot':'Хацот айом (Полдень)', 'minchaGedola':'Минха гдола (Самое раннее время Минхи)', 'minchaKetana':'Минха ктана (Малая минха)', 
                'plagHaMincha':'Плаг аминха (Полу-минха)', 'sunset':'закат', 'dusk':'сумерки', 'tzeit7083deg':'tzeit7083deg', 'tzeit85deg':'tzeit85deg', 'tzeit42min':'tzeit42min', 
                'tzeit50min':'tzeit50min', 'tzeit72min':'tzeit72min'}        

results = ''

for item in zmanim['times']:
    if item in title_list:
        title = title_list[item]
        time = str(datetime.fromisoformat(zmanim['times'][item]).time()).replace(':00','',1)
        results += f'{title} {time}\n'

print (results)



