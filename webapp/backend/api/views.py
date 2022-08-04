from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import HitasSerializer
from .models import Hitas
from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import HttpResponse
from .permisions import BlocklistPermission

def index(request):
    return HttpResponse("DRF")


class HitasViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Hitas to be viewed or edited.
    """
    queryset = Hitas.objects.all()
    serializer_class = HitasSerializer
    permission_classes = (BlocklistPermission,)

    @action(methods=['get'], detail=False)
    def chumash(self, request):
        model = Hitas.objects.order_by('-created_date')[:1].get()
        return Response({'title': 'Хумаш',
                         'date': model.jew_data,
                         'text': model.chumash
                         })

    @action(methods=['get'], detail=False)
    def tehillim(self, request):
        model = Hitas.objects.order_by('-created_date')[:1].get()
        return Response({'title': 'Теилим',
                         'date': model.jew_data,
                         'text': model.tehillim
                         })

    @action(methods=['get'], detail=False)
    def tanya(self, request):
        model = Hitas.objects.order_by('-created_date')[:1].get()
        return Response({'title': 'Тания',
                         'date': model.jew_data,
                         'text': model.tanya
                         })

    @action(methods=['get'], detail=False)
    def hayom_yoma(self, request):
        model = Hitas.objects.order_by('-created_date')[:1].get()
        return Response({'title': 'Йом йом',
                         'date': model.jew_data,
                         'text': model.hayom_yoma
                         })

    @action(methods=['get'], detail=False)
    def rambam(self, request):
        model = Hitas.objects.order_by('-created_date')[:1].get()
        return Response({'title': '«Книга заповедей» РАМБАМа',
                         'date': model.jew_data,
                         'text': model.rambam
                         })

    @action(methods=['get'], detail=False)
    def moshiach(self, request):
        model = Hitas.objects.order_by('-created_date')[:1].get()
        return Response({'title': 'Мошиах и Освобождение',
                         'date': model.jew_data,
                         'text': model.moshiach,
                         })
