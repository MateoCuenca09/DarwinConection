import pandas as pd


def calcular_porcentaje(valor, total):
    if total == 0 or None:
        return "0%"
    porcentaje = (valor / total) * 100
    porcentaje_redondeado = round(porcentaje)
    porcentaje_con_simbolo = f"{porcentaje_redondeado}%"
    return porcentaje_con_simbolo

def tabla1(starts,DNI_inc,menuPrincipal,timeouts,derivadas):
    try:
        df = pd.DataFrame({
        "TOTAL": {
            "START (Inicio de conversación)": starts, 
            "DNI incorrecto":DNI_inc, 
            "LLEGAN AL MENÚ PRINCIPAL":menuPrincipal,
            "TIMEOUT (cliente no responde y bot envía mensaje)":timeouts, 
            "DERIVACIONES A ASESOR":derivadas,
            '':None  
                },

        "PORCENTAJES": {
            "START (Inicio de conversación)":calcular_porcentaje(starts,starts),
            "DNI incorrecto":calcular_porcentaje(DNI_inc,starts),
            "LLEGAN AL MENÚ PRINCIPAL":calcular_porcentaje(menuPrincipal,starts), 
            "TIMEOUT (cliente no responde y bot envía mensaje)":calcular_porcentaje(timeouts,starts),
            "DERIVACIONES A ASESOR":calcular_porcentaje(derivadas,starts),
            '':None  
            },
        })
        return df
    except Exception as e:
        print("Error al crear Tabla1:", e)

def tabla2(menuAceso,menuPrincipal):
    try:
        df1 = pd.DataFrame({
        "TOTAL": {
            'Expensas':menuAceso['opcion1'], 'Inicio de Obra / Amojonado':menuAceso['opcion2'],'Cesiones':menuAceso['opcion3'],
            'Servicios e impuestos':menuAceso['opcion4'], 'Contactos útiles':menuAceso['opcion5'], 'Ventas y alquileres':menuAceso['opcion6'],
            'Otras consultas': menuAceso['opcion7'], 'Se pierden en este menú':menuAceso['perdidos'],
            '':None  
        },
        "PORCENTAJES":{
            'Expensas':calcular_porcentaje(menuAceso['opcion1'],menuPrincipal), 
            'Inicio de Obra / Amojonado':calcular_porcentaje(menuAceso['opcion2'],menuPrincipal),
            'Cesiones':calcular_porcentaje(menuAceso['opcion3'],menuPrincipal),
            'Servicios e impuestos':calcular_porcentaje(menuAceso['opcion4'],menuPrincipal), 
            'Contactos útiles':calcular_porcentaje(menuAceso['opcion5'],menuPrincipal), 
            'Ventas y alquileres':calcular_porcentaje(menuAceso['opcion6'],menuPrincipal),
            'Otras consultas': calcular_porcentaje(menuAceso['opcion7'],menuPrincipal),
            'Se pierden en este menú':calcular_porcentaje(menuAceso['perdidos'],menuPrincipal),
            '':None            
        }
        })
        return df1
    except Exception as e:
        print("Error al crear Tabla2:", e)

def Tabla3(reclamos,starts):
    try:
        df2 = pd.DataFrame({
        "TOTAL":{
            'PREGUNTA SI EL RECLAMO FUE RESUELTO':reclamos['P_Reclamo'],
            'SÍ':reclamos['encuestaSi'],
            'NO':reclamos['encuestaNo'],
            'SIN RESPUESTA':reclamos['Perdidos_encuesta'],
            '':None
        },
        'PORCENTAJES':{
            'PREGUNTA SI EL RECLAMO FUE RESUELTO':calcular_porcentaje(reclamos['P_Reclamo'],starts),
            'SÍ':calcular_porcentaje(reclamos['encuestaSi'],reclamos['P_Reclamo']),
            'NO':calcular_porcentaje(reclamos['encuestaNo'],reclamos['P_Reclamo']),
            'SIN RESPUESTA':calcular_porcentaje(reclamos['Perdidos_encuesta'],reclamos['P_Reclamo']),
            '':None
        }
        })
        return df2
    except Exception as e:
        print("Error al crear Tabla3:", e)

def Tabla4(encuesta,starts):
    try:
        df3 = pd.DataFrame({
        'TOTAL':{
        'ENCUESTAS DE SATISFACCIÓN ENVIADAS':encuesta['Encuestas'],
        'MUY SATISFECHO':encuesta['Muy_Satisfecha'],
        'SATISFECHO':encuesta['Satisfecha'],
        'INSATISFECHO':encuesta['Insatisfecha'],
        'MUY INSATISFECHO':encuesta['Muy_Satisfecha'],
        'SIN RESPUESTA':encuesta['Sin_respuesta'],
        '':None
        },
        'PORCENTAJES':{
        'ENCUESTAS DE SATISFACCIÓN ENVIADAS':calcular_porcentaje(encuesta['Encuestas'],starts),
        'MUY SATISFECHO':calcular_porcentaje(encuesta['Muy_Satisfecha'],encuesta['Encuestas']),
        'SATISFECHO':calcular_porcentaje(encuesta['Satisfecha'],encuesta['Encuestas']),
        'INSATISFECHO':calcular_porcentaje(encuesta['Insatisfecha'],encuesta['Encuestas']),
        'MUY INSATISFECHO':calcular_porcentaje(encuesta['Muy_Satisfecha'],encuesta['Encuestas']),
        'SIN RESPUESTA':calcular_porcentaje(encuesta['Sin_respuesta'],encuesta['Encuestas']),
        '':None        
        }
        })
        return df3
    except Exception as e:
        print("Error al crear Tabla4:", e)