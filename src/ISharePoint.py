from office365.sharepoint.files.file import File
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
import os
from dotenv import load_dotenv
load_dotenv()
SITE = os.getenv('SITE_I') 
USER = os.getenv('USER_I') 
PASSWORD = os.getenv('PASSWORD_I') 
SITE_NAME = os.getenv('SITE_NAME') 
DOC = os.getenv('DOC') 
DARWIN = os.getenv('DARWIN') # Carpeta target

class ISharePoint():
    def _auth(self): return ClientContext(SITE).with_credentials(UserCredential(USER, PASSWORD))
    
    def get_file_content(self, archivo: str):
        with open(archivo, 'rb') as f: return f.read()

    def get_file_name(self, archivo: str): return archivo.split('/')[-1]
    
    def _upload_file(self, archivo: str, dir: str, contenido):
        ctx = self._auth()
        target_folder = f'/sites/{SITE_NAME}/{DOC}/{dir}'
        try:
            root = ctx.web.get_folder_by_server_relative_url(target_folder)
            root.upload_file(archivo, contenido).execute_query()
        except Exception as err: print(err)

    def _download_file(self, file_name, folder_name):
        conn = self._auth()
        file_url = f'/sites/{SITE_NAME}/{DOC}/{folder_name}/{file_name}'
        file = File.open_binary(conn, file_url)
        return file.content
    
    def _save_file(self, file_dir, file_name, file_obj):
        file_dir_path = file_dir + file_name
        with open(file_dir_path, 'wb') as f:
            f.write(file_obj)
    
    def upload_darwin(self, archivo: str): 
        return self._upload_file(self.get_file_name(archivo), DARWIN + "/Datos", self.get_file_content(archivo))
    
    def upload_logger(self):
        return self._upload_file('Avisos.txt', DARWIN + "/Datos", self.get_file_content('datos/Avisos.txt'))

    
    def download_ExcelDarwin(self):
        file_name = "Excel Darwin - PBI - Automatico.xlsx"
        file_dir = "src/docs/"
        file = self._download_file(file_name, DARWIN)
        self._save_file(file_dir, file_name, file)


    
if __name__ == '__main__':
    ISharePoint().upload_logger()
