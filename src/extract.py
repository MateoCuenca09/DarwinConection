from utils import obtener_fecha_hoy_ayer
import os, requests, datetime, json
from dotenv import load_dotenv
load_dotenv()

raw_folder = 'data/raw'
conversation_url = "https://api.botdarwin.com/data/conversations"

class EvoltisConn:
    def __init__(self):
        self.login_url = os.getenv('login_url')
        self.login_data = {
            'username': os.getenv('username_evoltis'),
            'password': os.getenv('password_evoltis')
        }

    def _descargar_datos(self, startDate, endDate):
        """  
        :param startDate: datetime %Y/%m/%d
        :param endDate: datetime %Y/%m/%d
        """

        response = requests.post(self.login_url, self.login_data)
        
        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Extraer el token de la respuesta JSON
            token = response.json().get("idToken")

            # Utilizar el token para hacer la siguiente solicitud
            headers = {
                "darwinclientname": "edisur",
                "Authorization": f"Bearer {token}"
            }

            # Parámetros de la consulta
            params = {
                "startDate": startDate,
                "endDate": endDate
            }

            # Realizar la solicitud con el token
            response_conversations = requests.get(conversation_url, headers=headers, params=params)

            # Verificar si la solicitud fue exitosa (código de estado 200)
            if response_conversations.status_code == 200:
                # Procesar la respuesta JSON de las conversaciones
                datos = response_conversations.json()
                return datos
            else:
                raise Exception(f"Error en la solicitud de conversaciones: {response_conversations.status_code}")
        else:
            raise Exception (f"Error en el inicio de sesión: {response.status_code}")
        
    
        
    def _guardar_datos(self, datos):
        """  
        :param datos: json crudo de descargar_datos
        """
        # Obtenemos la carpeta del mes
        path_month_folder = os.path.join(raw_folder, datetime.datetime.now().strftime("%Y-%m"))
        os.makedirs(path_month_folder, exist_ok=True)

        # Armamos la ruta del archivo
        filename = datetime.datetime.now().strftime("%Y-%m-%d") + 'dataRAW.json'
        ruta_archivo = os.path.join(path_month_folder,filename)

        with open(ruta_archivo, 'w') as archivo:
            json.dump(datos, archivo, indent=4)

def obtener_y_guardar_datos():
    startDate,endDate = obtener_fecha_hoy_ayer()
    ec = EvoltisConn()
    datos = ec._descargar_datos(startDate, endDate)
    ec._guardar_datos(datos)

if __name__ == '__main__':
    obtener_y_guardar_datos()