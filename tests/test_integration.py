import sys
sys.path.append("src")

from extract import Extractor
from transform import Clasificador
from utils.utils import obtener_fecha_hoy_ayer
import pandas as pd

def test_extractor():
    ayer,hoy = obtener_fecha_hoy_ayer()
    json_dict = Extractor(ayer,hoy).get_data_reports()

    for nombre,json_t in json_dict.items():
        path_xlsx = f'data/debug/{nombre}_extractor.xlsx'
        df = pd.DataFrame(json_t)
        df.to_excel(path_xlsx, index=False)

def test_clasificador():
    ayer = '2025/01/20'
    hoy = '2025/01/24'
    json_dict = Extractor(ayer,hoy).get_data_reports()

    df = Clasificador(json_dict['Data_Conversations']).main()

    df.to_excel('Prueba_clasificador.xlsx', index=False)

if __name__ == "__main__":
    test_clasificador()