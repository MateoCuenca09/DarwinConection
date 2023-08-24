#Funciones Obtener Datos para Arbol

def menu_Principal(df): 
    try:
        df['combined'] = df['page'] + ' ' + df['message']

        df_filtrado = df.loc[df['combined'] == 'Menu Principal - A1 1']
        expensas = df_filtrado.shape[0]

        df_filtrado = df.loc[df['combined'] == 'Menu Principal - A1 2']
        amojonado = df_filtrado.shape[0]

        df_filtrado = df.loc[df['combined'] == 'Menu Principal - A1 3']
        cesiones = df_filtrado.shape[0]

        df_filtrado = df.loc[df['combined'] == 'Menu Principal - A1 4']
        servicios = df_filtrado.shape[0]

        df_filtrado = df.loc[df['combined'] == 'Menu Principal - A1 5']
        contactos = df_filtrado.shape[0]

        df_filtrado = df.loc[df['combined'] == 'Menu Principal - A1 6']
        ventas = df_filtrado.shape[0]

        df_filtrado = df.loc[df['combined'] == 'Menu Principal - A1 7']
        otras = df_filtrado.shape[0]

        return {"expensas": expensas, "amojonado": amojonado,"cesiones": cesiones, "servicios": servicios,
                "contactos": contactos,"ventas": ventas,"otras": otras}
    except Exception as e:
        print("Error al procesar menuAcesos:", e)


##### MENU EXPENSAS ####

def Id_expensas(df):
    try:
        ##ID EXPENSAS
        df_filtrado = df.loc[df['page'] == 'Menu Expensas']
        id_expensas = df_filtrado[df_filtrado['message'] == '1'].shape[0]

        ## RESUELTO X SISTEMA
        sistema = (df['message'].str.startswith('Tu ID de expensas es:')).sum()

        ## ASCESOR
        ascesor = (df['message'].str.startswith('No pudimos encontrar un ID de expensa con esos datos.')).sum()

        return {"id_expensas":id_expensas,"sistema":sistema,"ascesor":ascesor}
    except Exception as e:
        print("Error Id_expensas(): ",e)

def Expensa_corriente(df):
    try:
        ## EXPENSA CORRIENTE
        df_filtrado = df.loc[df['page'] == 'Menu Expensas']
        expensa_corriente = df_filtrado[df_filtrado['message'] == '2'].shape[0]
        return expensa_corriente
    except Exception as e:
        print("Error Expensa_corriente(): ",e)

def Actualizar_cupon(df):
    try:
        ## ACTUALIZAR CUPON
        df_filtrado = df.loc[df['page'] == 'Menu Expensas']
        actualizar_cupon = df_filtrado[df_filtrado['message'] == '3'].shape[0]

        ## LLEGAN A ASCESOR
        df_actualizar_cupon = df_filtrado.loc[df_filtrado['message'] == '3']

        ascesor = 0
        for id in df_actualizar_cupon['idChat']:
            if df.loc[(df['page'] == 'Derivar') & (df['idChat'] == id)].shape[0] > 0:
                ascesor += 1
        return {"actualizar_cupon":actualizar_cupon, "ascesor":ascesor}
    except Exception as e:
        print("Error Actualizar_cupon(): ",e)

def Plan_de_pagos(df):
    try:
        ## PLAN DE PAGOS
        df_filtrado = df.loc[df['page'] == 'Menu Expensas']
        plan_de_pagos = df_filtrado[df_filtrado['message'] == '4'].shape[0]

        ## LLEGAN A ASCESOR
        df_plan_de_pagos = df_filtrado.loc[df_filtrado['message'] == '4']

        ascesor = 0
        for id in df_plan_de_pagos['idChat']:
            if df.loc[(df['page'] == 'Derivar') & (df['idChat'] == id)].shape[0] > 0:
                ascesor += 1

        return {"plan_de_pagos":plan_de_pagos,"ascesor":ascesor}
    except Exception as e:
        print("Error Plan_de_pagos(): ",e)

def Otras_consultas(df):
    try:
        ## OTRAS CONSULTAS
        df_filtrado = df.loc[df['page'] == 'Menu Expensas']
        otras_consultas = df_filtrado[df_filtrado['message'] == '5'].shape[0]

        ## Llegan a ascesor
        df_otras_consultas = df_filtrado.loc[df_filtrado['message'] == '5']

        ascesor = 0
        for id in df_otras_consultas['idChat']:
            if df.loc[(df['page'] == 'Derivar') & (df['idChat'] == id)].shape[0] > 0:
                ascesor += 1
        return {"otras_consultas":otras_consultas,"ascesor":ascesor}
    except Exception as e:
        print("Error Otras_consultas(): ",e)


