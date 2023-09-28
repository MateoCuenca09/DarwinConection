import pandas as pd
import os
from datetime import datetime, timedelta
from unidecode import unidecode
from MIguardar import guardar_historico

def mainPBI(datos):
    """
    Función principal de PBI_functions que procesa y guarda en .xlsx los datos.

    Parámetros:
    - Datos: Archivo .json con datos de conversaciones
    """
    # Transformamos los datos a un DataFrame
    df = pd.DataFrame(datos)

    # Asegurémonos de que la columna 'date' sea de tipo datetime
    df['date'] = pd.to_datetime(df['date'])

    # Eliminar la zona horaria de la columna 'date'
    df['date'] = df['date'].dt.tz_convert(None)


    # Procesamos los datos segun importancia
    menu_Principal(df)
    menu_Secundario(df)
    Feedback(df)
    perdidos(df)
    no_ingresan(df)

    #df = df[df['user'] != 'system'] # Mantener solo los mensajes de clientes
    df = df.drop(['type','channel','darwinChatID','page','__v','intent','endpoint','typeClose'], axis=1) # Quitamos datos inecesarios


    guardar_historico(df)


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
    menu_Contactos(df)
    menu_Servicios(df)
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
        df.loc[filtro, 'Menu Secundario'] = 'Resueltos x Sistema'
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'



    except Exception as e:
        print("Error al procesar menuAcesos:", e)

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
        filtro = df['message'].str.startswith("Tu ID de expensas es:")
        df_idexp = df.loc[filtro]
        idChats_idexp = df_idexp['idChat']
        filtro = (df['idChat'].isin(idChats_idexp)) & (df['Menu Secundario'] == 'ID Expensas')
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'
        df.loc[filtro, 'user'] = df['room']

        ######  EXPENSA CORRIENTE ######
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '2')
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Secundario'] = 'Expensa Corriente'
        
            # Encuentra ID Expensas
        filtro = (df['page'] == 'Archivo Expensa')
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Secundario'] = 'Expensa Corriente'
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'
        df.loc[filtro, 'user'] = df['room'] 

            # No encuentra y Deriva a asesor
        filtro = df['message'].str.startswith("No pudimos encontrar un ID de expensa con esos datos.")
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Secundario'] = 'ID Expensas'
        df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'
        df.loc[filtro, 'user'] = df['room']


        ###### ACTUALIZAR CUPON ######
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '3')
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Secundario'] = 'Actualizar Cupon'


        ###### PLAN DE PAGOS ######
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '4')
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Secundario'] = 'Plan de Pagos'


        ###### OTRAS CONSULTAS ######
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '5')
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Secundario'] = 'Otras Consultas'
        

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

        ###### Derivados ######
        filtro = df['message'].str.startswith("¡Gracias! Te voy a derivar con un asesor para que resuelva tu consulta.")
        df_derivados = df.loc[filtro]
        idChats = df_derivados['idChat']
        filtro = (df['Menu Principal'] == 'Expensas') & (df['Menu Secundario'].notnull()) & (df['idChat'].isin(idChats)) & (df['Menu Terciario'].isnull())
        df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'
        
    except Exception as e:
        print("Error menu_Expensas(): ",e)


