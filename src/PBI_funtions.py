import pandas as pd
from datetime import datetime, timedelta
from unidecode import unidecode
from guardar import FileHandler
from ISharePoint import ISharePoint
import logging
from config import DEBUG
import os
from dotenv import load_dotenv
# Cargamos variables privadas
load_dotenv()
archivo_excel =os.getenv('archivo_excel')
log_format = '%(asctime)s, %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(filename='datos/Avisos.txt', level=logging.INFO, format=log_format, datefmt=date_format)

def mainPBI(datos):
    """
    Función principal de PBI_functions que procesa y guarda en .xlsx los datos.

    Parámetros:
    - Datos: Archivo .json con datos de conversaciones
    """
    # Transformamos los datos a un DataFrame
    df = pd.DataFrame(datos)

    if DEBUG: df.to_excel("Crudo.xlsx", index= False)

    """ try:
        # Asegurémonos de que la columna 'date' sea de tipo datetime
        df['date'] = pd.to_datetime(df['date'])

        # Eliminar la zona horaria de la columna 'date'
        df['date'] = df['date'].dt.tz_convert(None)
        if DEBUG: df.to_excel("Date.xlsx", index= False)
    except Exception as e:  """

    # Procesamos los datos segun importancia
    menu_Principal(df)
    menu_Secundario(df)
    Feedback(df)
    fuera_de_horario(df)
    perdidos(df)
    no_ingresan(df)

    columnas = ['_id','user','date','message', 'room', 'idChat', 'Menu Principal', 'Menu Secundario', 'Menu Terciario', 'Otras Consultas', 'Reclamo', 'Encuesta']
    df = df[columnas]

    if DEBUG: df.to_excel("Procesado.xlsx", index= False)
    FileHandler().guardar_mes(df)
    FileHandler().separar_por_mes(df)


def Feedback(df):
    """
    Función Feedback que hace procesar los datos de Feedback de manera secuencial y los guarda en el mismo df.

    Parámetros:
    - df: Dataframe con todos los datos 
    """

    reclamo(df)
    encuesta(df)
    


def menu_Secundario(df):
    """
    Función menu_Secundario que procesa todos los posibles menus secundario.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    menu_Expensas(df)
    menu_Obras(df)
    menu_Cesiones(df)
    menu_Servicios(df)
    menu_Contactos(df)
    menu_Ventas(df)
    menu_OtrasConsultas(df)

def menu_Principal(df): 
    """
    Función menu_Principal que procesa todos los posibles menus principales y los guarda en el dataframe.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    try:
        ###### EXPENSAS ######
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '1')
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
    
        ###### OBRAS ######
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '2')
        df.loc[filtro, 'Menu Principal'] = 'Obras'

        ###### CESIONES ######
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '3')
        df.loc[filtro, 'Menu Principal'] = 'Cesiones'

        ###### SERVICIOS E IMPUESTOS ######
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '4')
        df.loc[filtro, 'Menu Principal'] = 'Servicios e Impuestos'

        ###### CONTACTOS UTILES ######
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '5')
        df.loc[filtro, 'Menu Principal'] = 'Contactos Útiles'

        ###### VENTAS ######
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '6')
        df.loc[filtro, 'Menu Principal'] = 'Ventas'

    except Exception as e:
        logging.warn("Error al procesar Menus Principales", e)

