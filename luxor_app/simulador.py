# --- CONSTANTES ---
CUOTAS_PLAN = 84
ANIOS_PLAN = CUOTAS_PLAN // 12
TASA_INTERES = 0.065  # 6.5%
GASTOS_PATENTAMIENTO = 0.08  # 8%
ANTIGUEDAD_DEPENDIENTE = 1
ANTIGUEDAD_INDEPENDIENTE = 2
FACTOR_INGRESO_GARANTE = 4

# Catalogo de Vehículos
MODELOS_AUTOS = {
    "Fiat Cronos Precision": 38500000,
    "VW Taos Comfortline": 59000000,
    "Toyota SW4 SRX": 95000000,
    "Audi A4 Quattro": 155000000
}


# --- Core del simulador adaptado
def calcular_simulacion_web(datos_usuario):
    # Busco el auto en el catálogo
    modelo_nombre = datos_usuario['modelo']
    precio_auto = MODELOS_AUTOS.get(modelo_nombre, 0)

    # Configuración del plan
    plan_nombre = datos_usuario['plan']
    if plan_nombre == "Plan 70/30":
        p_fin, p_adj = 0.7, 0.3
    else:
        p_fin, p_adj = 0.8, 0.2

    # Financiamiento
    monto_fin = precio_auto * p_fin
    cuota = (monto_fin + (monto_fin * TASA_INTERES)) / CUOTAS_PLAN

    # Validaciones de edad y antiguedad
    errores = []

    # Comprobamos antigüedad según si es independiente o no
    es_independiente = datos_usuario['garante_tipo_trabajo'] == 'independiente'
    req_antiguedad = ANTIGUEDAD_INDEPENDIENTE if es_independiente else ANTIGUEDAD_DEPENDIENTE

    if datos_usuario['garante_antiguedad'] < req_antiguedad:
        errores.append(f"Garante requiere {req_antiguedad} años de antigüedad.")

    # Comprobamos tus ingresos protegidos del garante
    if datos_usuario['ingresos_garante'] < (cuota * FACTOR_INGRESO_GARANTE):
        monto_minimo = cuota * FACTOR_INGRESO_GARANTE
        errores.append(f"Ingreso del garante insuficiente (Mínimo requerido: ${monto_minimo:,.2f}).")

    # Si la lista de errores tiene algo, significa que no calificó
    if errores:
        return {
            'aprobado': False,
            'lista_errores': errores
        }

    # Si no hay errores, devolvemos el informe de financiamiento
    return {
        'aprobado': True,
        'resultado': {
            'modelo': modelo_nombre,
            'precio_base': precio_auto,
            'plan': plan_nombre,
            'cuotas': CUOTAS_PLAN,
            'cuota_mensual': round(cuota, 2),
            'adjudicacion': round(precio_auto * p_adj, 2),
            'gastos_retiro': round(precio_auto * GASTOS_PATENTAMIENTO, 2),
            'tasa': "6,50%"
        }
    }