from rest_framework import serializers
from .models import SolicitudFinanciamiento

class SolicitudFinanciamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudFinanciamiento
        fields = '__all__'