def menu_Expensas(df):
    """
    Función menu_Expensas que procesa todos los clientes que ingresaron al menu Expensas y su posteriores elecciones guardandolos en el dataframe.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    try:
        ###### ID EXPENSAS ######
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '1')
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Secundario'] = 'ID Expensas'

            # Encuentra ID Expensas
        filtro = df['message'].str.contains("Tu ID de expensas es:")
        df_idexp = df.loc[filtro]
        idChats_idexp = df_idexp['idChat']
        filtro = (df['idChat'].isin(idChats_idexp)) & (df['Menu Secundario'] == 'ID Expensas')
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'
        df.loc[filtro, 'user'] = df['room']

            # No Encuentra ID Expensas
        # Derivados Expensas #

        ######  EXPENSA CORRIENTE ######
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '2')
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Secundario'] = 'Expensa Corriente'
        
            # Encuentra Expensa Corriente
        filtro = (df['page'] == 'Archivo Expensa')
        df_expcorr = df.loc[filtro]
        idChats_expcorr = df_expcorr['idChat']
        filtro = (df['idChat'].isin(idChats_expcorr)) & (df['Menu Secundario'] == 'Expensa Corriente')
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'

            # No encuentra y Deriva a asesor
        filtro = df['message'].str.contains("No pudimos encontrar un ID de expensa con esos datos.")
        df_expcorNE = df.loc[filtro]
        idChats_expcorrNE = df_expcorNE['idChat']
        filtro = (df['idChat'].isin(idChats_expcorrNE)) & (df['Menu Secundario'] == 'Expensa Corriente') 
        df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'


        ###### ACTUALIZAR CUPON ######
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '3')
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Secundario'] = 'Actualizar Cupon'
        # Derivados Expensas #

        ###### PLAN DE PAGOS ######
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '4')
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Secundario'] = 'NO Plan de Pagos'
        # Derivados Expensas #


        ###### OTRAS CONSULTAS ######
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '5')
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Secundario'] = 'Otras Consultas'
        df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'
        # Derivados Expensas #
        

        ###### DEBITO AUTOMATICO ######
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '6')
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Secundario'] = 'Debito Automatico'
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'

        ###### VOLVER ######
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '0')
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Secundario'] = 'Volver'
        df.loc[filtro, 'Menu Terciario'] = 'Volver'

        ###### Derivados Expensas ######
        filtro = (df['message'].str.contains("derivacion")) 
        df_derivados = df.loc[filtro]
        idChats = df_derivados['idChat']
        filtro = (df['Menu Principal'] == 'Expensas') & (df['Menu Secundario'].notnull()) & (df['idChat'].isin(idChats)) & (df['Menu Terciario'].isnull())
        df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'
        
    except Exception as e:
        logging.warn(f'Error menu_Expensas() {e}')


def menu_Obras(df):
    """
    Función menu_Obras que procesa todos los clientes que ingresaron al menu Obras y su posteriores elecciones guardandolos en el dataframe.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    try:
        # 1 #
        ###### INSTRUCTIVO DE OBRA ######
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '1')
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Instructivo de obra'
            # Resuelto x Sistema
        filtro = df['message'].str.contains("Acá te envío el link para que puedas acceder al instructivo de obra para tu emprendimento:")
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Instructivo de obra'
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'
        df.loc[filtro, 'user'] = df['room']
            # Resuelto x Sistema V2
        filtro = df['message'].str.contains("Acá te envío el link para que puedas acceder al instructivo de obra para tu emprendimento")
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Instructivo de obra'
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'
        df.loc[filtro, 'user'] = df['room']

        # 2 #
        ###### FIRMA DE BOLETO ######
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '2')
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Firma de boleto'
        # Derivados Obras #

        # 3 #
        ###### AMOJONADO ######
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '3')
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Amojonado'
        # Derivados Obras #

        # 4 # 
        ###### REGISTRAR OBRA NUEVA ######
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '4')
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Registrar obra nueva'
        # Resuelto x Sistema
        filtro = df['message'].str.contains("Acá te envío el link para que puedas acceder al formulario de registro de legajo de obra:")
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Registrar obra nueva'
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'
        df.loc[filtro, 'user'] = df['room']

        # 5 #
        ###### CONEXION DE LUZ ######
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '5')
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Conexion de Luz'
        # Derivados Obras #

        # 6 # 
        ###### ESTADO DE SERVICIOS ######
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '4')
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Estado de servicios'
        # Derivados Obras #

        # 7 #
        ###### OTRAS CONSULTAS ######
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '7')
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Otras consultas'
        df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'      

        # Derivados Obras #

        ###### VOLVER ######
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '0')
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Volver'        
        df.loc[filtro, 'Menu Terciario'] = 'Volver'  


        ###### Derivados Obras ######
        filtro = (df['message'].str.contains("derivacion"))
        df_derivados = df.loc[filtro]
        idChats = df_derivados['idChat']
        filtro = (df['Menu Principal'] == 'Obras') & (df['Menu Secundario'].notnull()) & (df['idChat'].isin(idChats)) & (df['Menu Terciario'].isnull())
        df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'      

    except Exception as e:
        logging.warn(f'Error menu_Amojonado() {e}')

