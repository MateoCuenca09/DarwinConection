from extract import Extractor, RawDataSaver
from transform import Clasificador
from utils.utils import obtener_fecha_hoy_ayer,
import os

def main(fecha_inicio, fecha_fin):
    extractor = Extractor(fecha_inicio, fecha_fin)
    raw_data = extractor.get_df_conversations()

    raw_saver = RawDataSaver('data/raw')
    raw_saver.save_csv(raw_data, "conversations.csv")

    transformer = DataCleaner()
    clean_data = transformer.clean(raw_data)

    loader = DatabaseLoader()
    loader.load(clean_data)
