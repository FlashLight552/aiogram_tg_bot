from rest_framework import serializers
from .models import Hitas


class HitasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hitas
        fields = [
            'jew_data', 'chumash', 'tehillim', 'tanya',
            'hayom_yoma', 'rambam', 'moshiach',
            ]