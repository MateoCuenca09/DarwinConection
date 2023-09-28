from datetime import datetime, timedelta
import requests
import pandas as pd
from PBI_funtions import mainPBI


# URL de la API que deseas conectar
url_api = "https://api.botdarwin.com/data/conversations"

# Token de autenticación requerido por la API
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnQiOiJlZGlzdXIiLCJyb3V0ZXMiOlsiL2FnZW50cyIsIi9pbnRlbnRzIiwiL2RhdGEiXSwiaWF0IjoxNjg5Nzk1MDk1fQ.Iv4iye5d0uLJz2kTOu9GoEFGGtQGtGCyh-tn0EGCbP8"

# Obtener la fecha actual
#endDate = datetime.now().strftime("%Y/%m/%d")
endDate = '9/27/2023'
# Obtener la fecha de 3 días atrás
#startDate = (datetime.now() - timedelta(days=3)).strftime("%Y/%m/%d")
startDate = '9/24/2023'
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
