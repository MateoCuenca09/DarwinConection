import pandas as pd

# Especifica la ruta de tu archivo Excel con Palabras Clave 
archivo_excel = 'O:/Gestion y Experiencia del Cliente/5. SERVICIO DE ATENCIÓN AL CLIENTE/11. TRANSFORMACIÓN DIGITAL/Excel - Otras Consultas/Excel Darwin - PBI - Automatico.xlsx' 
activo_path = "O:\\Gestion y Experiencia del Cliente\\5. SERVICIO DE ATENCIÓN AL CLIENTE\\11. TRANSFORMACIÓN DIGITAL\\ReportesDarwin\\Datos\\Activo.xlsx"
temp_path = "O:\\Gestion y Experiencia del Cliente\\5. SERVICIO DE ATENCIÓN AL CLIENTE\\11. TRANSFORMACIÓN DIGITAL\\ReportesDarwin\\Datos\\Temp.xlsx"
folder_temp_path = "O:\\Gestion y Experiencia del Cliente\\5. SERVICIO DE ATENCIÓN AL CLIENTE\\11. TRANSFORMACIÓN DIGITAL\\ReportesDarwin\\Datos\\"

def guardar(df):
    try:
        guardar_archivo(df,activo_path)
        separar_dos_meses()
        separar_por_mes()
    except Exception as e:
        print("Error guardar(): ",e)

def separar_dos_meses():
    try:        
        df = pd.read_excel(activo_path)
        fecha_reciente = pd.to_datetime(df['date'].max())
        delta_tiempo = 60 # Tiempo en dias que se quiere acumular en el Excel historico
        fecha_antigua = fecha_reciente - pd.to_timedelta(delta_tiempo, unit='D')

        df_activo = df.loc[df['date']>= fecha_antigua]
        df_dump = df.loc[df['date']<= fecha_antigua]
        guardar_archivo(df_dump,temp_path)
        df_activo.to_excel(activo_path, index = False)


    except Exception as e:
        print("Error separar_dos_meses(): ",e)


def guardar_archivo(df,path):
    try:
        df_existente = pd.read_excel(path)
        df_nuevo = pd.concat([df, df_existente], ignore_index=True)
        df_nuevo = df_nuevo.drop_duplicates(ignore_index=True, keep='last', subset='_id')
        df_nuevo.to_excel(path, index = False)
    except FileNotFoundError:
        print("Creando nuevo archivo, ",path)
        df.to_excel(path, index = False)
    except Exception as e:
        print("Error al guardar_archivo()")
        print("Archivo: ",path)
        print("Error: ",e)



def separar_por_mes():
    try:
        df_dump = pd.read_excel(temp_path)
        df_dump['date_temp'] = df_dump['date']
        df_dump['date_temp'] = pd.to_datetime(df_dump['date_temp'])
        df_dump['date_temp'] = df_dump['date_temp'].dt.strftime('%Y-%m')
        meses = df_dump['date_temp'].unique()
        for mes in meses:
            df_mes = df_dump.loc[df_dump['date_temp'] == mes]
            df_mes = df_mes.drop('date_temp', axis=1)
            archivo_path = folder_temp_path + mes + ".xlsx"
            guardar_archivo(df_mes, archivo_path)

    except Exception as e:
        print("Error separar_por_mes(): ", e)