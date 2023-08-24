import pandas as pd
import os

def menu_Principal(df): 
    try:
        # Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '1')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Principal'] = 'Expensas'

        # Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '2')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Principal'] = 'Obras'

        # Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '3')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Principal'] = 'Cesiones'

        # Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '4')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Principal'] = 'Servicios e Impuestos'


        # Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '5')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Principal'] = 'Contactos Útiles'


        # Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '6')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Principal'] = 'Ventas'

        # Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '7')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Principal'] = 'Otras Consultas'

    except Exception as e:
        print("Error al procesar menuAcesos:", e)

def menu_Expensas(df):
    try:
        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '1')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Secundario'] = 'ID Expensas'

        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '2')
        
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Expensa Corriente'
        df.loc[filtro, 'Menu Principal'] = 'Expensas'

        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '3')
        
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Actualizar Cupon'
        df.loc[filtro, 'Menu Principal'] = 'Expensas'

        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '4')
        
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Plan de Pagos'
        df.loc[filtro, 'Menu Principal'] = 'Expensas'

        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '5')
        
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Otras Consultas'
        df.loc[filtro, 'Menu Principal'] = 'Expensas'

        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '6')
        
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Debito Automatico'
        df.loc[filtro, 'Menu Principal'] = 'Expensas'

        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '7')
        
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Volver'
        df.loc[filtro, 'Menu Principal'] = 'Expensas'

    except Exception as e:
        print("Error menu_Expensas(): ",e)

def menu_Obras(df):
    try:
        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '1')
        
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Instructivo de obra'
        df.loc[filtro, 'Menu Principal'] = 'Obras'


        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '2')
        
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Firma de boleto'
        df.loc[filtro, 'Menu Principal'] = 'Obras'


        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '3')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Firma de posesión'
        df.loc[filtro, 'Menu Principal'] = 'Obras'


        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '4')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Amojonado'
        df.loc[filtro, 'Menu Principal'] = 'Obras'


        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '5')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Tareas previas'
        df.loc[filtro, 'Menu Principal'] = 'Obras'


        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '6')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Registrar obra nueva'
        df.loc[filtro, 'Menu Principal'] = 'Obras'


        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '7')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Otras consultas'
        df.loc[filtro, 'Menu Principal'] = 'Obras'


        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '0')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Volver'        
        df.loc[filtro, 'Menu Principal'] = 'Obras'


    except Exception as e:
        print("Error menu_Amojonado(): ",e)

def menu_Cesiones(df):
    try:
        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Cesiones') & (df['message'] == '0')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Principal'] = 'Cesiones'
        df.loc[filtro, 'Menu Secundario'] = 'Volver'  
        df.loc[filtro, 'Menu Terciario'] = 'Volver'    

        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Cesiones') & (df['message'] == '1')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Ceder'     
        df.loc[filtro, 'Menu Principal'] = 'Cesiones'

        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Menu Cesiones') & (df['message'] == '0')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Informar'      
        df.loc[filtro, 'Menu Principal'] = 'Cesiones'
        
    except Exception as e:
        print("Error menu_Cesiones(): ",e)

def menu_Servicios(df):
    try:
        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Botonera Tipo Servicio - F5') & (df['message'] == '1')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'UF Aguas Cordobesas'      
        df.loc[filtro, 'Menu Principal'] = 'Servicios e Impuestos'

        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Botonera Tipo Servicio - F5') & (df['message'] == '2')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Imp. Pcial.'  
        df.loc[filtro, 'Menu Principal'] = 'Servicios e Impuestos'
        
        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Botonera Tipo Servicio - F5') & (df['message'] == '3')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Imp. Municipal'  
        df.loc[filtro, 'Menu Principal'] = 'Servicios e Impuestos'

        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Botonera Tipo Servicio - F5') & (df['message'] == '0')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Volver'  
        df.loc[filtro, 'Menu Principal'] = 'Servicios e Impuestos'
        df.loc[filtro, 'Menu Terciario'] = 'Volver'  

    except Exception as e:
        print("Error menu_Servicios(): ",e)
        

