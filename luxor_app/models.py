from django.db import models


class SolicitudFinanciamiento(models.Model):
    # --- DATOS DEL TITULAR ---
    nombre = models.CharField(max_length=100)
    dni = models.BigIntegerField()
    telefono = models.CharField(max_length=20)
    edad = models.IntegerField()
    email = models.EmailField()
    ingresos_personal = models.FloatField()

    # --- DATOS DEL GARANTE ---
    garante_nombre = models.CharField(max_length=100)
    ingresos_garante = models.FloatField()
    edad_garante = models.IntegerField()
    garante_tipo_trabajo = models.CharField(max_length=20)
    garante_antiguedad = models.IntegerField()

    # --- DATOS DEL PLAN FINANCIERO CALCULADO ---
    modelo = models.CharField(max_length=50)
    precio_base = models.FloatField()
    plan = models.CharField(max_length=20)
    cuotas_cantidad = models.IntegerField()
    cuota_mensual = models.FloatField()
    importe_adjudicacion = models.FloatField()
    gastos_retiro = models.FloatField()


    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud #{self.id} - {self.nombre} ({self.modelo})"