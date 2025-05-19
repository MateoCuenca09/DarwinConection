"""  
Version: 1.0.0
Solo se refactorizo el codigo
"""
import pandas as pd


class Modelo_Darwin:
    """  
    Este modelo se encarga de clasificar un DF de conversaciones segun elecciones de la siguiente manera:
    * Menu Principal
    * Menu Secundario
    * Menu Terciario
    * Reclamo Anterior
    * Feedback del bot
    """
    def __init__(self, df):
        self.df = df
        pass

    def main(self):
        """  
        Pipeline completo para procesar los datos
        """
        self.menu_principal()
        self.menu_secundario()
        self.feedback()
        self.fuera_de_horario()
        self.perdidos()
        self.no_ingresan()

        return self.df

    def menu_principal(self):
        """
        Función menu_Principal que procesa todos los posibles menus principales y los guarda en el dataframe.
        """
        try:
            ###### EXPENSAS ######
            filtro = (self.df['page'] == 'Menu Principal - A1') & (self.df['message'] == '1')
            self.df.loc[filtro, 'Menu Principal'] = 'Expensas'
        
            ###### OBRAS ######
            filtro = (self.df['page'] == 'Menu Principal - A1') & (self.df['message'] == '2')
            self.df.loc[filtro, 'Menu Principal'] = 'Obras'

            ###### CESIONES ######
            filtro = (self.df['page'] == 'Menu Principal - A1') & (self.df['message'] == '3')
            self.df.loc[filtro, 'Menu Principal'] = 'Cesiones'

            ###### SERVICIOS E IMPUESTOS ######
            filtro = (self.df['page'] == 'Menu Principal - A1') & (self.df['message'] == '4')
            self.df.loc[filtro, 'Menu Principal'] = 'Servicios e Impuestos'

            ###### CONTACTOS UTILES ######
            filtro = (self.df['page'] == 'Menu Principal - A1') & (self.df['message'] == '5')
            self.df.loc[filtro, 'Menu Principal'] = 'Contactos Útiles'

            ###### VENTAS ######
            filtro = (self.df['page'] == 'Menu Principal - A1') & (self.df['message'] == '6')
            self.df.loc[filtro, 'Menu Principal'] = 'Ventas'

        except Exception as e:
            raise Exception(f'Error al procesar menuAcesos ({e})')

    def menu_secundario(self):
        """
        Función menu_Secundario que procesa todos los posibles menus secundario.

        Parámetros:
        - df: Dataframe con todos los datos 
        """
        self._menu_Expensas()
        self._menu_Obras()
        self._menu_Cesiones()
        self._menu_Servicios()
        self._menu_Contactos()
        self._menu_Ventas()
        self._menu_OtrasConsultas()

    def feedback(self):
        pass

    def fuera_de_horario(self):
        pass

    def perdidos(self):
        pass

    def no_ingresan(self):
        pass

    def _menu_Expensas(self):
        """
        Función menu_Expensas que procesa todos los clientes que ingresaron al menu Expensas y su posteriores elecciones guardandolos en el dataframe.

        Parámetros:
        - df: Dataframe con todos los datos 
        """
        try:
            ###### ID EXPENSAS ######
            filtro = (self.df['page'] == 'Menu Expensas') & (self.df['message'] == '1')
            self.df.loc[filtro, 'Menu Principal'] = 'Expensas'
            self.df.loc[filtro, 'Menu Secundario'] = 'ID Expensas'

                # Encuentra ID Expensas
            filtro = self.df['message'].str.startswith("Tu ID de expensas es:")
            df_idexp = self.df.loc[filtro]
            idChats_idexp = df_idexp['idChat']
            filtro = (self.df['idChat'].isin(idChats_idexp)) & (self.df['Menu Secundario'] == 'ID Expensas')
            self.df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'
            self.df.loc[filtro, 'user'] = self.df['room']

                # No Encuentra ID Expensas
            # Derivados Expensas #

            ######  EXPENSA CORRIENTE ######
            filtro = (self.df['page'] == 'Menu Expensas') & (self.df['message'] == '2')
            self.df.loc[filtro, 'Menu Principal'] = 'Expensas'
            self.df.loc[filtro, 'Menu Secundario'] = 'Expensa Corriente'
            
                # Encuentra Expensa Corriente
            filtro = (self.df['page'] == 'Archivo Expensa')
            df_expcorr = self.df.loc[filtro]
            idChats_expcorr = df_expcorr['idChat']
            filtro = (self.df['idChat'].isin(idChats_expcorr)) & (self.df['Menu Secundario'] == 'Expensa Corriente')
            self.df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'

                # No encuentra y Deriva a asesor
            filtro = self.df['message'].str.startswith("No pudimos encontrar un ID de expensa con esos datos.")
            df_expcorNE = self.df.loc[filtro]
            idChats_expcorrNE = df_expcorNE['idChat']
            filtro = (self.df['idChat'].isin(idChats_expcorrNE)) & (self.df['Menu Secundario'] == 'Expensa Corriente') 
            self.df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'


            ###### ACTUALIZAR CUPON ######
            filtro = (self.df['page'] == 'Menu Expensas') & (self.df['message'] == '3')
            self.df.loc[filtro, 'Menu Principal'] = 'Expensas'
            self.df.loc[filtro, 'Menu Secundario'] = 'Actualizar Cupon'
            # Derivados Expensas #

            ###### PLAN DE PAGOS ######
            filtro = (self.df['page'] == 'Menu Expensas') & (self.df['message'] == '4')
            self.df.loc[filtro, 'Menu Principal'] = 'Expensas'
            self.df.loc[filtro, 'Menu Secundario'] = 'Plan de Pagos'
            # Derivados Expensas #


            ###### OTRAS CONSULTAS ######
            filtro = (self.df['page'] == 'Menu Expensas') & (self.df['message'] == '5')
            self.df.loc[filtro, 'Menu Principal'] = 'Expensas'
            self.df.loc[filtro, 'Menu Secundario'] = 'Otras Consultas'
            # Derivados Expensas #
            

            ###### DEBITO AUTOMATICO ######
            filtro = (self.df['page'] == 'Menu Expensas') & (self.df['message'] == '6')
            self.df.loc[filtro, 'Menu Principal'] = 'Expensas'
            self.df.loc[filtro, 'Menu Secundario'] = 'Debito Automatico'
            self.df.loc[filtro, 'Menu Terciario'] = 'Resueltos x Sistema'

            ###### VOLVER ######
            filtro = (self.df['page'] == 'Menu Expensas') & (self.df['message'] == '0')
            self.df.loc[filtro, 'Menu Principal'] = 'Expensas'
            self.df.loc[filtro, 'Menu Secundario'] = 'Volver'
            self.df.loc[filtro, 'Menu Terciario'] = 'Volver'

            ###### Derivados Expensas ######
            filtro = self.df['message'].str.startswith("¡Gracias! Te voy a derivar con un asesor para que resuelva tu consulta.")
            df_derivados = self.df.loc[filtro]
            idChats = df_derivados['idChat']
            filtro = (self.df['Menu Principal'] == 'Expensas') & (self.df['Menu Secundario'].notnull()) & (self.df['idChat'].isin(idChats)) & (self.df['Menu Terciario'].isnull())
            self.df.loc[filtro, 'Menu Terciario'] = 'Derivados Bot'
            
        except Exception as e:
            raise Exception(f'Error menu_Expensas({e})')

    def _menu_Obras(self):
        pass

    def _menu_Cesiones(self):
        pass

    def _menu_Servicios(self):
        pass

    def _menu_Contactos(self):
        pass

    def _menu_Ventas(self):
        pass

    def _menu_OtrasConsultas(self):
        pass

class MENSAJES_DARWIN:
    """ 
     Este modelo contiene los mensajes que se envian al cliente y los que envia el cliente al bot.
    """
    #DERIVADOS = {message:'Derivacion',user:'System'}
    