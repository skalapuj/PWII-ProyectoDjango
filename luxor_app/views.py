import requests
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import JsonResponse
from .forms import SimuladorForm
from .models import SolicitudFinanciamiento
from .simulador import calcular_simulacion_web
from django.conf import settings

def pagina_inicial(request):
    return render(request, "luxor_app/index.html")


def obtener_cotizacion_dolar_view(request):
    url_api_externa = "https://dolarapi.com/v1/dolares/oficial"

    try:
        respuesta = requests.get(url_api_externa, timeout=5)

        if respuesta.status_code == 200:
            datos_api = respuesta.json()
            valor_venta = datos_api.get('venta')

            return JsonResponse({
                'status': 'success',
                'cotizacion': valor_venta
            })
        else:
            return JsonResponse({
                'status': 'fallback',
                'cotizacion': 1500.00,  # Valor por si se cae la API externa
                'message': 'API externa no disponible, usando valor de respaldo.'
            })

    except requests.RequestException as e:
        return JsonResponse({
            'status': 'fallback',
            'cotizacion': 1500.00,
            'error': str(e)
        })


def simular_financiamiento_view(request):
    if request.method == 'POST':
        form = SimuladorForm(request.POST)

        if form.is_valid():
            datos_limpios = form.cleaned_data
            resultado_simulador = calcular_simulacion_web(datos_limpios)

            if not resultado_simulador['aprobado']:
                return JsonResponse({
                    'status': 'error',
                    'errors': resultado_simulador['lista_errores']
                }, status=400)


            try:
                res_calculado = resultado_simulador['resultado']
                nueva_solicitud = SolicitudFinanciamiento.objects.create(
                    # Datos que vinieron limpios del formulario web
                    nombre=datos_limpios['nombre'],
                    dni=datos_limpios['dni'],
                    telefono=datos_limpios['telefono'],
                    email=datos_limpios['email'],
                    edad=datos_limpios['edad'],
                    ingresos_personal=datos_limpios['ingresos_personal'],

                    garante_nombre=datos_limpios['garante_nombre'],
                    ingresos_garante=datos_limpios['ingresos_garante'],
                    edad_garante=datos_limpios['edad_garante'],
                    garante_tipo_trabajo=datos_limpios['garante_tipo_trabajo'],
                    garante_antiguedad=datos_limpios['garante_antiguedad'],

                    # Datos numéricos calculados por simulador.py
                    modelo=res_calculado['modelo'],
                    precio_base=res_calculado['precio_base'],
                    plan=res_calculado['plan'],
                    cuotas_cantidad=res_calculado['cuotas'],
                    cuota_mensual=res_calculado['cuota_mensual'],
                    importe_adjudicacion=res_calculado['adjudicacion'],
                    gastos_retiro=res_calculado['gastos_retiro']
                )

            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'errors': [f"Error crítico al guardar en Base de Datos: {str(e)}"]
                }, status=500)

            try:
                asunto_mail = f"Confirmación de Simulación de Financiamiento - Luxor Motors"

                cuerpo_mensaje = (
                    f"Hola {datos_limpios['nombre']},\n\n"
                    f"¡Gracias por consultar en Luxor Motors! Te confirmamos que tu solicitud de simulación "
                    f"ha sido procesada y aprobada con éxito por nuestro sistema de calificación.\n\n"
                    f"A continuación, te detallamos el Informe Final de tu financiamiento:\n"
                    f"==================================================\n"
                    f"• Vehículo Seleccionado: {res_calculado['modelo']}\n"
                    f"• Precio de Lista Base: ${res_calculado['precio_base']:,}\n"
                    f"• Tipo de Financiamiento: {res_calculado['plan']}\n"
                    f"• Cantidad de Cuotas: {res_calculado['cuotas']} meses\n"
                    f"--------------------------------------------------\n"
                    f"• VALOR CUOTA MENSUAL: ${res_calculado['cuota_mensual']:,}\n"
                    f"• Importe Adjudicación (30% o 0%): ${res_calculado['adjudicacion']:,}\n"
                    f"• Gastos Estimados de Retiro (8%): ${res_calculado['gastos_retiro']:,}\n"
                    f"• Tasa de Interés Nominal Anual: {res_calculado['tasa']}\n"
                    f"==================================================\n\n"
                    f"Datos del Garante Calificado:\n"
                    f"• Nombre completo: {datos_limpios['garante_nombre']}\n"
                    f"• Relación laboral: {datos_limpios['garante_tipo_trabajo']}\n\n"
                    f"Un asesor comercial se estará comunicando con vos al teléfono {datos_limpios['telefono']} "
                    f"para ultimar los detalles del contrato de adjudicación.\n\n"
                    f"Atentamente,\n"
                    f"El equipo de Luxor Motors S.A. 2026."
                )

                send_mail(
                    subject=asunto_mail,
                    message=cuerpo_mensaje,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[datos_limpios['email']],
                    fail_silently=True,
                )
                print(f" Correo de confirmación enviado con éxito a: {datos_limpios['email']}")
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'errors': [f"Error crítico al enviar en email: {str(e)}"]
                }, status=500)

            return JsonResponse({
                'status': 'success',
                'resultado': resultado_simulador['resultado']
            })

        else:
            return JsonResponse({ 'status': 'error', 'errors': form.errors }, status=400)

    return JsonResponse({ 'status': 'error', 'message': 'Método no permitido'}, status=405)

