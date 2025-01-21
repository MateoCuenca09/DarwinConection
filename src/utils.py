import datetime

def obtener_fecha_hoy_ayer():
    # Fecha de hoy
    fecha_hoy = datetime.datetime.now()
    fecha_hoy_formateada = fecha_hoy.strftime("%Y/%m/%d")
    
    # Fecha de ayer
    fecha_ayer = fecha_hoy - datetime.timedelta(days=1)
    fecha_ayer_formateada = fecha_ayer.strftime("%Y/%m/%d")
    
    return fecha_ayer_formateada, fecha_hoy_formateada