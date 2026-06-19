from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator

class SimuladorForm(forms.Form):
    # ==========================================
    # 1. DATOS PERSONALES
    # ==========================================
    nombre = forms.CharField(
        max_length=100,
        min_length=3,
        required=True,
        error_messages={
            'required': 'El nombre es obligatorio.',
            'min_length': 'El nombre debe tener al menos 3 caracteres.',
            'max_length': 'El nombre es demasiado largo.'
        }
    )

    dni = forms.IntegerField(
        required=True,
        validators=[
            # Rangos numéricos lógicos para un DNI en Argentina
            MinValueValidator(1000000, message="El DNI ingresado es demasiado corto."),
            MaxValueValidator(100000000, message="El DNI ingresado no es válido.")
        ],
        error_messages={
            'required': 'El DNI es obligatorio.',
            'invalid': 'Debe ingresar un número válido sin puntos.'
        }
    )

    telefono = forms.CharField(
        max_length=20,
        required=True,
        error_messages={'required': 'El teléfono de contacto es obligatorio.'}
    )

    edad = forms.IntegerField(
        required=True,
        validators=[
            MinValueValidator(18, message="El titular debe tener al menos 18 años."),
            MaxValueValidator(68, message="El titular al finalizar el plan debe tener como máximo 75 años.")
        ],
        error_messages={
            'required': 'La edad es obligatorio.',
            'invalid': 'El titular debe tener entre 18 y 68 años.'
        }
    )

    email = forms.EmailField(
        required=True,
        validators=[EmailValidator(message="El formato del correo electrónico no es válido.")],
        error_messages={'required': 'El correo electrónico es obligatorio.'}
    )

    ingresos_personal = forms.IntegerField(
        required=True,
        validators=[
            MinValueValidator(1, message="Los ingresos mensuales deben ser mayores a 0.")
        ],
        error_messages={
            'required': 'Debe especificar los ingresos mensuales del garante.',
            'invalid': 'Debe ingresar un monto numérico entero.'
        }
    )

    # ==========================================
    # 2. DATOS DEL GARANTE
    # ==========================================
    garante_nombre = forms.CharField(
        max_length=100,
        min_length=3,
        required=True,
        error_messages={
            'required': 'El nombre del garante es obligatorio.',
            'min_length': 'El nombre del garante debe tener al menos 3 caracteres.'
        }
    )

    edad_garante = forms.IntegerField(
        required=True,
        validators=[
            MinValueValidator(18, message="El garante debe tener al menos 18 años.")        ],
        error_messages={
            'required': 'La edad de garante es obligatorio.',
            'invalid': 'El garante debe tener al menos 18 años.'
        }
    )

    ingresos_garante = forms.IntegerField(
        required=True,
        validators=[
            MinValueValidator(1, message="Los ingresos mensuales deben ser mayores a 0.")
        ],
        error_messages={
            'required': 'Debe especificar los ingresos mensuales del garante.',
            'invalid': 'Debe ingresar un monto numérico entero.'
        }
    )

    garante_tipo_trabajo = forms.ChoiceField(
        choices=[('dependiente', 'Dependiente'), ('independiente', 'Independiente')],
        required=True
    )

    garante_antiguedad = forms.IntegerField(
        required=True,
        validators = [
        MinValueValidator(1, message="El garante debe tener antiguedad.")
        ]
    )

    # ==========================================
    # 3. DATOS DEL PLAN (Campos de Selección)
    # ==========================================

    # Definimos las opciones idénticas a los <option> de tu HTML
    OPCIONES_MODELOS = [
        ('Fiat Cronos Precision', 'Fiat Cronos Precision'),
        ('VW Taos Comfortline', 'VW Taos Comfortline'),
        ('Toyota SW4 SRX', 'Toyota SW4 SRX'),
        ('Audi A4 Quattro', 'Audi A4 Quattro'),
    ]

    OPCIONES_PLANES = [
        ('Plan 70/30', 'Plan 70/30'),
        ('Plan 80/20', 'Plan 80/20'),
    ]

    modelo = forms.ChoiceField(
        choices=OPCIONES_MODELOS,
        required=True,
        error_messages={'required': 'Debe seleccionar un modelo de la lista.'}
    )

    plan = forms.ChoiceField(
        choices=OPCIONES_PLANES,
        required=True,
        error_messages={'required': 'Debe seleccionar un tipo de plan.'}
    )