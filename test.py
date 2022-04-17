import requests
from datetime import datetime

request_zmanim = requests.get('https://www.hebcal.com/zmanim?cfg=json&geonameid=706448')
zmanim = (request_zmanim.json())
title = []
title_ru = ['Хацот алайла(Полночь)','Аллот Ашахар (Рассвет)','Мишейакир (Самое раннее время надевания талита и тфилин)','misheyakirMachmir','рассвет','восход',\
    'Соф Зман Шма (самое позднее время чтения Шма)','sofZmanShmaMGA','Соф Зман Тфила (Самое позднее время для Шахарит)','sofZmanTfillaMGA','Хацот айом (Полдень)',\
        'Минха гдола (Самое раннее время Минхи)','Минха ктана (Малая минха)','Плаг аминха (Полу-минха)','закат','сумерки','Цейс (выход звезд)']
title_eng = ['chatzotNight','alotHaShachar','misheyakir','misheyakirMachmir','dawn','sunrise','sofZmanShma','sofZmanShmaMGA','sofZmanTfilla','sofZmanTfillaMGA',\
            'chatzot','minchaGedola','minchaKetana','plagHaMincha','sunset','dusk','tzeit']        

for item in zmanim['times']:
    title.append(item)

for i in range(0, len(title)):
    if title[i] in title_eng:
        time_name_ru = title_ru[i]
        time_name_eng = title_eng[i]
        time = str(datetime.fromisoformat(zmanim['times'][title[i]]).time()).replace(':00','',1)
        print (time_name_ru +' = '+ time_name_eng +': '+ time)



'''
chatzotNight	    Хацот алайла(Полночь)
alotHaShachar	    Аллот Ашахар (Рассвет)
misheyakir	        Мишейакир (Самое раннее время надевания талита и тфилин)
misheyakirMachmir	
dawn	            рассвет
sunrise	            восход
sofZmanShma	        Соф Зман Шма (самое позднее время чтения Шма)
sofZmanShmaMGA	
sofZmanTfilla	    Соф Зман Тфила (Самое позднее время для Шахарит
sofZmanTfillaMGA	
chatzot	            Хацот айом (Полдень)
minchaGedola	    Минха гдола (Самое раннее время Минхи)
minchaKetana	    Минха ктана (Малая минха)
plagHaMincha	    Плаг аминха (Полу-минха)
sunset	            закат
dusk	            сумерки
tzeit	            Цейс (выход звезд)
'''