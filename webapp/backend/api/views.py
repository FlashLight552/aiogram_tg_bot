from rest_framework.response import Response
from .serializers import HitasSerializer
from .models import Hitas
from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import HttpResponse
from .permissions import BlocklistPermission

def index(request):
    return HttpResponse("DRF")


fields = {
    'chumash': "Хумаш",
    'tehillim': "Теилим",
    'tanya': "Тания",
    'hayom_yoma': "Йом йом",
    'rambam': "«Книга заповедей» РАМБАМа",
    'moshiach': "Мошиах и Освобождение",
    }

class HitasViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Hitas to be viewed or edited.
    """
    queryset = Hitas.objects.all()
    serializer_class = HitasSerializer
    permission_classes = (BlocklistPermission,)
    
    @action(methods=['get'], detail=True)
    def view(self, request, pk=None):
        model = Hitas.objects.order_by('-created_date')[:1].get()
        for item in fields.keys():
            if item == pk:
                title = fields[item]
        return Response({
                'title': title,
                'date': model.jew_data,
                'text': getattr(model, pk),
                })