def menu_Cesiones(df):
    """
    Función menu_Cesiones que procesa todos los clientes que ingresaron al menu Cesiones y su posteriores elecciones guardandolos en el dataframe.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    try:
        ###### CEDER ######
        filtro = (df['page'] == 'Menu Cesiones') & (df['message'] == '1')     
        df.loc[filtro, 'Menu Principal'] = 'Cesiones'
        df.loc[filtro, 'Menu Secundario'] = 'Ceder'
        # Derivado
        filtro = (df['message'].str.contains("derivacion"))
        df_derivados = df.loc[filtro]
        idChats = df_derivados['idChat']
        filtro =(df['idChat'].isin(idChats)) & (df['Menu Principal'] == 'Cesiones') & (df['Menu Secundario'] == 'Ceder') & (df['Menu Terciario'].isnull())
        df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'


        ###### INFORMAR ######
        filtro = (df['page'] == 'Menu Cesiones') & (df['message'] == '2') 
        df.loc[filtro, 'Menu Principal'] = 'Cesiones'
        df.loc[filtro, 'Menu Secundario'] = 'Informar'   
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'    

        ###### VOLVER ######
        filtro = (df['page'] == 'Menu Cesiones') & (df['message'] == '0')
        df.loc[filtro, 'Menu Principal'] = 'Cesiones'
        df.loc[filtro, 'Menu Secundario'] = 'Volver'  
        df.loc[filtro, 'Menu Terciario'] = 'Volver'    

        
    except Exception as e:
        print(f'Error menu_Cesiones() {e}')

def menu_Servicios(df):
    """
    Función menu_Servicios que procesa todos los clientes que ingresaron al menu Servicios y su posteriores elecciones guardandolos en el dataframe.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    try:
        ###### UF AGUAS CORDOBESAS ######
        filtro = (df['page'] == 'Botonera Tipo Servicio - F5') & (df['message'] == '1')
        df_servicios = df[filtro]
        idChats_servicios = df_servicios['idChat']
        filtro = (df['idChat'].isin(idChats_servicios)) & (df['Menu Principal'] == 'Servicios e Impuestos' )
        df.loc[filtro, 'Menu Secundario'] = 'UF Aguas Cordobesas'  
        df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'


        ###### IMP POLICIAL ######
        filtro = (df['page'] == 'Botonera Tipo Servicio - F5') & (df['message'] == '2')
        df_servicios = df[filtro]
        idChats_servicios = df_servicios['idChat']
        filtro = (df['idChat'].isin(idChats_servicios)) & (df['Menu Principal'] == 'Servicios e Impuestos' )
        df.loc[filtro, 'Menu Secundario'] = 'Imp. Pcial.'
        df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'

        
        ###### IMP MUNICIPAL ######
        filtro = (df['page'] == 'Botonera Tipo Servicio - F5') & (df['message'] == '3')
        df_servicios = df[filtro]
        idChats_servicios = df_servicios['idChat']
        filtro = (df['idChat'].isin(idChats_servicios)) & (df['Menu Principal'] == 'Servicios e Impuestos' )
        df.loc[filtro, 'Menu Secundario'] = 'Imp. Municipal' 
        df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot' 

        ###### VOLVER ######
        filtro = (df['page'] == 'Botonera Tipo Servicio - F5') & (df['message'] == '0')
        df_servicios = df[filtro]
        idChats_servicios = df_servicios['idChat']
        filtro = (df['idChat'].isin(idChats_servicios)) & (df['Menu Principal'] == 'Servicios e Impuestos' )
        df.loc[filtro, 'Menu Secundario'] = 'Volver'  
        df.loc[filtro, 'Menu Terciario'] = 'Volver'  

    except Exception as e:
        logging.warn(f'Error menu_Servicios() {e}')

