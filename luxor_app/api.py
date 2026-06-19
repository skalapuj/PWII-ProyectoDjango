from rest_framework import viewsets
from .models import SolicitudFinanciamiento
from .serializers import SolicitudFinanciamientoSerializer


class SolicitudFinanciamientoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SolicitudFinanciamiento.objects.all().order_by('-fecha_creacion')
    serializer_class = SolicitudFinanciamientoSerializer