import schedule
import time
from datetime import datetime, timedelta
import requests
from PBI_funtions import mainPBI
import os
import logging
from dotenv import load_dotenv
# Cargamos variables privadas
load_dotenv()

login_url = os.getenv("login_url")
username = os.getenv("username_f")
password = os.getenv("password_f")
login_data = {
    "username": username,
    "password": password
}

# Configuramos el Logger
logging.basicConfig(filename='Avisos.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DConnection:

    def main(self):
        try:
            datos = self._descarga(days=2)
        except Exception as e:
            logging.warn("No se pueden procesar los datos nuevos.")
        else:
            mainPBI(datos)
        finally:
            print("")
            #subir logging al Sharepoint

    def single_run(self, days):
        datos = self._descarga(days)
        mainPBI(datos)

    def ShowCredentials(self):
        print(f"""
            USUARIO : {username}
            CONTRASEÑA : {password}
            URL : {login_url}
              """)
        
    def _descarga(self, days):
        try:
            # Calculo fecha
            endDate = datetime.now().strftime("%Y/%m/%d")
            startDate = (datetime.now() - timedelta(days)).strftime("%Y/%m/%d")

            # Realizar la solicitud de inicio de sesión
            response = requests.post(login_url, json=login_data)

            # Verificar si la solicitud fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Extraer el token de la respuesta JSON
                token = response.json().get("idToken")

                # Utilizar el token para hacer la siguiente solicitud
                conversation_url = "https://api.botdarwin.com/data/conversations"
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
                    print(f"Error en la solicitud de conversaciones: {response_conversations.status_code}")
                    logging.error('No se pudo descargar los datos de Evoltis')
            else:
                print(f"Error en el inicio de sesión: {response.status_code}")
                logging.error('No se pudo validar los datos con Evoltis')

            print("Descarga exitosa!")
            logging.info("Descarga de datos exitosa!")
        except requests.exceptions.RequestException as e:
            print("Error al descargar los datos main():", e)
            logging.error('Error en Descarga')

    def daily(self):
        schedule.every().day.at('22:00').do(self.main)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    DConnection().single_run(60)