def menu_Obras(df):
    """
    Función menu_Obras que procesa todos los clientes que ingresaron al menu Obras y su posteriores elecciones guardandolos en el dataframe.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    try:
        ###### INSTRUCTIVO DE OBRA ######
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '1')
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Instructivo de obra'
            # Resuelto x Sistema
        filtro = df['message'].str.startswith("Acá te envío el link para que puedas acceder al instructivo de obra para tu emprendimento:")
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Instructivo de obra'
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'
        df.loc[filtro, 'user'] = df['room']
            # Resuelto x Sistema V2
        filtro = df['message'].str.startswith("Para acceder al Instructivo de obra")
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Instructivo de obra'
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'
        df.loc[filtro, 'user'] = df['room']




        ###### FIRMA DE BOLETO ######
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '2')
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Firma de boleto'


        ###### FIRMA DE POSESION ######
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '3')
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Firma de posesión'


        ###### AMOJONADO ######
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '4')
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Amojonado'


        ###### TAREAS PREVIAS ######
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '5')
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Tareas previas'


        ###### REGISTRAR OBRA NUEVA ######
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '6')
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Registrar obra nueva'
        # Resuelto x Sistema
        filtro = df['message'].str.startswith("Acá te envío el link para que puedas acceder al formulario de registro de legajo de obra:")
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Registrar obra nueva'
        df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'
        df.loc[filtro, 'user'] = df['room']


        ###### OTRAS CONSULTAS ######
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '7')
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Otras consultas'


        ###### VOLVER ######
        filtro = (df['page'] == 'Obras - Motivo de Contacto - D2') & (df['message'] == '0')
        df.loc[filtro, 'Menu Principal'] = 'Obras'
        df.loc[filtro, 'Menu Secundario'] = 'Volver'        
        df.loc[filtro, 'Menu Terciario'] = 'Volver'  


        ###### Derivados ######
        filtro = df['message'].str.startswith("¡Gracias! Te voy a derivar con un asesor para que resuelva tu consulta.")
        df_derivados = df.loc[filtro]
        idChats = df_derivados['idChat']
        filtro = (df['Menu Principal'] == 'Obras') & (df['Menu Secundario'].notnull()) & (df['idChat'].isin(idChats)) & (df['Menu Terciario'].isnull())
        df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'      

    except Exception as e:
        print("Error menu_Amojonado(): ",e)

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
        filtro = df['message'].str.startswith("¡Gracias! Te voy a derivar con un asesor para que resuelva tu consulta.")
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
        print("Error menu_Cesiones(): ",e)

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
        print("Error menu_Servicios(): ",e)

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
        print("Error menu_Contactos(): ",e)

def menu_OtrasConsultas(df):
    """
    Función menu_OtrasConsultas procesa todos los clientes que ingresaron al menu Otras Consultas y 
    los clasifica mediante palabras clave, guardando todo en el dataframe.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    try:
                        ###### MENU OTRAS CONSULTAS ###### 
        filtro = (df['page'] == 'Menu Otras Consultas') & (df['user'] != 'system')
        df_otrasconsultas = df.loc[filtro]
        idChats_otrasconsultas = df_otrasconsultas['idChat']
        df.loc[filtro, 'Menu Principal'] = 'Otras Consultas'
        df.loc[filtro, 'Menu Secundario'] = 'Derivados Bot'
        df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'

                        ###### ABANDONAN ######
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '7') & (~df['idChat'].isin(idChats_otrasconsultas))
        df.loc[filtro, 'Menu Principal'] = 'Otras Consultas'
        df.loc[filtro, 'Menu Secundario'] = 'Abandonan'
        df.loc[filtro, 'Menu Terciario'] = 'Abandonan'    

                        ###### FILTRO PALABRAS ######
        # Especifica la ruta de tu archivo Excel con Palabras Clave 
        archivo_excel ='C:/Users/cuenc/OneDrive - EDISUR SA/Mateo Cuenca/DarwinConection/.ignore/Excel Darwin - PBI - V3.xlsx'
        ""'O:/Gestion y Experiencia del Cliente/5. SERVICIO DE ATENCIÓN AL CLIENTE/11. TRANSFORMACIÓN DIGITAL/Excel - Otras Consultas/Excel Darwin - PBI - Automatico.xlsx'""
        ""'C:/Users/cuenc/OneDrive - EDISUR SA/Mateo Cuenca/DarwinConection/.ignore/Excel Darwin - PBI - V3.xlsx'""

        # Lee todas las hojas del archivo Excel en un diccionario de DataFrames
        dataframes_por_hoja = pd.read_excel(archivo_excel, sheet_name=None, engine='openpyxl')
        # Itera a través de las hojas
        for hoja, dataframe in dataframes_por_hoja.items():
            if not dataframe.empty:
                primera_columna = dataframe.iloc[1:, 1].to_numpy()  # Selecciona la segunda columna
                buscar_palabras(df, primera_columna, hoja) 
                print(f'Hoja: {hoja}') # Hojas detectadas



    except Exception as e:
        print("Error levantar palabras menu_OtrasConsultas()")

        filtro = (df['page'] == 'Menu Otras Consultas') & (df['user'] != 'system')
        df_otrasconsultas = df.loc[filtro]
        idChats_otrasconsultas = df_otrasconsultas['idChat']
        df.loc[filtro, 'Menu Principal'] = 'Otras Consultas'
        df.loc[filtro, 'Menu Secundario'] = 'Derivados Bot'
        df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'

        menu_OtrasConsultasERROR(df,idChats_otrasconsultas) # Si falla el levantar palaras hacemos menu_OtrasConsultas anterior
          
        


