


import pandas as pd
from datetime import datetime, timedelta
from main import descargar_datos_desde_api

# URL de la API que deseas conectar
url_api = "https://api.botdarwin.com/data/conversations"

# Token de autenticación requerido por la API
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnQiOiJlZGlzdXIiLCJyb3V0ZXMiOlsiL2FnZW50cyIsIi9pbnRlbnRzIiwiL2RhdGEiXSwiaWF0IjoxNjg5Nzk1MDk1fQ.Iv4iye5d0uLJz2kTOu9GoEFGGtQGtGCyh-tn0EGCbP8"

# Obtener la fecha actual
endDate = datetime.now().strftime("%Y/%m/%d")

# Obtener la fecha de 7 días atrás
startDate = (datetime.now() - timedelta(days=44)).strftime("%Y/%m/%d")

datos = descargar_datos_desde_api(url_api, token, startDate, endDate)

df = pd.DataFrame(datos)
df.to_excel("DatosDescarga.xlsx",index=False)

from PBI import mainPBI         
mainPBI(datos)  