def Debito_automatico(df):
    try:
        ## DEBITO AUTOMATICO
        df_filtrado = df.loc[df['page'] == 'Menu Expensas']
        debito_automatico = df_filtrado[df_filtrado['message'] == '6'].shape[0]
        return debito_automatico
    except Exception as e:
        print("Error Debito_automatico(): ",e)

def Volver_expensa(df):
    try:
        ## VOLVER
        df_filtrado = df.loc[df['page'] == 'Menu Expensas']
        volver = df_filtrado[df_filtrado['message'] == '7'].shape[0]
        return volver
    except Exception as e:
        print("Error Volver_expensa(): ",e)


#### MENU AMOJONADO/INICIO DE OBRA ###
def menu_Amojonado(df):    
    try:
        ## LLEGAN A ASCESOR
        Amojonado = df.loc[(df['page'] == 'Menu Principal - A1') & (df['message'] == '2')]

        agente = 0
        for id in Amojonado['idChat']:
            if df.loc[(df['page'] == 'Derivar') & (df['idChat'] == id)].shape[0] > 0:
                agente += 1
        ## LLEGAN A LINK
        link = 0
        for id in Amojonado['idChat']:
            if df.loc[(df['message'].str.startswith('Acá te envío el link para que puedas acceder al formulario de registro de legajo de obra:')) & (df['idChat'] == id)].shape[0] > 0:
                link += 1
        return {"agente":agente, "link":link}
    except Exception as e:
        print("Error menu_Amojonado(): ",e)

#### MENU CESIONES ####
def menu_Cesiones(df):
    try:

        ceder = df[(df['page'] == 'Menu Cesiones') & (df['message'] == '1')].shape[0]

        informar = df[(df['page'] == 'Menu Cesiones') & (df['message'] == '2')].shape[0]

        volver = df[(df['page'] == 'Menu Cesiones') & (df['message'] == '0')].shape[0]

        return{"ceder":ceder,"informar":informar,"volver":volver}
    except Exception as e:
        print("Error menu_Cesiones(): ",e)


#### MENU SERVICIOS E IMPUESTOS ####
def menu_Servicios(df):
    try:
        servicios = df[(df['page'] == 'Menu Principal - A1') & (df['message'] == '4')]
        ascesor = 0
        for id in servicios ['idChat']:
            df_id = df.loc[df['idChat'] == id]
            df_id = df_id.fillna("Vacio")
            df_time =  df_id.sort_values('date')
            historial = df_time['page'].to_list()
            for i in range(len(historial)):
                if historial[i] == "Menu Servicios e Impuestos":
                    servicios = True
                if (historial[i] == "Derivar") and (servicios == True):
                    ascesor += 1
                    break
                if (historial[i].startswith("Menu")) & (historial[i]!= "Menu Servicios e Impuestos"):
                    servicios = False
        return ascesor
    except Exception as e:
        print("Error menu_Servicios(): ",e)

#### MENU CONTACTOS UTILES DEL BARRIO ####
def menu_Contactos(df):
    try:
        contactos = df[(df['page'] == 'Botonera Tipo Contacto - G5') & (df['message'] == '1')].shape[0]
        emprendedores = df[(df['page'] == 'Botonera Tipo Contacto - G5') & (df['message'] == '2')].shape[0]
        comercios = df[(df['page'] == 'Botonera Tipo Contacto - G5') & (df['message'] == '3')].shape[0]
        volver_contactos = df[(df['page'] == 'Botonera Tipo Contacto - G5') & (df['message'] == '0')].shape[0]
        return {"contactos":contactos,"emprendedores":emprendedores,"comercios":comercios,"volver_contactos":volver_contactos}
    except Exception as e:
        print("Error menu_Contactos(): ",e)
    
#### MENU OTRAS CONSULTAS ####
def menu_Consultas(df):
    try:
        consultas = df.loc[(df['page'] == 'Menu Principal - A1') & (df['message'] == '7')]

        ascesor = 0
        for id in consultas ['idChat']:
            df_id = df.loc[df['idChat'] == id]
            df_id = df_id.fillna("Vacio")
            df_time =  df_id.sort_values('date')
            historial = df_time['page'].to_list()
            for i in range(len(historial)):
                if historial[i] == "Menu Otras Consultas":
                    consulta = True
                if (historial[i] == "Derivar") and (consulta == True):
                    ascesor += 1
                    break
                if (historial[i].startswith("Menu")) & (historial[i]!= "Menu Otras Consultas"):
                    consulta = False
        return ascesor
    except Exception as e:
        print("Error menu_Consultas(): ",e)