def reclamo(df):
    """
    Función reclamo que procesa todos los clientes que les consultamos si su reclamo fue resuelto
    con su posteriores elecciones guardandolos en el dataframe.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    try:
                # Consultas Enviadas    
        filtro = df['message'] == '¿Tu reclamo o consulta fue resuelto? Si No'
        df_idchats_reclamo = df.loc[filtro]
        idchats_reclamo = df_idchats_reclamo['idChat']
        filtro = (df['idChat'].isin(idchats_reclamo)) & (df['Menu Terciario'].notnull())
        df.loc[filtro,'Reclamo'] = 'Encuesta Incompleta'



        # Respuestas Enviadas
        ### SI
        filtro = (df['page'] == 'Encuesta 2 - B1') & (df['message'] == 'Si')
        df_idChats = df.loc[filtro]
        idchats = df_idChats['idChat']
        filtro1 = (df['idChat'].isin(idchats)) & (df['Menu Terciario'].notnull()) 
        df.loc[filtro1, 'Reclamo'] = 'Si' 

        filtro = (df['page'] == 'Encuesta 2 - B1') & (df['message'] == 'si')
        df_idChats = df.loc[filtro]
        idchats = df_idChats['idChat']
        filtro1 = (df['idChat'].isin(idchats)) & (df['Menu Terciario'].notnull()) 
        df.loc[filtro1, 'Reclamo'] = 'Si' 

        ### NO
        filtro = (df['page'] == 'Encuesta 2 - B1') & (df['message'] == 'No')
        df_idChats = df.loc[filtro]
        idchats = df_idChats['idChat']
        filtro1 = (df['idChat'].isin(idchats)) & (df['Menu Terciario'].notnull()) 
        df.loc[filtro1, 'Reclamo'] = 'No' 

        filtro = (df['page'] == 'Encuesta 2 - B1') & (df['message'] == 'no')
        df_idChats = df.loc[filtro]
        idchats = df_idChats['idChat']
        filtro1 = (df['idChat'].isin(idchats)) & (df['Menu Terciario'].notnull()) 
        df.loc[filtro1, 'Reclamo'] = 'No' 

        # Encuestas Incompletas
        filtro = df['message'] == '¿Tu reclamo o consulta fue resuelto? Si No'
        df_idchats_reclamo = df.loc[filtro]
        idchats_reclamo = df_idchats_reclamo['idChat']
        filtro = (df['idChat'].isin(idchats_reclamo)) & (df['Reclamo'] == 'Si')
        df.loc[filtro,'Encuesta'] = 'Encuesta Incompleta'
        

    except Exception as e:
            print("Error reclamo(): ",e)
              
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

        #encuesta_Incompleta(df)

    except Exception as e:
        print("Error encuesta(): ",e)


def encuesta_Incompleta(df):
    """
    Función encuesta_Incompleta que procesa todos los clientes que les consultamos  y no respondieron 
    guardandolos en el dataframe.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    try:
                # No Responden Reclamo
        filtro = (df['Menu Principal'] == 'Feedback') & (df['Encuesta'].isnull()) & (df['Reclamo'].isnull())
        df.loc[filtro,'Reclamo'] = 'Encuesta Incompleta'

                # No responden Encuesta Gestion
        filtro = (df['Menu Principal'] == 'Feedback') & (df['Encuesta'].isnull()) & (df['Reclamo'] == 'Si')
        df.loc[filtro,'Encuesta'] = 'Encuesta Incompleta'

    except Exception as e:
        print("Error encuesta_Incompleta(): ",e)

