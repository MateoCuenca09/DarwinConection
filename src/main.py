import schedule, os, logging, time, requests
from datetime import datetime, timedelta
from PBI_funtions import mainPBI
import pandas as pd
from dotenv import load_dotenv
from guardar import FileHandler
from config import DEBUG

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
log_format = '%(asctime)s, %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(filename='datos/Avisos.txt', level=logging.INFO, format=log_format, datefmt=date_format)


class DConnection:

    def main(self):
        logging.info('Comienza conexion con Darwin')
        try:
            datos = self._descarga(days=1)

        except Exception as e:
            logging.warning("No se pueden procesar los datos nuevos.")
        else:
            try:
                # Transformamos los datos a un DataFrame
                df_crudo = pd.DataFrame(datos)
                
                if DEBUG: df_crudo.to_excel("temp/Crudo.xlsx", index= False)

                df_proces = mainPBI(df_crudo)
                
                if DEBUG: df_proces.to_excel("temp/Procesado.xlsx", index= False)

                FileHandler().guardar_mes(df_proces)
                FileHandler().separar_por_mes(df_proces)

                logging.info(f'Termina proceso exitosamente {datetime.now().strftime("%Y/%m/%d")}')



            except Exception as e:
                logging.info('Termina proceso con errores')


    def single_run(self, days):
        datos = self._descarga(days)
        mainPBI(datos)

    def ShowCredentials(self):
        print(f"""
            USUARIO : {username}
            CONTRASEÑA : {password}
            URL : {login_url}
              """)
        logging.info(f'User: {username}')
        logging.info(f'User: {password}')
        logging.info(f'User: {login_url}')
        
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
            time.sleep(60)


if __name__ == '__main__':
    DConnection().main()