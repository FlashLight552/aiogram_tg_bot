from django.shortcuts import render
from datetime import datetime

from . import services


def index(request):
    context = {}
    return render(request, 'index.html', context)

def chumash(request):
    list = services.hitas_text()
    context = { 'time' : list[0],
                'text' : list[1],
                'title' : 'Хумаш',
                }
    return render(request, 'content.html', context)

def tehillim(request):
    list = services.hitas_text()
    context = { 'time' : list[0],
                'text' : list[2],
                'title' : 'Теилим',
                }
    return render(request, 'content.html', context)

def tanya(request):
    list = services.hitas_text()
    context = { 'time' : list[0],
                'text' : list[3],
                'title' : 'Тания',
                }
    return render(request, 'content.html', context)

def hayom_yom(request):
    list = services.hitas_text()
    context = { 'time' : list[0],
                'text' : list[4],
                'title' : 'Йом йом',
                }
    return render(request, 'content.html', context)

def rambam(request):
    list = services.hitas_text()
    context = { 'time' : list[0],
                'text' : list[5],
                'title' : '«Книга заповедей» РАМБАМа',
                }
    return render(request, 'content.html', context)

def moshiach(request):
    list = services.hitas_text()
    context = { 'time' : list[0],
                'text' : list[6],
                'title' : '«Мошиах и Освобождение»',
                }
    return render(request, 'content.html', context)


def conversion_start(request):
    context = {}
    return render(request, 'conversion_start.html', context)

def gregorian_conv(request):

    date = datetime.today().strftime('%Y-%m-%d')
    context = {'day' : date.split('-')[2],
                'mounth' : date.split('-')[1],
                'year' : date.split('-')[0],}
    return render(request, 'gregorian_conv.html', context)

def hebrew_conv(request):
    d, m ,y = services.hebrew_data()
    context = {'day':d, 'mounth':m, 'year':y}
    return render(request, 'hebrew_conv.html', context)