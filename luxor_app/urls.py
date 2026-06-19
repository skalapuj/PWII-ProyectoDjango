from django.urls import path
from . import views
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from luxor_app.api import SolicitudFinanciamientoViewSet

router = DefaultRouter()
router.register(r'solicitudes', SolicitudFinanciamientoViewSet, basename='solicitud-api')

urlpatterns = [
    path('', views.pagina_inicial, name='index'),
    path('api/', include(router.urls)),
    path('simular-financiamiento/', views.simular_financiamiento_view, name='simular_financiamiento'),
    path('api/cotizacion-dolar/', views.obtener_cotizacion_dolar_view, name='api_dolar'),
]