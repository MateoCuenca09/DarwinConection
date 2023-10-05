from datetime import datetime, timedelta
import requests
import pandas as pd
from PBI_funtions import mainPBI

days = 30 # Dias para atras que se quiere analizar

# Obtener la fecha actual
endDate = datetime.now().strftime("%Y/%m/%d")
# Obtener la fecha de 3 días atrás
startDate = (datetime.now() - timedelta(days)).strftime("%Y/%m/%d")
#startDate = '2023/08/01'


url_api = "https://api.botdarwin.com/data/conversations"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnQiOiJlZGlzdXIiLCJyb3V0ZXMiOlsiL2FnZW50cyIsIi9pbnRlbnRzIiwiL2RhdGEiXSwiaWF0IjoxNjg5Nzk1MDk1fQ.Iv4iye5d0uLJz2kTOu9GoEFGGtQGtGCyh-tn0EGCbP8"
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