def menu_Contactos(df):
    """
    Función menu_Contactos que procesa todos los clientes que ingresaron al menu Contactos y su posteriores elecciones guardandolos en el dataframe.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    try:

        ###### CONTACTOS DEL BARRIO ######
        filtro = (df['page'] == 'Botonera Tipo Contacto - G5') & (df['message'] == '1')
        df.loc[filtro, 'Menu Principal'] = 'Contactos Útiles'
        df.loc[filtro, 'Menu Secundario'] = 'Contactos del Barrio'  
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'

        ###### EMPRENDEDORES ######
        filtro = (df['page'] == 'Botonera Tipo Contacto - G5') & (df['message'] == '2')
        df.loc[filtro, 'Menu Principal'] = 'Contactos Útiles'
        df.loc[filtro, 'Menu Secundario'] = 'Emprendedores'
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'

        ###### COMERCIOS ######
        filtro = (df['page'] == 'Botonera Tipo Contacto - G5') & (df['message'] == '3')
        df.loc[filtro, 'Menu Principal'] = 'Contactos Útiles'
        df.loc[filtro, 'Menu Secundario'] = 'Comercios'
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'

        ###### VOLVER ######
        filtro = (df['page'] == 'Botonera Tipo Contacto - G5') & (df['message'] == '0')
        df.loc[filtro, 'Menu Principal'] = 'Contactos Útiles'
        df.loc[filtro, 'Menu Secundario'] = 'Volver'  
        df.loc[filtro, 'Menu Terciario'] = 'Volver'  

 
        
    except Exception as e:
        logging.warn(f'Error menu_Contactos() {e}')

def menu_Ventas(df):
    """  """
    try:
        #### Comprar ####
        filtro = (df['page'] == 'Ventas y Alquileres') & (df['message'] == '1')
        df.loc[filtro, 'Menu Principal'] = 'Ventas'
        df.loc[filtro, 'Menu Secundario'] = 'Comprar'  
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'

        #### Alquilar ####
        filtro = (df['page'] == 'Ventas y Alquileres') & (df['message'] == '2')
        df.loc[filtro, 'Menu Principal'] = 'Ventas'
        df.loc[filtro, 'Menu Secundario'] = 'Alquilar'  
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'        

        #### Ceder/Vender ####
        filtro = (df['page'] == 'Ventas y Alquileres') & (df['message'] == '3')
        df.loc[filtro, 'Menu Principal'] = 'Ventas'
        df.loc[filtro, 'Menu Secundario'] = 'Ceder/Vender'  
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'            

        #### Volver ####
        filtro = (df['page'] == 'Ventas y Alquileres') & (df['message'] == '0')
        df.loc[filtro, 'Menu Principal'] = 'Ventas'
        df.loc[filtro, 'Menu Secundario'] = 'Volver'  
        df.loc[filtro, 'Menu Terciario'] = 'Volver'   


    except Exception as e:
        logging.warn(f'Error menu_ventas: {e}')

def menu_OtrasConsultas(df):
    """
    Función menu_OtrasConsultas procesa todos los clientes que ingresaron al menu Otras Consultas y 
    los clasifica mediante palabras clave, guardando todo en el dataframe.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    try:
                        ###### MENU OTRAS CONSULTAS ###### 
            # Derivados 
        filtro = (df['page'] == 'Consulta o reclamo') & (df['user'] != 'system') # filtro
        df_otrasconsultas = df.loc[filtro]
        idChats_otrasconsultas1 = df_otrasconsultas['idChat']
        df.loc[filtro, 'Menu Principal'] = 'Otras Consultas'
        df.loc[filtro, 'Menu Secundario'] = 'Sin Reclamo Anterior'
        df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'

            # Respuesta automatica por nro de Caso
        filtro = (df['page'] == 'CASO DERIVADO')  # filtro
        df_otrasconsultas = df.loc[filtro]
        idChats_otrasconsultas2 = df_otrasconsultas['idChat']
        df.loc[filtro, 'Menu Principal'] = 'Otras Consultas'
        df.loc[filtro, 'Menu Secundario'] = 'Con Reclamo Anterior'
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'

            # Con Reclamo pero sin numero
        filtro = (df['page'] == 'Derivación por error Regex') | (df['intent'] == 'sin-numero') 
        df_otrasconsultas = df.loc[filtro]
        idChats_otrasconsultas3 = df_otrasconsultas['idChat']
        df.loc[filtro, 'Menu Principal'] = 'Otras Consultas'
        df.loc[filtro, 'Menu Secundario'] = 'Con Reclamo Anterior'
        df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'

                        ###### ABANDONAN ######
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '7') & (~df['idChat'].isin(idChats_otrasconsultas1)) & (~df['idChat'].isin(idChats_otrasconsultas2)) & (~df['idChat'].isin(idChats_otrasconsultas3))
        df.loc[filtro, 'Menu Principal'] = 'Otras Consultas'
        df.loc[filtro, 'Menu Secundario'] = 'Abandonan'
        df.loc[filtro, 'Menu Terciario'] = 'Abandonan' 

    except Exception as e:
        logging.warn(f'Error menu_OtrasConsultas(): {e}')   

