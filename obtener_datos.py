import pandas as pd
import datetime

def timeouts(df): 
    try:
        # Convertir la columna de fecha a tipo datetime
        df['date'] = pd.to_datetime(df['date'])

        # Ordenar el DataFrame por 'idchat' y 'fecha' en orden descendente
        df = df.sort_values(['darwinChatID', 'date'], ascending=[True, False])

        # Agrupar por 'idchat' y seleccionar el primer mensaje de cada grupo
        ultimo_mensaje = df.groupby('darwinChatID').first()

        # Filtrar los grupos donde el mensaje contiene 'timeout'
        timeout = ultimo_mensaje[ultimo_mensaje['typeClose'] == 'timeout'].shape[0]
        return timeout
    except Exception as e:
        print("Error al procesar timeouts:", e)


def start(df):
    try:
        start = df['darwinChatID'].nunique()
        return start
    except Exception as e:
        print("Error al procesar starts:", e)

def DNI_inc(df):
    try:
        conteo_mensaje = df['message'].value_counts().get('El formato ingresado es incorrecto, por favor indícanos tu DNI, CUIT o CUIL.')
        if conteo_mensaje == None:
            conteo_mensaje = 0
        return conteo_mensaje
    except Exception as e:
        print("Error al procesar DNIs incorrectos:", e)

def menuPrincipal(df):   
    try:
        # Filtrar el DataFrame por el valor "Menu Principal" en la columna 'page'
        df_filtrado = df.loc[df['page'] == 'Menu Principal - A1']
        df_filtrado2 = df_filtrado.loc[df['user'] != 'system']

        # Contar la cantidad de valores únicos en la columna 'darwinChatID' después del filtrado
        cantidad_menu_principal = df_filtrado2.shape[0]
        return cantidad_menu_principal
    except Exception as e:
        print("Error al procesar menuPrincipal:", e)

def derivadas(df):
    try:
        # Filtrar el DataFrame por el valor "Menu Principal" en la columna 'page'
        df_filtrado = df.loc[df['page'] == 'Derivar']

        # Contar la cantidad de valores únicos en la columna 'darwinChatID' después del filtrado
        Derivadas = df_filtrado['darwinChatID'].nunique()
        return Derivadas
    except Exception as e:
        print("Error al procesar derivadas:", e)

def menuAceso(df): 
    try:
        cantidad_menu_principal = menuPrincipal(df)  
        df['combined'] = df['page'] + ' ' + df['message']

        df_filtrado = df.loc[df['combined'] == 'Menu Principal - A1 1']
        MPop1 = df_filtrado.shape[0]

        df_filtrado = df.loc[df['combined'] == 'Menu Principal - A1 2']
        MPop2 = df_filtrado.shape[0]

        df_filtrado = df.loc[df['combined'] == 'Menu Principal - A1 3']
        MPop3 = df_filtrado.shape[0]

        df_filtrado = df.loc[df['combined'] == 'Menu Principal - A1 4']
        MPop4 = df_filtrado.shape[0]

        df_filtrado = df.loc[df['combined'] == 'Menu Principal - A1 5']
        MPop5 = df_filtrado.shape[0]

        df_filtrado = df.loc[df['combined'] == 'Menu Principal - A1 6']
        MPop6 = df_filtrado.shape[0]

        df_filtrado = df.loc[df['combined'] == 'Menu Principal - A1 7']
        MPop7 = df_filtrado.shape[0]

        totalMP = MPop1 + MPop2 + MPop3 + MPop4 + MPop5 + MPop6 + MPop7
        perdidos = cantidad_menu_principal - totalMP

        return {"opcion1": MPop1, "opcion2": MPop2,"opcion3": MPop3, "opcion4": MPop4,"opcion5": MPop5,"opcion6": MPop6,"opcion7": MPop7,"perdidos": perdidos,}
    except Exception as e:
        print("Error al procesar menuAcesos:", e)


def reclamo(df):
    try:
        df_filtrado = df.loc[df['combined'] == 'Encuesta 2 - B1 ¿Tu reclamo o consulta fue resuelto? Si No']
        P_Reclamo = df_filtrado.shape[0]

        df_filtrado = df.loc[df['intent'] == 'opcion-si']
        encuestaSi = df_filtrado.shape[0]

        df_filtrado = df.loc[df['intent'] == 'opcion-no']
        encuestaNo = df_filtrado.shape[0]

        Perdidos_encuesta = P_Reclamo - encuestaSi - encuestaNo
        return {"P_Reclamo":P_Reclamo, "encuestaNo":encuestaNo, "encuestaSi":encuestaSi, "Perdidos_encuesta":Perdidos_encuesta}
    except Exception as e:
        print("Error al procesar reclamos:", e)

def encuesta(df):
    try:
        df_filtrado = df.loc[df['combined'] == 'Calificacion - B2 ¿Cómo calificas el nivel de satisfacción con esta gestión? Muy Insatisfecha/o Insatisfecha/o Indiferente Satisfecha/o Muy Satisfecha/o']
        Encuestas = df_filtrado.shape[0]

        df_filtrado = df.loc[df['combined'] == 'Calificacion - B2 Muy Satisfecha/o']
        Muy_Satisfecha = df_filtrado.shape[0]

        df_filtrado = df.loc[df['combined'] == 'Calificacion - B2 Satisfecha/o']
        Satisfecha = df_filtrado.shape[0]

        df_filtrado = df.loc[df['combined'] == 'Calificacion - B2 Insatisfecha/o']
        Insatisfecha = df_filtrado.shape[0]

        df_filtrado = df.loc[df['combined'] == 'Calificacion - B2 Muy Insatisfecha/o']
        Muy_Insatisfecha = df_filtrado.shape[0]

        sin_respuesta = Encuestas - Muy_Satisfecha - Satisfecha - Insatisfecha - Muy_Insatisfecha
        return{"Encuestas":Encuestas, "Muy_Satisfecha":Muy_Satisfecha, "Satisfecha":Satisfecha, "Insatisfecha":Insatisfecha,
               "Muy_Insatisfecha":Muy_Insatisfecha,'Sin_respuesta':sin_respuesta}
    except Exception as e:
        print("Error al procesar encuestas:", e)

