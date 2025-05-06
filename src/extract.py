from utils.DarwinConn import API_Darwin
import pandas as pd
import os, datetime
from dotenv import load_dotenv
load_dotenv()

class Extractor:
    """  
    """
    def __init__(self, startDate, endDate):
        """  
            :param startDate: datetime %Y/%m/%d
            :param endDate: datetime %Y/%m/%d
        """
        self.Api_Darwin = API_Darwin()
        self.startDate = startDate
        self.endDate = endDate
        pass
    
    def get_data_reports(self):
        json_conversations = self.Api_Darwin.get_data_conversations(self.startDate,self.endDate)
        json_feedback = self.Api_Darwin.get_data_feedback(self.startDate,self.endDate)
        json_noMatch = self.Api_Darwin.get_data_noMatch(self.startDate,self.endDate)

        data_dict = {
            'Data_Conversations':json_conversations,
            'Data_Feedback':json_feedback,
            'Data_NoMatch':json_noMatch
        }
        return data_dict

    def get_reports(self):
        self.Api_Darwin.get_report_loggedPerDay(self.startDate,self.endDate)
        self.Api_Darwin.get_report_interactionsMonth(self.startDate,self.endDate)    
        self.Api_Darwin.get_report_feedback(self.startDate,self.endDate)

    def get_df_conversations(self):
        json_conversations = self.Api_Darwin.get_data_conversations(self.startDate,self.endDate)
        df_conversations = pd.DataFrame(json_conversations)
        return df_conversations


class RawDataSaver:
    def __init__(self, base_path):
        self.base_path = base_path

    def _get_month_folder(self):
        hoy = datetime.date.today()
        return hoy.strftime("%Y-%m")  # "2025-04"

    def save_csv(self, df, datatype):
        folder = os.path.join(self.base_path, self._get_month_folder())
        os.makedirs(folder, exist_ok=True)  # Crea la carpeta si no existe

        filename = datetime.date.today() + datatype
        full_path = os.path.join(folder, filename)
        df.to_csv(full_path, index=False)
        print(f"Archivo guardado en: {full_path}")

if __name__ == '__main__':
    pass