#    try:
#        ISharePoint().download_ExcelDarwin()
#    except Exception as e: print("Error al actualizar DarwinExcel ", e)
    
    try:

                        ###### FILTRO PALABRAS ######
        # Lee todas las hojas del archivo Excel en un diccionario de DataFrames
        dataframes_por_hoja = pd.read_excel(archivo_excel, sheet_name=None, engine='openpyxl')
        # Itera a través de las hojas
        for hoja, dataframe in dataframes_por_hoja.items():
            if not dataframe.empty:
                primera_columna = dataframe.iloc[1:, 1].to_numpy()  # Selecciona la segunda columna
                buscar_palabras(df, primera_columna, hoja) 
                print(f'Hoja: {hoja}') # Hojas detectadas
        
        # Inclasificables
        filtro_inclasificables(df)

        

    except Exception as e:
        logging.warn(f'Error en Filtro de Palabras de Otras Consultas {e}')

          
        


def reclamo(df):
    """
    Función reclamo que procesa todos los clientes que les consultamos si su reclamo fue resuelto
    con su posteriores elecciones guardandolos en el dataframe.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    try:
                # Consultas Enviadas    
        filtro = df['message'].str.contains('¿Tu reclamo o consulta fue resuelto?')
        df.loc[filtro,'Reclamo'] = 'Encuesta Incompleta'

        # Respuestas Enviadas
        ### SI
        filtro = (df['page'] == 'Encuesta 2 - B1') & (df['intent'] == 'opcion-si')
        df_idChats = df.loc[filtro]
        idchats = df_idChats['idChat']
        filtro1 = (df['idChat'].isin(idchats)) & (df['Reclamo'].notnull()) 
        df.loc[filtro1, 'Reclamo'] = 'Si' 
        df.loc[filtro1,'Encuesta'] = 'Encuesta Incompleta' 

        ### NO
        filtro = (df['page'] == 'Encuesta 2 - B1') & (df['intent'] == 'opcion-no') & ((df['message'] == 'no') | (df['message'] == 'No'))
        df_idChats = df.loc[filtro]
        idchats = df_idChats['idChat']
        filtro1 = (df['idChat'].isin(idchats)) & (df['Reclamo'].notnull()) 
        df.loc[filtro1, 'Reclamo'] = 'No' 

        # Encuestas Incompletas
        """ 
        Aca se marcan por adelantado la gente que realizo el feedback positivo de reclamo
        por lo tanto deberian pasar a la encuesta para calificar, si abandonan o no responden bien, quedaran marcados como
        Encuesta Incompleta 
        """
        filtro = df['message'].str.contains('¿Tu reclamo o consulta fue resuelto?')
        df_idchats_reclamo = df.loc[filtro]
        idchats_reclamo = df_idchats_reclamo['idChat']
        filtro = (df['Reclamo'] == 'Si')
        df.loc[filtro,'Encuesta'] = 'Encuesta Incompleta' 
        

    except Exception as e:
            logging.warn(f'Error en procesar reclamos {e}')
              
def encuesta(df):
    """
    Función encuesta que procesa todos los clientes que les consultamos la puntuacion de la atencion
    con su posteriores elecciones guardandolos en el dataframe.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    try:
        filtro = (df['page'] == 'Calificacion - B2') & (df['message'] == 'Muy Satisfecha/o')
        df_idChats = df.loc[filtro]
        idchats = df_idChats['idChat']
        filtro1 = (df['idChat'].isin(idchats)) & (df['Reclamo'].notnull())
        df.loc[filtro1, 'Encuesta'] = 'Muy Satisfecha/o'
      

        filtro = (df['page'] == 'Calificacion - B2') & (df['message'] == 'Satisfecha/o')
        df_idChats = df.loc[filtro]
        idchats = df_idChats['idChat']
        filtro1 = (df['idChat'].isin(idchats)) & (df['Reclamo'].notnull())
        df.loc[filtro1, 'Encuesta'] = 'Satisfecha/o'
       

        filtro = (df['page'] == 'Calificacion - B2') & (df['message'] == 'Insatisfecha/o')
        df_idChats = df.loc[filtro]
        idchats = df_idChats['idChat']
        filtro1 = (df['idChat'].isin(idchats)) & (df['Reclamo'].notnull())
        df.loc[filtro1, 'Encuesta'] = 'Insatisfecha/o'


        filtro = (df['page'] == 'Calificacion - B2') & (df['message'] == 'Muy Insatisfecha/o')
        df_idChats = df.loc[filtro]
        idchats = df_idChats['idChat']
        filtro1 = (df['idChat'].isin(idchats)) & (df['Reclamo'].notnull())
        df.loc[filtro1, 'Encuesta'] = 'Muy Insatisfecha/o'

    except Exception as e:
        logging.warn(f'Error en procesar encuestas {e}')


