import pandas as pd
import os
from datetime import datetime, timedelta
from unidecode import unidecode

def mainPBI(datos):
    df = pd.DataFrame(datos)


    # Asegurémonos de que la columna 'date' sea de tipo datetime
    df['date'] = pd.to_datetime(df['date'])

    # Eliminar la zona horaria de la columna 'date'
    df['date'] = df['date'].dt.tz_convert(None)



    menu_Principal(df)
    menu_Secundario(df)
    Feedback(df)


    perdidos(df)
    no_ingresan(df)

    #df = df[df['user'] != 'system']
    df = df.drop(['type','channel','darwinChatID','page','__v','intent','endpoint','username','isLogin','typeClose'], axis=1)
    #df = df.dropna(subset=['Menu Principal'])
    #df = df.dropna(subset=['Menu Secundario'])
    #df = df.dropna(subset=['Menu Terciario'])
    #df1 = df.drop_duplicates(subset=['idChat', 'Menu Principal','Menu Secundario','Menu Terciario'], keep='last')

    guardar_historico(df)


def Feedback(df):
    reclamo(df)
    encuesta(df)
    


def menu_Secundario(df):
    menu_Expensas(df)
    menu_Obras(df)
    menu_Cesiones(df)
    menu_Contactos(df)
    menu_Servicios(df)
    menu_OtrasConsultas(df)

def menu_Principal(df): 
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
    try:
        ###### ID EXPENSAS ######
        filtro = (df['page'] == 'Menu Expensas') & (df['message'] == '1')
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Secundario'] = 'ID Expensas'

            # Encuentra ID Expensas
        filtro = df['message'].str.startswith("Tu ID de expensas es:")
        df.loc[filtro, 'Menu Principal'] = 'Expensas'
        df.loc[filtro, 'Menu Secundario'] = 'ID Expensas'
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
        df.loc[filtro, 'Menu Terciario'] = 'Derivados'
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
        df.loc[filtro, 'Menu Terciario'] = 'Derivados'
        
    except Exception as e:
        print("Error menu_Expensas(): ",e)


def menu_Obras(df):
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
        df.loc[filtro, 'Menu Terciario'] = 'Derivados'      

    except Exception as e:
        print("Error menu_Amojonado(): ",e)