def perdidos(df):
    """
    Función perdidos que procesa todos los clientes que se perdieron en el menu y dejaron de contestar
    guardandolos en el dataframe.

    Parámetros:
    - df: Dataframe con todos los datos 
    """
    try:
        # Envian mal 3 mensajes seguidos
        # Todos los que derivan
        filtro = df['message'].str.endswith("¡No te preocupes! Te derivo con un asesor…")
        df.loc[filtro,'user'] = df['room']
        df_idChats = df.loc[filtro]
        idChats_todos = df_idChats['idChat']
        # Los que tienen el 3er Menu Vacio
        filtro = (df['idChat'].isin(idChats_todos)) & (df['Menu Secundario'].notnull()) & (df['Menu Terciario'].isnull()) 
        df.loc[filtro,'Menu Terciario'] = 'Derivados Error'

        # Los que tienen el 2do Menu Vacio
        df_idChats_confundidos3 = df[filtro]
        idChats_confundidos3 = df_idChats_confundidos3['idChat'] # 3ro
        df_idChats_sobra3 = df_idChats[~df_idChats['idChat'].isin(idChats_confundidos3)] # 2do = Todos - 3ro
        idChats_sobra3 = df_idChats_sobra3['idChat']
        filtro = (df['idChat'].isin(idChats_sobra3)) & (df['Menu Principal'].notnull()) & (df['Menu Secundario'].isnull()) # Solo los que tienen 2do Vacio
        df.loc[filtro,'Menu Secundario'] = 'Derivados Error'
        df.loc[filtro,'Menu Terciario'] = 'Derivados Error'

        df_idChats_confundidos2 = df[filtro] 
        idChats_confundidos2 = df_idChats_confundidos2['idChat'] # 2do Vacio
        df_idChats_confundidos1 = df_idChats_sobra3[~df_idChats_sobra3['idChat'].isin(idChats_confundidos2)]
        idChats_confundidos1 = df_idChats_confundidos1['idChat']
        filtro = (df['idChat'].isin(idChats_confundidos1)) & (df['message'].str.endswith("¡No te preocupes! Te derivo con un asesor…"))
        df.loc[filtro,'user'] = df['room']
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
        print('Error perdidos(): ',e)

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
        filtro = ~df['idChat'].isin(id_ingresan)
        df.loc[filtro, 'Menu Principal'] = 'Abandonan'
        df.loc[filtro, 'Menu Secundario'] = 'Abandonan'
        df.loc[filtro, 'Menu Terciario'] = 'Abandonan'



    except Exception as e:
        print("Error no_ingresan(): ",e)


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
        filtro = (df['page'] == 'Menu Otras Consultas') & (df['user'] != 'system')

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
        print("Error buscar_palabras(): ",e)