def perdidos(df):
    """
    Función perdidos que procesa todos los clientes que se perdieron en el menu y dejaron de contestar
    guardandolos en el dataframe.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    try:
        # Todos los que derivan
        filtro = (df['message'].str.contains("derivacion",case=False, na=False)) & (df['user']!= 'system') 
        #df.loc[filtro,'user'] = df['room']
        df_idChats = df.loc[filtro]
        idChats_todos = df_idChats['idChat'] # idChats que recibieron el mensaje
        # Los que tienen el 3er Menu Completo
        filtro = (df['idChat'].isin(idChats_todos)) & (df['Menu Terciario'].notnull())  
        df_idChats_completos3 = df[filtro] # entonces de esos idChats cuales tienen al menos un 3er menu completo
        idChats_completos3 = df_idChats_completos3['idChat'] # y aca en version lista

        # Los que tienen el 3er Menu Vacio
        filtro = (df['idChat'].isin(idChats_todos)) & (df['Menu Secundario'].notnull()) & (df['Menu Terciario'].isnull()) 
        # Si salieron de algun flujo y no le marcaron el tercer menu y fueron derivados, aca entran como derivados error
        df.loc[filtro,'Menu Terciario'] = 'Derivados Error'

        # Los que tienen el 2do Menu Vacio
        df_idChats_confundidos3 = df[filtro]
        idChats_confundidos3 = df_idChats_confundidos3['idChat'] # 3er menu vacio
        df_idChats_sobra3 = df_idChats[~df_idChats['idChat'].isin(idChats_confundidos3) & (~df_idChats['idChat'].isin(idChats_completos3))] # 2do = Todos - 3ro vacio - 3ro completo
        idChats_sobra3 = df_idChats_sobra3['idChat']
        filtro = (df['idChat'].isin(idChats_sobra3)) & (df['Menu Principal'].notnull()) & (df['Menu Secundario'].isnull()) & (df['Menu Terciario'].isnull())  # Solo los que tienen 2do Vacio
        df.loc[filtro,'Menu Secundario'] = 'Derivados Error'
        df.loc[filtro,'Menu Terciario'] = 'Derivados Error'

        df_idChats_confundidos2 = df[filtro] 
        idChats_confundidos2 = df_idChats_confundidos2['idChat'] # 2do Vacio
        df_idChats_confundidos1 = df_idChats_sobra3[(~df_idChats_sobra3['idChat'].isin(idChats_confundidos2)) & (~df_idChats_sobra3['idChat'].isin(idChats_completos3))] # Los que sobraron del tercer menu vacio, menos los que sobraron en el segundo menu vacio, menos los que tenian 3 menus completos
        idChats_confundidos1 = df_idChats_confundidos1['idChat']
        filtro = (df['idChat'].isin(idChats_confundidos1)) & ((df['message'].str.contains("deriva")) or (df['message'].str.contains("ejecutivo")))
        #df.loc[filtro,'user'] = df['room']
        df.loc[filtro,'Menu Principal'] = 'Derivados Error'
        df.loc[filtro,'Menu Secundario'] = 'Derivados Error'
        df.loc[filtro,'Menu Terciario'] = 'Derivados Error'

        # Se pierden en el 3er Menu
        df_completados = df.loc[(df['Menu Terciario'].notnull()) | (df['Menu Principal'] == 'Feedback')]
        idChats_completados = df_completados['idChat'] 
        df_iniciados = df.loc[df['Menu Principal'].notnull()] # Todos los idChats que entraron al menu

        df_idChats_perdidos = df_iniciados[~df_iniciados['idChat'].isin(idChats_completados)] # df con idchat que no llegaron a menu Terciario
        idChatsperdidos = df_idChats_perdidos['idChat'] # idChats que no llegaron a menu Terciario

        # No finalizaron el 3er Menu (tienen 1er y 2do Menu)
        filtro = (df['idChat'].isin(idChatsperdidos)) & (df['Menu Secundario'].notnull()) & (df['Menu Terciario'].isnull())
        df.loc[filtro, 'Menu Terciario'] = 'Abandonan'

        # Se pierden en el 2do Menu (tienen 1er Menu)
        df_idChats_perdidos3 =  df.loc[filtro]
        idChats3 = df_idChats_perdidos3['idChat']
        df_idChats_perdidos2 =df_idChats_perdidos[~df_idChats_perdidos['idChat'].isin(idChats3)]
        idChats_perdidos2 = df_idChats_perdidos2['idChat']

        menus = ['Servicios e Impuestos','Otras Consultas','Expensas', 'Obras','Contactos Útiles','Ventas','Cesiones']
        filtro = (df['idChat'].isin(idChats_perdidos2)) & (df['Menu Secundario'].isnull()) & (df['Menu Terciario'].isnull() )& (df['Menu Principal'].isin(menus))# & (df['Menu Principal']!='Feedback')
        df.loc[filtro, 'Menu Secundario'] = 'Abandonan'
        df.loc[filtro, 'Menu Terciario'] = 'Abandonan'

    except Exception as e:
        logging.warn(f'Error en procesar perdidos {e}')

def no_ingresan(df):
    """
    Función que procesa todos los clientes que inicializaron una conversacion pero no avanzaron a ningun lado
    guardandolos en el dataframe.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    try:
        df_ingresan = df.loc[df['Menu Principal'].notnull()]
        id_ingresan = df_ingresan['idChat']
        filtro = (~df['idChat'].isin(id_ingresan)) & (df['message'] == 'Te estuve esperando... Si querés seguir chateando, volvé a escribirme "hola". Si no escribime de nuevo cuando quieras.')
        df.loc[filtro, 'Menu Principal'] = 'Abandonan'
        df.loc[filtro, 'Menu Secundario'] = 'Abandonan'
        df.loc[filtro, 'Menu Terciario'] = 'Abandonan'



    except Exception as e:
        logging.warn(f'Error en procesar no_ingresan {e}')


