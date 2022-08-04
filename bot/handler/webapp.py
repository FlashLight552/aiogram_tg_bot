from aiogram import types, Dispatcher
import requests

async def web_app_mess(message: types.message):
    await message.delete()
    date = str(message.web_app_data.data).split('-')
    month_name = {
    "Nisan": "Нисана",
    "Iyyar": "Ияра",
    "Sivan": "Сивана",
    "Tamuz": "Тамуза",
    "Av": "Ава",
    "Elul": "Элула",
    "Tishrei": "Тишрея",
    "Cheshvan": "Хешвана",
    "Kislev": "Кислева",
    "Tevet": "Тевета",
    "Sh'vat": "Швата",
    "Adar": "Адара",
    "Adar I": "Адара I",
    "Adar II": "Адара II",
    }
    if date[0] == 'gregorian':
        date[4] = str(date[4]).replace('true','on')
        url = f'https://www.hebcal.com/converter?cfg=json&date={date[3]}-{date[2]}-{date[1]}&g2h=1&strict=1&gs={date[4]}'
        request = requests.get(url).json()
        for item in month_name.keys():
            if item == request['hm']:
                hm =  month_name[item]
        await message.answer("Григорианская дата:\n"\
                        f"{request['gd']}/{request['gm']}/{request['gy']}\n"\
                        "Еврейская дата:\n"\
                        f"{request['hd']} {hm} {request['hy']}")

    if date[0] == 'hebrew':
        url = f'https://www.hebcal.com/converter?cfg=json&hy={date[3]}&hm={date[2]}&hd={date[1]}&h2g=1&strict=1'
        request = requests.get(url).json()
        for item in month_name.keys():
            if item == request['hm']:
                hm =  month_name[item]
        await message.answer("Еврейская дата:\n"\
                        f"{request['hd']} {hm} {request['hy']}\n"\
                        "Григорианская дата:\n"\
                        f"{request['gd']}/{request['gm']}/{request['gy']}")


def handlers_webapp(dp: Dispatcher):
    dp.register_message_handler(web_app_mess, content_types='web_app_data')
