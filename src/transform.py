import pandas as pd
from dateutil import parser
from datetime import datetime, timezone, timedelta
from model.modelo import Modelo_Darwin

class Clasificador:
    """  
    JSON goes in, DF goes out
    """
    def __init__(self, datos):
        self.datos_json = datos # data in
        self.datos_df = pd.DataFrame(datos) # data in
        
    def main(self):
        self.correcion_zona_horaria()
        df_process = Modelo_Darwin(self.datos_df).main()
        return df_process

    def correcion_zona_horaria(self, df = None):
        """  
        Corrector de Zona Horaria UTC-3 a UTC-0
        :param df: DataFrame a corregir. Si no se pasa, se usa self.datos_df
        """
        if df is None:
            df = self.datos_df
        df["date"] = df["date"].apply(self._convert_to_local_timezone)
        df["date"] = df["date"].dt.tz_localize(None)
        self.datos_df = df
        return df

    def _convert_to_local_timezone(self, date_str):

        utc_minus_3 = timezone(timedelta(hours=-3))
        # Convertir la fecha a datetime (soporta cualquier formato ISO)
        date_obj = parser.isoparse(date_str)
        # Convertir a UTC-3
        return date_obj.astimezone(utc_minus_3)
    
    def add_metadata(self, df_process):
        """  
        Adds data of procesing time, batch, path to raw.
            * Version del modelo
            * Fecha de la ejecución del clasificador
            * Ruta al archivo crudo
        """
        df_process['model_version'] = 'darwinModel_1.0.0'
        df_process['process_time'] = datetime.now()
        df_process['raw_path'] = ''