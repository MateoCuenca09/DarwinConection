import schedule
import time
from datetime import datetime, timedelta
import requests
from PBI_funtions import mainPBI
import os
from dotenv import load_dotenv
# Cargamos variables privadas
load_dotenv()

login_url = os.getenv("login_url")
username = os.getenv("username_f")
password = os.getenv("password")
login_data = {
    "username": username,
    "password": password
}


def main():
    """
    Función principal que descarga los datos de la API y envia a main PBI_functions.

    Parámetros:
    - Empty
    Retorna:
    - Empty
    """
    try:
        days = 2 # Dias para atras que se quiere analizar

        # Obtener la fecha actual
        endDate = datetime.now().strftime("%Y/%m/%d")
        # Obtener la fecha de 3 días atrás
        startDate = (datetime.now() - timedelta(days)).strftime("%Y/%m/%d")
        #startDate = '2023/08/01'





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
            else:
                print(f"Error en la solicitud de conversaciones: {response_conversations.status_code}")
        else:
            print(f"Error en el inicio de sesión: {response.status_code}")

        print("Descarga exitosa!")
        # Inicializa mainPBI
        mainPBI(datos)

    except requests.exceptions.RequestException as e:
        print("Error al descargar los datos main():", e)



# Rutina diaria de inicializacion del programa
schedule.every().monday.at("20:00").do(main)
schedule.every().tuesday.at("20:00").do(main)
schedule.every().wednesday.at("20:00").do(main)
schedule.every().thursday.at("20:00").do(main)
schedule.every().friday.at("20:00").do(main)
schedule.every().saturday.at("20:00").do(main)
schedule.every().sunday.at("20:00").do(main)

# Mantener el programa en ejecución para que se realicen las tareas programadas
while True:
    schedule.run_pending()
    time.sleep(1) 


