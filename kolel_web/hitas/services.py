from bs4 import BeautifulSoup as bs
from datetime import datetime
import requests


def hitas_text():
    url = 'https://moshiach.ru/chitas.php'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
    page = requests.get(url, headers = headers)
    soup = bs(page.text, 'lxml')

    hitasNavDay = soup.find('h4', class_='hitasNavDay')
    Hwrap_raw = soup.find_all('div', class_='Hwrap')

    hitasNavDay = str(hitasNavDay).replace('/', '.',2)

    chumash = str(Hwrap_raw[0]).replace('chumash Hwrap', 'Hwrap')
    tehillim = str(Hwrap_raw[1])[:-1061]
    tanya = str(Hwrap_raw[2])
    hayom_yom = str(Hwrap_raw[3])
    rambam = str(Hwrap_raw[4])
    moshiach = str(Hwrap_raw[5])

    list = [hitasNavDay, chumash, tehillim, tanya, hayom_yom, rambam, moshiach]

    return(list)


def hebrew_data():
    date = (datetime.today().strftime('%Y-%m-%d')).split('-')
    url = f'https://www.hebcal.com/converter?cfg=json&date={date[0]}-{date[1]}-{date[2]}&g2h=1&strict=1'
    request = requests.get(url).json()
    d = request['hd']
    m = request['hm']
    y = request['hy']
    return(d,m,y)