import schedule
import time
from datetime import datetime, timedelta
from main import main

 # URL de la API que deseas conectar
url_api = "https://api.testing.botdarwin.com/data/conversations"

# Token de autenticación requerido por la API
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnQiOiJlZGlzdXIiLCJyb3V0ZXMiOlsiL2FnZW50cyIsIi9pbnRlbnRzIiwiL2RhdGEiXSwiaWF0IjoxNjg2OTM3Nzc4fQ.F9Zdk2F50azIsgubt_HMMaQ5X20V-Iaw3UuJmcm27Qc"

# Obtener la fecha actual
endDate = datetime.now().strftime("%Y/%m/%d")

# Obtener la fecha de 7 días atrás
startDate = (datetime.now() - timedelta(days=7)).strftime("%Y/%m/%d")

main()


""" schedule.every().saturday.at("13:12").do(main)

# Mantener el programa en ejecución para que se realicen las tareas programadas
while True:
    schedule.run_pending()
    time.sleep(1) 
 """