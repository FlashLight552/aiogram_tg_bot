from django.urls import path, include
from api.views import HitasViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'hitas', HitasViewSet)

urlpatterns = [
    path('', include('api.urls')),
    path('api/', include(router.urls)),
]
