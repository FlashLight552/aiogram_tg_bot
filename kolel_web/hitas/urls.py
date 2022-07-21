from django.urls import path

from . import views

app_name = 'hitas'

urlpatterns = [
    path('', views.index, name='index'),
    path('chumash/', views.chumash, name='chumash'),
    path('tehillim/', views.tehillim, name='tehillim'),
    path('tanya/', views.tanya, name='tanya'),
    path('hayom_yom/', views.hayom_yom, name='hayom_yom'),
    path('rambam/', views.rambam, name='rambam'),
    path('moshiach/', views.moshiach, name='moshiach'),
    path('gregorian_conv/', views.gregorian_conv, name='gregorian_conv'),
    path('hebrew_conv/', views.hebrew_conv, name='hebrew_conv'),
    path('conversion_start/', views.conversion_start, name='conversion_start'),
]