def buscar_palabras(df, palabras_clave, valor_asignar):
    """
    Función que busca en la columna message de los clientes que dejaron su 'Otras Consultas' palabras clave 
    y si encuentra le agrega valor_asignar a esa fila

    Parámetros:
    - df: Dataframe con todos los datos 
    - palabras_clave: str de palabras que se quiere buscar
    - valor_asignar: str que se coloca en las filas que contiene alguna de las palabras_clave
    """
    try:
        # Filtro
        filtro = (df['page'] == 'Consulta o reclamo') & (df['user'] != 'system')

        # Crear una copia temporal de la columna 'message' para aplicar las modificaciones
        df['message_temp'] = df.loc[filtro, 'message'].apply(lambda x: unidecode(x.lower()).replace('.', ' ').replace(',', ' ').replace(';', ' '))


        # Normalizacion de la lista de palabras
        lista_minusculas = [elemento.lower() for elemento in palabras_clave]
        lista_sin_acentos = [unidecode(elemento) for elemento in lista_minusculas]
        lista_esp = [' ' + elemento + ' ' for elemento in lista_sin_acentos]


        # Iterar a través de cada fila del dfFrame
        for index, row in df.loc[filtro].iterrows():
            for palabra in lista_esp:
                row_esp = " " + row["message_temp"] + " " # Agregar un espaciado al principio y final de cada mensaje
                if palabra in row_esp:
                    df.at[index, "Otras Consultas"] = valor_asignar

        # Eliminar la columna temporal 'message_temp'
        df.drop(columns=['message_temp'], inplace=True)

    except Exception as e:
        logging.warn(f'Error en buscar palabras de Otras Consultas {e}')

