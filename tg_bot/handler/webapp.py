from aiogram import types, Dispatcher
import requests

async def web_app_mess(message: types.message):
    await message.delete()
    date = str(message.web_app_data.data).split('-')
    if date[0] == 'gregorian':
        date[4] = str(date[4]).replace('true','on')
        url = f'https://www.hebcal.com/converter?cfg=json&date={date[3]}-{date[2]}-{date[1]}&g2h=1&strict=1&gs={date[4]}'
        raw_request = requests.get(url)
        text_request = raw_request.json()
        
        await message.answer("Gregorian data:\n"\
                        f"{text_request['gd']}/{text_request['gm']}/{text_request['gy']}\n"\
                        "Hebrew data:\n"\
                        f"{text_request['hd']} {text_request['hm']} {text_request['hy']}")

    if date[0] == 'hebrew':
        url = f'https://www.hebcal.com/converter?cfg=json&hy={date[3]}&hm={date[2]}&hd={date[1]}&h2g=1&strict=1'
        request = requests.get(url).json()
        await message.answer("Hebrew data:\n"\
                        f"{request['hd']} {request['hm']} {request['hy']}\n"\
                        "Gregorian data:\n"\
                        f"{request['gd']}/{request['gm']}/{request['gy']}")


def handlers_webapp(dp: Dispatcher):
    dp.register_message_handler(web_app_mess, content_types='web_app_data')