def menu_Cesiones(df):
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
        df.loc[filtro, 'Menu Terciario'] = 'Derivados'


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
    try:
        ###### UF AGUAS CORDOBESAS ######
        filtro = (df['page'] == 'Botonera Tipo Servicio - F5') & (df['message'] == '1')
        df_servicios = df[filtro]
        idChats_servicios = df_servicios['idChat']
        filtro = (df['idChat'].isin(idChats_servicios)) & (df['Menu Principal'] == 'Servicios e Impuestos' )
        df.loc[filtro, 'Menu Secundario'] = 'UF Aguas Cordobesas'  
        df.loc[filtro, 'Menu Terciario'] = 'Derivados'


        ###### IMP POLICIAL ######
        filtro = (df['page'] == 'Botonera Tipo Servicio - F5') & (df['message'] == '2')
        df_servicios = df[filtro]
        idChats_servicios = df_servicios['idChat']
        filtro = (df['idChat'].isin(idChats_servicios)) & (df['Menu Principal'] == 'Servicios e Impuestos' )
        df.loc[filtro, 'Menu Secundario'] = 'Imp. Pcial.'
        df.loc[filtro, 'Menu Terciario'] = 'Derivados'

        
        ###### IMP MUNICIPAL ######
        filtro = (df['page'] == 'Botonera Tipo Servicio - F5') & (df['message'] == '3')
        df_servicios = df[filtro]
        idChats_servicios = df_servicios['idChat']
        filtro = (df['idChat'].isin(idChats_servicios)) & (df['Menu Principal'] == 'Servicios e Impuestos' )
        df.loc[filtro, 'Menu Secundario'] = 'Imp. Municipal' 
        df.loc[filtro, 'Menu Terciario'] = 'Derivados' 

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
    try:
        filtro = (df['page'] == 'Menu Otras Consultas') & (df['user'] != 'system')
        df_otrasconsultas = df.loc[filtro]
        idChats_otrasconsultas = df_otrasconsultas['idChat']
        df.loc[filtro, 'Menu Principal'] = 'Otras Consultas'
        df.loc[filtro, 'Menu Secundario'] = 'Derivados'
        df.loc[filtro, 'Menu Terciario'] = 'Derivados'
          
        #### CLASIFICACION DE OTRAS CONSULTAS ####
        # EXPENSAS
        palabras_clave = [
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
            'expensas anteriores',
            'Expensa corriente',
            'expensa inactiva',
            'expensa vigente',
            'ID',
            'ID de expensa',
            'ID expensa',
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

        buscar_palabras(df, palabras_clave, valor_asignar)

        # INIC OBRA - AMOJONADO
        palabras_clave = [
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
        ]
        valor_asignar = 'Inic Obras'
        buscar_palabras(df, palabras_clave, valor_asignar)

        # CESION INMUEBLE
        palabras_clave = [
            'autorizacion de venta',
            'autorizacion para ceder',
            'cedente',
            'ceder',
            'cesion',
            'cesionario',
            'cesiones',
            'nuevo propietario',
        ]
        valor_asignar = 'Cesiones'
        buscar_palabras(df, palabras_clave, valor_asignar)

        # SERVICIOS E IMPUESTOS
        palabras_clave = [
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
            'UF',
            'uf aguas cordobesas',
            'unidad de facturación',
            'unidaddes de facturacion',
        ]
        valor_asignar = 'Servicios e Impuestos'
        buscar_palabras(df, palabras_clave, valor_asignar)

        # CONTACTOS UTILES
        palabras_clave = [
            'telefono del intendente'
        ]
        valor_asignar = 'Contactos Utiles'
        buscar_palabras(df, palabras_clave, valor_asignar)








        ###### ABANDONAN ######
        filtro = (df['page'] == 'Menu Principal - A1') & (df['message'] == '7') & (~df['idChat'].isin(idChats_otrasconsultas))
        df.loc[filtro, 'Menu Principal'] = 'Otras Consultas'
        df.loc[filtro, 'Menu Secundario'] = 'Abandonan'
        df.loc[filtro, 'Menu Terciario'] = 'Abandonan'

      

    except Exception as e:
        print("Error menu_OtrasConsultas(): ",e)


def reclamo(df):
        try:
            # Consultas Enviadas    
            filtro = df['message'] == '¿Tu reclamo o consulta fue resuelto? Si No'
            df.loc[filtro,'user'] = df['room']
            df.loc[filtro,'Menu Principal'] = 'Feedback'
            df.loc[filtro,'Menu Secundario'] = 'Feedback'
            df.loc[filtro,'Menu Terciario'] = 'Feedback'

            # Respuestas Enviadas
            ### SI
            filtro = (df['page'] == 'Encuesta 2 - B1') & (df['message'] == 'Si')
            df_idChats = df.loc[filtro]
            idchats = df_idChats['idChat']
            filtro1 = (df['idChat'].isin(idchats)) & (df['Menu Principal'] == 'Feedback') 
            df.loc[filtro1, 'Reclamo'] = 'Si' 

            filtro = (df['page'] == 'Encuesta 2 - B1') & (df['message'] == 'si')
            df_idChats = df.loc[filtro]
            idchats = df_idChats['idChat']
            filtro1 = (df['idChat'].isin(idchats)) & (df['Menu Principal'] == 'Feedback') 
            df.loc[filtro1, 'Reclamo'] = 'Si' 

            ### NO
            filtro = (df['page'] == 'Encuesta 2 - B1') & (df['message'] == 'No')
            df_idChats = df.loc[filtro]
            idchats = df_idChats['idChat']
            filtro1 = (df['idChat'].isin(idchats)) & (df['Menu Principal'] == 'Feedback') 
            df.loc[filtro1, 'Reclamo'] = 'No' 

            filtro = (df['page'] == 'Encuesta 2 - B1') & (df['message'] == 'no')
            df_idChats = df.loc[filtro]
            idchats = df_idChats['idChat']
            filtro1 = (df['idChat'].isin(idchats)) & (df['Menu Principal'] == 'Feedback') 
            df.loc[filtro1, 'Reclamo'] = 'No' 
            

        except Exception as e:
              print("Error reclamo(): ",e)
              
def encuesta(df):
    try:
        filtro = (df['page'] == 'Calificacion - B2') & (df['message'] == 'Muy Satisfecha/o')
        df_idChats = df.loc[filtro]
        idchats = df_idChats['idChat']
        filtro1 = (df['idChat'].isin(idchats)) & (df['Menu Principal'] == 'Feedback')
        df.loc[filtro1, 'Encuesta'] = 'Muy Satisfecha/o'
      

        filtro = (df['page'] == 'Calificacion - B2') & (df['message'] == 'Satisfecha/o')
        df_idChats = df.loc[filtro]
        idchats = df_idChats['idChat']
        filtro1 = (df['idChat'].isin(idchats)) & (df['Menu Principal'] == 'Feedback')
        df.loc[filtro1, 'Encuesta'] = 'Satisfecha/o'
       

        filtro = (df['page'] == 'Calificacion - B2') & (df['message'] == 'Insatisfecha/o')
        df_idChats = df.loc[filtro]
        idchats = df_idChats['idChat']
        filtro1 = (df['idChat'].isin(idchats)) & (df['Menu Principal'] == 'Feedback')
        df.loc[filtro1, 'Encuesta'] = 'Insatisfecha/o'


        filtro = (df['page'] == 'Calificacion - B2') & (df['message'] == 'Muy Insatisfecha/o')
        df_idChats = df.loc[filtro]
        idchats = df_idChats['idChat']
        filtro1 = (df['idChat'].isin(idchats)) & (df['Menu Principal'] == 'Feedback')
        df.loc[filtro1, 'Encuesta'] = 'Muy Insatisfecha/o'

        encuesta_Incompleta(df)

    except Exception as e:
        print("Error encuesta(): ",e)


def encuesta_Incompleta(df):
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
    try:
        # Envian mal 3 mensajes seguidos
        # Todos los que derivan
        filtro = df['message'].str.endswith("¡No te preocupes! Te derivo con un asesor…")
        df.loc[filtro,'user'] = df['room']
        df_idChats = df.loc[filtro]
        idChats_todos = df_idChats['idChat']
        # Los que tienen el 3er Menu Vacio
        filtro = (df['idChat'].isin(idChats_todos)) & (df['Menu Secundario'].notnull()) & (df['Menu Terciario'].isnull()) 
        df.loc[filtro,'Menu Terciario'] = 'Confundidos Derivados'

        # Los que tienen el 2do Menu Vacio
        df_idChats_confundidos3 = df[filtro]
        idChats_confundidos3 = df_idChats_confundidos3['idChat'] # 3ro
        df_idChats_sobra3 = df_idChats[~df_idChats['idChat'].isin(idChats_confundidos3)] # 2do = Todos - 3ro
        idChats_sobra3 = df_idChats_sobra3['idChat']
        filtro = (df['idChat'].isin(idChats_sobra3)) & (df['Menu Principal'].notnull()) & (df['Menu Secundario'].isnull()) # Solo los que tienen 2do Vacio
        df.loc[filtro,'Menu Secundario'] = 'Confundidos Derivados'
        df.loc[filtro,'Menu Terciario'] = 'Confundidos Derivados'

        df_idChats_confundidos2 = df[filtro] 
        idChats_confundidos2 = df_idChats_confundidos2['idChat'] # 2do Vacio
        df_idChats_confundidos1 = df_idChats_sobra3[~df_idChats_sobra3['idChat'].isin(idChats_confundidos2)]
        idChats_confundidos1 = df_idChats_confundidos1['idChat']
        filtro = (df['idChat'].isin(idChats_confundidos1)) & (df['message'].str.endswith("¡No te preocupes! Te derivo con un asesor…"))
        df.loc[filtro,'user'] = df['room']
        df.loc[filtro,'Menu Principal'] = 'Confundidos Derivados'
        df.loc[filtro,'Menu Secundario'] = 'Confundidos Derivados'
        df.loc[filtro,'Menu Terciario'] = 'Confundidos Derivados'





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
    try:
        df_ingresan = df.loc[df['Menu Principal'].notnull()]
        id_ingresan = df_ingresan['idChat']
        filtro = ~df['idChat'].isin(id_ingresan)
        df.loc[filtro, 'Menu Principal'] = 'Abandonan'
        df.loc[filtro, 'Menu Secundario'] = 'Abandonan'
        df.loc[filtro, 'Menu Terciario'] = 'Abandonan'



    except Exception as e:
        print("Error no_ingresan(): ",e)

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

def buscar_palabras(df, palabras_clave, valor_asignar):
    try:
        # Filtro
        filtro = (df['page'] == 'Menu Otras Consultas') & (df['user'] != 'system')
        # Normalizacion
        lista_minusculas = [elemento.lower() for elemento in palabras_clave]
        lista_sin_acentos = [unidecode(elemento) for elemento in lista_minusculas]

        df.loc[filtro,"message"] = df["message"].apply(lambda x: unidecode(x.lower()))

        # Iterar a través de cada fila del dfFrame
        for index, row in df.loc[filtro].iterrows():
            for palabra in lista_sin_acentos:
                if palabra in row["message"]:
                    df.at[index, "Otras Consultas"] = valor_asignar
    except Exception as e:
        print("Error buscar_palabras(): ",e)