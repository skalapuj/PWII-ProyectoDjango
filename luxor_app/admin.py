from django.contrib import admin
from .models import SolicitudFinanciamiento

@admin.register(SolicitudFinanciamiento)
class SolicitudFinanciamientoAdmin(admin.ModelAdmin):
   list_display = ('id', 'nombre', 'dni', 'modelo', 'plan', 'cuota_mensual', 'fecha_creacion')
   list_filter = ('modelo', 'plan', 'fecha_creacion')
   search_fields = ('nombre', 'dni', 'email', 'telefono')
   ordering = ('-fecha_creacion',)
   readonly_fields = ('nombre', 'dni', 'edad', 'ingresos_garante', 'edad_garante', 'garante_antiguedad', 'garante_tipo_trabajo',
                      'fecha_creacion', 'modelo', 'plan', 'cuota_mensual', 'precio_base', 'importe_adjudicacion',
                       'gastos_retiro', 'cuotas_cantidad')

   def has_delete_permission(self, request, obj=None):
      return False

   def has_add_permission(self, request):
      return False