from bs4 import BeautifulSoup as bs
import requests


def hitas_text_post():
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
    tehillim = str(Hwrap_raw[1])[:-1061].replace(' Короля Мошиаха:', ':')
    tanya = str(Hwrap_raw[2])
    hayom_yom = str(Hwrap_raw[3])
    rambam = str(Hwrap_raw[4])
    moshiach = str(Hwrap_raw[5])

    fields = {
        'jew_data': hitasNavDay,
        'chumash': chumash,
        'tehillim': tehillim,
        'tanya': tanya,
        'hayom_yoma': hayom_yom,
        'rambam': rambam,
        'moshiach': moshiach,
    }

    requests.post('http://127.0.0.1:8000/api/hitas/', data=fields)