def filtro_inclasificables(df):
    try:
        filtro = (df['page'] == 'Menu Otras Consultas') & (df['user'] != 'system') #Filtro mnje otras consultas
        df['cont_message_temp'] = df.loc[filtro, 'message'].str.split().apply(len) # Creo copia temporal

        filtro = (df['cont_message_temp'] <= 2) & (df['Otras Consultas'].isnull())
        df.loc[filtro, 'Otras Consultas'] = '(INCLASIFICABLE)'

    except Exception as e:
        logging.warn(f'Error en filtro_inclasificables de palabras {e}')

def fuera_de_horario(df):
    """ 
    Esta funcion se encarga de encontrar y clasificar los usuarios que, luego de recorrer el menu, y a la hora de derivarlos a
    un ascesor, se encuentran fuera de horario, por lo tanto no son atendidos...
    """
    try:
        filtro = (df['page'] == 'End Session') & (df['agent'] == 'derivacion')
        df_fh = df.loc[filtro]
        idChats_todos = df_fh['idChat']
            # Los que tienen el 3er Menu Vacio
        filtro = (df['idChat'].isin(idChats_todos)) & (df['Menu Secundario'].notnull()) & (df['Menu Terciario'].isnull()) 
        df.loc[filtro,'Menu Terciario'] = 'Fuera de Horario'

        # Los que tienen el 2do Menu Vacio
        df_idChats_confundidos3 = df[filtro]
        idChats_confundidos3 = df_idChats_confundidos3['idChat'] # 3ro
        df_idChats_sobra3 = df_fh[~df_fh['idChat'].isin(idChats_confundidos3)] # 2do = Todos - 3ro
        idChats_sobra3 = df_idChats_sobra3['idChat']
        filtro = (df['idChat'].isin(idChats_sobra3)) & (df['Menu Principal'].notnull()) & (df['Menu Secundario'].isnull()) # Solo los que tienen 2do Vacio
        df.loc[filtro,'Menu Secundario'] = 'Fuera de Horario'
        df.loc[filtro,'Menu Terciario'] = 'Fuera de Horario'

        df_idChats_confundidos2 = df[filtro] 
        idChats_confundidos2 = df_idChats_confundidos2['idChat'] # 2do Vacio
        df_idChats_confundidos1 = df_idChats_sobra3[~df_idChats_sobra3['idChat'].isin(idChats_confundidos2)]
        idChats_confundidos1 = df_idChats_confundidos1['idChat']
        filtro = (df['idChat'].isin(idChats_confundidos1)) & (df['message'].str.contains("En este momento no podemos atenderte. Nuestro horario de atención es"))
        df.loc[filtro,'user'] = df['room']
        df.loc[filtro,'Menu Principal'] = 'Fuera de Horario'
        df.loc[filtro,'Menu Secundario'] = 'Fuera de Horario'
        df.loc[filtro,'Menu Terciario'] = 'Fuera de Horario'

    except Exception as e:
        logging.warning(f'Error fuera_de_horario {e}')