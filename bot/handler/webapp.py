from aiogram import types, Dispatcher
import requests

async def web_app_mess(message: types.message):
    await message.delete()
    date = str(message.web_app_data.data).split('-')
    mounth_name = {
    "Nisan": "Нисан",
    "Iyyar": "Ияр",
    "Sivan": "Сиван",
    "Tamuz": "Тамуз",
    "Av": "Ав",
    "Elul": "Элул",
    "Tishrei": "Тишрей",
    "Cheshvan": "Хешван",
    "Kislev": "Кислев",
    "Tevet": "Тевет",
    "Sh'vat": "Шват",
    "Adar": "Адар",
    "Adar I": "Адар I",
    "Adar II": "Адар II",
    }
    if date[0] == 'gregorian':
        date[4] = str(date[4]).replace('true','on')
        url = f'https://www.hebcal.com/converter?cfg=json&date={date[3]}-{date[2]}-{date[1]}&g2h=1&strict=1&gs={date[4]}'
        request = requests.get(url).json()
        for item in mounth_name.keys():
            if item == request['hm']:
                hm =  mounth_name[item]
        await message.answer("Григорианская дата:\n"\
                        f"{request['gd']}/{request['gm']}/{request['gy']}\n"\
                        "Еврейская дата:\n"\
                        f"{request['hd']} {hm} {request['hy']}")

    if date[0] == 'hebrew':
        url = f'https://www.hebcal.com/converter?cfg=json&hy={date[3]}&hm={date[2]}&hd={date[1]}&h2g=1&strict=1'
        request = requests.get(url).json()
        for item in mounth_name.keys():
            if item == request['hm']:
                hm =  mounth_name[item]
        await message.answer("Еврейская дата:\n"\
                        f"{request['hd']} {hm} {request['hy']}\n"\
                        "Григорианская дата:\n"\
                        f"{request['gd']}/{request['gm']}/{request['gy']}")


def handlers_webapp(dp: Dispatcher):
    dp.register_message_handler(web_app_mess, content_types='web_app_data')
