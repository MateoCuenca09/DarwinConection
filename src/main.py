import schedule
import time
from datetime import datetime, timedelta
import requests
from PBI_funtions import mainPBI

def main():
    """
    Función principal que descarga los datos de la API y envia a main PBI_functions.

    Parámetros:
    - Empty
    Retorna:
    - Empty
    """
    try:
        # URL de la API de DARWIN
        url_api = "https://api.testing.botdarwin.com/data/conversations"

        # Token de autenticación requerido por la API
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnQiOiJlZGlzdXIiLCJyb3V0ZXMiOlsiL2FnZW50cyIsIi9pbnRlbnRzIiwiL2RhdGEiXSwiaWF0IjoxNjg2OTM3Nzc4fQ.F9Zdk2F50azIsgubt_HMMaQ5X20V-Iaw3UuJmcm27Qc"

        # Obtener la fecha actual
        endDate = datetime.now().strftime("%Y/%m/%d")

        # Obtener la fecha de 3 días atrás
        startDate = (datetime.now() - timedelta(days=3)).strftime("%Y/%m/%d")

        # Inicializar pedido API
        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "startDate": startDate,
            "endDate": endDate
        }
        response = requests.get(url_api, headers=headers, params=params)
        response.raise_for_status()
        datos = response.json()
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


