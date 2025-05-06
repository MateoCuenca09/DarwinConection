from utils import obtener_fecha_hoy_ayer
import os, requests, datetime, json
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

base_url = 'https://api.botdarwin.com'
debug = False

class API_Darwin:
    def __init__(self):
        self.base_url = base_url
        self.login_data = {
            'username': os.getenv('username_evoltis'),
            'password': os.getenv('password_evoltis')
        }
        self.token = self.login()
        self.headers =  {
                            "darwinclientname": "edisur",
                            "Authorization": f"Bearer {self.token}"
                        }

    def login(self):
        """
        """
        url = f'{self.base_url}/login'
        response = requests.post(url, self.login_data)
        
        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Extraer el token de la respuesta JSON
            token = response.json().get("idToken")      
            return token
        else:
            raise Exception (f"Error en el inicio de sesión: {response.status_code}")

    def _get_(self, endpoint: str, params: dict = None) -> dict:
        if not self.token:
            raise Exception("⚠️ No estás autenticado. Ejecuta `login()` primero.")

        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)

        # Guardar respuesta en un archivo para analizarla
        if debug:
            with open("response_debug.txt", "w", encoding="utf-8") as f:
                f.write(response.text)

        # Validar que la respuesta sea JSON
        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            raise Exception(f"❌ Respuesta inesperada: {content_type}\n{response.text[:500]}")

        try:
            return json.loads(response.text.strip())  # Strip para eliminar espacios en blanco
        except json.JSONDecodeError as e:
            raise Exception(f"❌ Error al decodificar JSON: {e}\nRevisar response_debug.txt")

    """ GET DATA """

    def get_datas(self,startDate, endDate):
        """  
        """
        conversations = self.get_data_conversations(startDate, endDate)
        noMatch = self.get_data_noMatch(startDate, endDate)
        feedback = self.get_data_feedback(startDate,endDate)
        nps = self.get_data_nps(startDate,endDate)

        data_dict = {
            "Conversations":pd.DataFrame(conversations),
            "NoMatch":pd.DataFrame(noMatch),
            "Feedback":pd.DataFrame(feedback),
            "Nps":pd.DataFrame(nps)
        }

        return data_dict

    def get_data_conversations(self, startDate, endDate):
        """  
        :param startDate: datetime %Y/%m/%d
        :param endDate: datetime %Y/%m/%d
        """
        endpoint = 'data/conversations'
        params = {
            "startDate": startDate,
            "endDate": endDate,
            "timeZoneOffset":"-03:00"
        }
        return self._get_(endpoint,params)
    
    def get_data_noMatch(self, startDate, endDate):
        """  
        :param startDate: datetime %Y/%m/%d
        :param endDate: datetime %Y/%m/%d
        """
        endpoint = 'data/noMatch'
        params = {
            "startDate": startDate,
            "endDate": endDate,
            "timeZoneOffset":'03:00'
        }
        return self._get_(endpoint,params)
    
    def get_data_feedback(self, startDate, endDate):
        """  
        :param startDate: datetime %Y/%m/%d
        :param endDate: datetime %Y/%m/%d
        """
        endpoint = 'data/feedback'
        params = {
            "startDate": startDate,
            "endDate": endDate,
            "timeZoneOffset":'03:00'
        }
        return self._get_(endpoint,params)
    
    def get_data_nps(self, startDate, endDate):
        """  
        :param startDate: datetime %Y/%m/%d
        :param endDate: datetime %Y/%m/%d
        """
        endpoint = 'data/nps'
        params = {
            "startDate": startDate,
            "endDate": endDate,
            "timeZoneOffset":'03:00'
        }
        return self._get_(endpoint,params)

    """ GET REPORTS """

    def get_report_conversationsPerDay(self, startDate, endDate):
        """  
        Me lo envian por mail... (????
        :param startDate: datetime %Y/%m/%d
        :param endDate: datetime %Y/%m/%d
        """
        endpoint = 'report/conversationsPerDay'
        params = {
            "channelsSelected":'["WEB","FACEBOOK","WHATSAPP"]',
            "startDate": startDate,
            "endDate": endDate,
            "timeZoneOffset":'03:00'
        }
        return self._get_(endpoint,params)

    def get_report_talkTime(self,startDate,endDate):
        """  
        Internal Server Error
        :param startDate: datetime %Y/%m/%d
        :param endDate: datetime %Y/%m/%d
        """
        endpoint = 'report/talkTime'
        params = {
            "channelsSelected":'["WEB","FACEBOOK","WHATSAPP"]',
            "startDate": startDate,
            "endDate": endDate,
            "timeZoneOffset":'03:00'
        }
        return self._get_(endpoint,params)
    
    def get_report_loggedPerDay(self, startDate, endDate):
        """  
        Check
        :param startDate: datetime %Y/%m/%d
        :param endDate: datetime %Y/%m/%d
        """
        endpoint = 'report/loggedPerDay'
        params = {
            "channelsSelected":'["WEB","FACEBOOK","WHATSAPP"]',
            "startDate": startDate,
            "endDate": endDate,
            "timeZoneOffset":'03:00'
        }
        return self._get_(endpoint,params)
    
    def get_report_conversationalInteractions(self,startDate,endDate):
        """  
        Internal Server Error
        :param startDate: datetime %Y/%m/%d
        :param endDate: datetime %Y/%m/%d
        """
        endpoint = 'report/conversationalInteractions'
        params = {
            "channelsSelected":'["WEB","FACEBOOK","WHATSAPP"]',
            "startDate": startDate,
            "endDate": endDate,
            "timeZoneOffset":'03:00'
        }
        return self._get_(endpoint,params)
    
    def get_report_interactionsMonth(self,startDate, endDate):
        """
        Check  
        :param startDate: datetime %Y/%m/%d
        :param endDate: datetime %Y/%m/%d
        """
        endpoint = 'report/interactionsMonth'
        params = {
            "channelsSelected":'["WEB","FACEBOOK","WHATSAPP"]',
            "startDate": startDate,
            "endDate": endDate,
            "timeZoneOffset":'03:00'
        }
        return self._get_(endpoint,params)
    
    def get_report_intents(self, startDate,endDate):
        """  
        Internal server error
        :param startDate: datetime %Y/%m/%d
        :param endDate: datetime %Y/%m/%d
        """
        endpoint = 'report/intents'
        params = {
            "channelsSelected":'["WEB","FACEBOOK","WHATSAPP"]',
            "startDate": startDate,
            "endDate": endDate,
            "timeZoneOffset":'03:00'
        }
        return self._get_(endpoint,params)
    
    def get_report_feedback(self, startDate,endDate):
        """  
        check
        :param startDate: datetime %Y/%m/%d
        :param endDate: datetime %Y/%m/%d
        """
        endpoint = 'report/feedback'
        params = {
            "channelsSelected":'["WEB","FACEBOOK","WHATSAPP"]',
            "startDate": startDate,
            "endDate": endDate,
            "timeZoneOffset":'03:00'
        }
        return self._get_(endpoint,params)
    
    def get_report_tags(self,startDate,endDate):
        """  
        Internal Server Error
        :param startDate: datetime %Y/%m/%d
        :param endDate: datetime %Y/%m/%d
        """
        endpoint = 'report/tags'
        params = {
            "channelsSelected":'["WEB","FACEBOOK","WHATSAPP"]',
            "startDate": startDate,
            "endDate": endDate,
            "timeZoneOffset":'03:00'
        }
        return self._get_(endpoint,params)
    
    def get_report_conversationsByIdChat(self,startDate,endDate):
        """  
        :param startDate: datetime %Y/%m/%d
        :param endDate: datetime %Y/%m/%d
        """
        endpoint = 'report/conversationByIdChat'
        params = {
            "channelsSelected":'["WEB","FACEBOOK","WHATSAPP"]',
            "startDate": startDate,
            "endDate": endDate,
            "timeZoneOffset":'03:00'
        }
        return self._get_(endpoint,params)

    def get_report_conversationsChattigo(self,startDate,endDate):
        """
        Endpoint not Found 404  
        :param startDate: datetime %Y/%m/%d
        :param endDate: datetime %Y/%m/%d
        """
        endpoint = 'report/conversationsChattigo'
        params = {
            "channelsSelected":'["WEB","FACEBOOK","WHATSAPP"]',
            "startDate": startDate,
            "endDate": endDate,
            "timeZoneOffset":'03:00'
        }
        return self._get_(endpoint,params)        

def get_and_save_datas():
    """  
    For tests only
    """
    ayer,hoy = obtener_fecha_hoy_ayer()
    df_dict = API_Darwin().get_datas(ayer,hoy)
    
    for nombre, df in df_dict.items():
        path_xlsx = f'data/debug/{nombre}.xlsx'
        df.to_excel(path_xlsx, index=False)

if __name__ == '__main__':
    df = pd.DataFrame(API_Darwin().get_data_conversations("2025/05/02", "2025/05/02"))
    df.to_excel('crudo_2025-05-02.xlsx', index=False)