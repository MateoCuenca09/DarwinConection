from datetime import datetime, timedelta
import requests
import pandas as pd
from PBI_funtions import mainPBI

days = 16 # Dias para atras que se quiere analizar

# Obtener la fecha actual
endDate = datetime.now().strftime("%Y/%m/%d")
# Obtener la fecha de 3 días atrás
startDate = (datetime.now() - timedelta(days)).strftime("%Y/%m/%d")
#startDate = '2023/08/01'



# URL y datos de inicio de sesión
login_url = "https://api.botdarwin.com/login"
login_data = {
    "username": "federico.caminal",
    "password": "ZuB947ZB!*Rk7_bAmR9!pE6YqHvATZ.."
}

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