def menu_Contactos(df):
    try:
        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Botonera Tipo Contacto - G5') & (df['message'] == '0')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Terciario'] = 'Volver'  
        df.loc[filtro, 'Menu Secundario'] = 'Volver'  
        df.loc[filtro, 'Menu Principal'] = 'Contactos Útiles'

        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Botonera Tipo Contacto - G5') & (df['message'] == '1')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Contactos del Barrio'  
        df.loc[filtro, 'Menu Principal'] = 'Contactos Útiles'
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'

        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Botonera Tipo Contacto - G5') & (df['message'] == '2')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Emprendedores'
        df.loc[filtro, 'Menu Principal'] = 'Contactos Útiles'
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'

        ###### Filtro para encontrar las filas que cumplan la condición
        filtro = (df['page'] == 'Botonera Tipo Contacto - G5') & (df['message'] == '3')
        # Renombrar los valores en la columna 'page' que cumplan con el filtro
        df.loc[filtro, 'Menu Secundario'] = 'Comercios'
        df.loc[filtro, 'Menu Principal'] = 'Contactos Útiles'
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'

        
    except Exception as e:
        print("Error menu_Contactos(): ",e)

def separar_por_mes(dataframe):
    try:        
        # Obtener la columna del mes
        dataframe['Mes'] = dataframe['date'].dt.strftime('%Y-%m')
        
        # Obtener el mes más nuevo o actual
        mes_actual = dataframe['Mes'].max()
        
        # Filtrar el DataFrame para obtener solo el mes más nuevo o actual
        df_mes_actual = dataframe[dataframe['Mes'] == mes_actual].copy()
        
        # Guardar cada DataFrame separado por mes en un archivo Excel
        for mes, df_mes in dataframe.groupby('Mes'):
            if mes != mes_actual:
                nombre_archivo = mes + '.xlsx'
                carpeta_guardado = 'C:\\Users\\cuenc\\OneDrive - EDISUR SA\\Mateo Cuenca\\DarwinConection\\PBI prueba'
                ruta_archivo = os.path.join(carpeta_guardado, nombre_archivo)
                df_mes.to_excel(ruta_archivo, index=False)
                print(f"El DataFrame para el mes {mes} ha sido guardado en {nombre_archivo}")

        df_mes_actual.drop('Mes', axis=1, inplace=True)

        return df_mes_actual
    except Exception as e:
        print("Error separar_por_mes(): ",e)

def guardar_historico(df):
    try:
        df_historico = pd.read_excel("C:\\Users\\cuenc\\OneDrive - EDISUR SA\\Mateo Cuenca\\DarwinConection\\PBI prueba\\Historico.xlsx")
        historico = True
    except FileNotFoundError as e:
        historico = False
        print("No se encuentra Excel Historico")
        print("Procede a crear uno nuevo vacio")
        df_historico = pd.DataFrame()

    try:
        df_historico_nuevo = pd.concat( [df_historico,df], ignore_index=True)
        if historico:
            df_historico_nuevo['date'] = pd.to_datetime(df_historico_nuevo['date'])
            df_historico_nuevo.sort_values('date')
            df_historico_nuevo = df_historico_nuevo.drop_duplicates(ignore_index=True, keep= 'first', subset='_id')
            df_historico_nuevo = separar_por_mes(df_historico_nuevo)
        df_historico_nuevo.to_excel("C:\\Users\\cuenc\\OneDrive - EDISUR SA\\Mateo Cuenca\\DarwinConection\\PBI prueba\\Historico.xlsx", index=False)
    except Exception as e:
        print("Error al indexar DF o guardar: ",e)


def getdatos(df):
    menu_Principal(df)
    menu_Expensas(df)
    menu_Obras(df)
    menu_Cesiones(df)
    menu_Servicios(df)
    menu_Contactos(df)

def mainPBI(datos):
    df = pd.DataFrame(datos)
    # Asegurémonos de que la columna 'date' sea de tipo datetime
    df['date'] = pd.to_datetime(df['date'])

    # Eliminar la zona horaria de la columna 'date'
    df['date'] = df['date'].dt.tz_convert(None)

    getdatos(df)
    guardar_historico(df)

    print("Termina proceso PBI")
