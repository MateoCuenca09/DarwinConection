import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime
# Cargamos variables privadas
load_dotenv()

# Especifica la ruta de tu archivo Excel  
archivo_excel = os.getenv("archivo_excel")  
activo_path = os.getenv("activo_path")
temp_path = os.getenv("temp_path")
folder_temp_path = os.getenv("folder_temp_path") 

def guardar(df):
    try:
        df_existente = pd.read_csv(activo_path) # Levanto datos existentes
        df_nuevo = pd.concat([df, df_existente], ignore_index=True) # Concateno con datos nuevos
        df_nuevo = df_nuevo.drop_duplicates(ignore_index=True, keep='last', subset='_id') # Tiro duplicados

    except FileNotFoundError:
        df_nuevo = df

    try:
        df_nuevo.loc[:, 'date'] = pd.to_datetime(df_nuevo['date']) # Convierto mi columna a datetime
        df_nuevo.loc[:, 'Mes'] = df_nuevo['date'].dt.strftime('%m-%Y') # Formateo mes-año

        df_nuevo.sort_values(by='date', ascending=False, inplace=True) # Ordeno por fecha mas actual

        df_actual = df_nuevo.iloc[:60000] # Separo las ultimas lineas
        df_actual.to_csv(activo_path, index = False, encoding='utf-8-sig') # Guardo las ultimas lineas

        df_antiguo = df_nuevo.iloc[60000:] # Selecciono el resto de lineas
        separar_por_mes(df_antiguo) # Separo y guardo x mes
    except Exception as e:
        print("Error guardar(): ",e)

def separar_por_mes(df_antiguo):
    try:
        df['nueva_columna'] = df['columna_original'].str.slice(0, 7)
        grupos_por_mes = df_antiguo.groupby('Mes') # Agrupo x mes

        # Iterar sobre cada grupo y guardar en archivos CSV
        for mes, grupo in grupos_por_mes:
            nombre_archivo = f'{mes}.csv'  # Establecer el nombre del archivo
            ruta = folder_temp_path + nombre_archivo
            grupo.to_csv(ruta, index=False, encoding='utf-8-sig')

    except Exception as e:
        print("Error separar_por_mes(): ", e)

class FileHandler():
    def guardar_mes(self, df):
        
        df_activo = self._concat_activo(df)

        df_activo.sort_values(by='date', ascending=False, inplace=True) # Ordeno por fecha mas actual
        df_activo = df_activo.iloc[:60000] # Separo las ultimas lineas
        df_activo.to_csv(activo_path, index = False, encoding='utf-8-sig') # Guardo las ultimas lineas


    def _concat_activo(self, df):
        try:
            df_local = pd.read_csv(activo_path) # Leo activo local
            df_activo = pd.concat([df, df_local], ignore_index=True) # Concateno con datos nuevos
            df_activo.drop_duplicates(ignore_index=True, keep='last', subset='_id', inplace=True) # Tiro duplicados
       
        except FileNotFoundError:
            df_activo = df
            
        return df_activo

    def separar_por_mes(self, df):
        try:
            df['Mes'] = df['date'].str.slice(0, 7)
            grupos_por_mes = df.groupby('Mes') # Agrupo x mes

            # Iterar sobre cada grupo y guardar en archivos CSV
            for mes, grupo in grupos_por_mes:
                nombre_archivo = f'{mes}.csv'  # Establecer el nombre del archivo
                ruta = folder_temp_path + nombre_archivo
                grupo.to_csv(ruta, index=False, encoding='utf-8-sig')

        except Exception as e:
            print("Error separar_por_mes(): ", e)

if __name__ == '__main__':
    df = pd.read_excel('Crudo.xlsx')
    FileHandler().separar_por_mes(df)