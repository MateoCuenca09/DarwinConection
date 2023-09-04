import pandas as pd
import os


def separar_por_mes(dataframe):
    try:
        # Obtener la columna del mes
        dataframe['Mes'] = dataframe['date'].dt.strftime('%Y-%m')

        # Obtener los dos meses más nuevos o actuales
        meses_actuales = dataframe['Mes'].nlargest(2)

        # Filtrar el DataFrame para obtener solo los dos meses más nuevos o actuales
        df_meses_actuales = dataframe[dataframe['Mes'].isin(meses_actuales)].copy()

        # Guardar cada DataFrame separado por mes en un archivo Excel
        for mes, df_mes in df_meses_actuales.groupby('Mes'):
            nombre_archivo = mes + '.xlsx'
            carpeta_guardado = "O:\\Gestion y Experiencia del Cliente\\5. SERVICIO DE ATENCIÓN AL CLIENTE\\11. TRANSFORMACIÓN DIGITAL\\ReportesDarwin\\PBI"
            ruta_archivo = os.path.join(carpeta_guardado, nombre_archivo)
            df_mes.to_excel(ruta_archivo, index=False)
            print(f"El DataFrame para el mes {mes} ha sido guardado en {nombre_archivo}")

        df_meses_actuales.drop('Mes', axis=1, inplace=True)

        return df_meses_actuales
    except Exception as e:
        print("Error separar_por_mes(): ", e)

def guardar_historico(df):
    try:
        df_historico = pd.read_excel("O:\\Gestion y Experiencia del Cliente\\5. SERVICIO DE ATENCIÓN AL CLIENTE\\11. TRANSFORMACIÓN DIGITAL\\ReportesDarwin\\PBI\\Historico.xlsx")
        historico = True
    except FileNotFoundError as e:
        historico = False
        print("No se encuentra Excel Historico")
        print("Procede a crear uno nuevo vacio")
        df_historico = pd.DataFrame()

    try:
        df_historico_nuevo = pd.concat([df_historico, df], ignore_index=True)
        if historico:
            df_historico_nuevo['date'] = pd.to_datetime(df_historico_nuevo['date'])
            df_historico_nuevo = df_historico_nuevo.sort_values('date')  # Agregamos 'inplace=True' para aplicar el orden directamente
            df_historico_nuevo = df_historico_nuevo.drop_duplicates(ignore_index=True, keep='first', subset='_id')
            separar_por_mes(df_historico_nuevo)  # Cambiamos esta línea para llamar a la función sin asignación
        df_historico_nuevo.to_excel("O:\\Gestion y Experiencia del Cliente\\5. SERVICIO DE ATENCIÓN AL CLIENTE\\11. TRANSFORMACIÓN DIGITAL\\ReportesDarwin\\PBI\\Historico.xlsx", index=False)
    except Exception as e:
        print("Error al indexar DF o guardar: ", e)