def menu_OtrasConsultasERROR(df,idChats_otrasconsultas):
#### CLASIFICACION DE OTRAS CONSULTAS ####
        # EXPENSAS
        key_expensas = [
            'abonar expensa',
            'abonar las expensa',
            'adeuda de expensa',
            'aumento de expensas',
            'autogestión',
            'autogestion expensas',
            'bajar las expensas',
            'cobrar las expensas',
            'cobrar expensas',
            'código electronico',
            'cupon',
            'cupon de expensas',
            'cupón de pago',
            'descargar las expensas',
            'deuda de expensas',
            'desmalezado',
            'expensas',
            'expensa',
            'expensas anteriores',
            'Expensa corriente',
            'expensa inactiva',
            'expensa vigente',
            'ID de expensa',
            'ID expensa',
            ' ID ',
            'importe de expensas',
            'inactiva',
            'libre deuda de expensas',
            'mercado pago',
            'numero de ID',
            'pagar expensas',
            'pagar las expensas',
            'pago electronico',
            'pago mis cuentas',
            'tema de expensas',
            'última expensa',
            'últimas expensas',
            'vencimiento'
        ]
        valor_asignar = 'Expensas'

        buscar_palabras(df, key_expensas, valor_asignar)

        # INICIO OBRA - AMOJONADO
        key_obras = [
            'acta de replanteo',
            'acta de tenencia',
            'amojonar',
            'amojonado',
            'amojonamiento',
            'avance de la obra',
            'avance de obra',
            'cercado el lote',
            'cercar el lote',
            'comenzar una obra',
            'comienzo de obra',
            'comienzo la obra',
            'conexión de luz',
            'conexión provisoria',
            'iniciar la obra',
            'iniciar obra',
            'iniciar una obra',
            'inicio de obra',
            'instructivo de obra',
            'legajo de obra',
            'nomenclatura',
            'tareas preliminares',
            'tareas previas',
            'acometida',
            'acometida de luz',
            'acometidas',
            'alta de servicio',
            'cloaca',
            'cloacas',
            'conexión de epec',
            'conexión de la luz',
            'conexión epec',
            'conexiones',
            'construir',
            'ecogas',
            'energía eléctrica',
            'epec',
            'firma',
            'firma de boleto',
            'gas natural',
            'inicio obra',
            'PCT',
            'PIG',
            'pilar',
            'pilares',
            'plano',
            'planos',
            'posesion',
            'posesiones',
            'pozo',
            'pedir la luz',
            'firmar',
            'boleto de venta',
            'preensamblado',
            'ensamblado',
            'lote esquina',
            'doble frente',
            'plancheta catastral',
            'obra gas',
            'normativa de edificacion',
            'terminada la obra',
            'conexión electrica',
            'conexiones electricas',
            'conectar la luz',
            'factibilidad de gas',
            'factibilidad',
            'especies',
            'permiso de obra',
            'dimensiones del terreno',
            'dimensiones del lote',
            'colindantes',
            'avance del servicio',
            'energia electrica definitiva',
            'cerramiento',
            'obrador',
            'baño quimico',
            'acopio de materiales',
            'anexo I y II',
            'anexo i y ii ',
            'certificado de amojonado',
            'certificado de amojonamiento',
            'conexión de servicio eléctrico',
            'red electrica',
        ]
        valor_asignar = 'Inicio Obras'
        buscar_palabras(df, key_obras, valor_asignar)

        # CESION INMUEBLE
        key_cesiones = [
            'autorizacion de venta',
            'autorizacion para ceder',
            'cedente',
            ' ceder',
            'cesion',
            'cesionario',
            'cesiones',
            'nuevo propietario',
        ]
        
        valor_asignar = 'Cesiones'
        buscar_palabras(df, key_cesiones, valor_asignar)

        # SERVICIOS E IMPUESTOS
        key_servicios = [
            'cuenta de rentas',
            'cuentas de rentas',
            'impuesto municipal',
            'impuestos municipales',
            'inmobiliario municipal',
            'impuesto de rentas',
            'impuestos de rentas',
            'impuesto municipal',
            'impuestos municipales',
            'numero de identificacion',
            'rentas',
            'uf aguas cordobesas',
            'unidad de facturación',
            'unidaddes de facturacion',
        ]
        valor_asignar = 'Servicios e Impuestos'
        buscar_palabras(df, key_servicios, valor_asignar)

        # CONTACTOS UTILES
        key_contactos = [
            'telefono del intendente'
        ]
        valor_asignar = 'Contactos Utiles'
        buscar_palabras(df, key_contactos, valor_asignar)

        # POSVENTA
        key_posventa = [
            'abertura',
            'aire',
            'aire acondicionado',
            'balcón',
            'caldera',
            'calefacción',
            'cocina',
            'electrodomestico',
            'electrodomesticos',
            'fisura',
            'horno',
            'humedad',
            'hundimiento',
            'lámpara',
            'lavarropas',
            'llave',
            'llave de paso',
            'mancha',
            'pared',
            'pintura',
            'portero',
            'portero eléctrico',
            'puerta',
            'quemada',
            'quemado',
            'quemados',
            'radiadores',
            'rajadura',
            'secador',
            'solar',
            'tanque',
            'techo',
            'timbre',
            'velas',
            'ventana',
            'pileta de inspección',
            'techo del balcón',
            'roturas de durlock',
            'problemas estructurales',
            'durlock',
            'cañeria',
            'pierde',
            'piso de arriba',
            'lavatorio',
            'muebles',
            'artefactos',
            'machimbre',
            'cielorraso',
            'galeria',
            'cielo raso',
            'actividades de visitas',
            'visitar el inmueble',
            'numeracion',
        ]
        valor_asignar = 'Posventa'
        buscar_palabras(df, key_posventa, valor_asignar)

        # Administracion
        key_admini = [
            'tarjeta de ingreso',
            'reglamento de edificio',
            'reserva de sum',
            'alambrado perimetral',
            'alambrado',
            'asadores',
        ]
        valor_asignar = 'Administración'
        buscar_palabras(df, key_admini, valor_asignar)

        ###### ABANDONAN ######
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '7') & (~df['idChat'].isin(idChats_otrasconsultas))
        df.loc[filtro, 'Menu Principal'] = 'Otras Consultas'
        df.loc[filtro, 'Menu Secundario'] = 'Abandonan'
        df.loc[filtro, 'Menu Terciario'] = 'Abandonan'

