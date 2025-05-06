from office365.sharepoint.files.file import File
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from tqdm.auto import tqdm

# USER & P4SS
load_dotenv()
USER = os.getenv('USER_I') 
PASSWORD = os.getenv('PASSWORD_I') 

# SITIO WEB
SITE = "https://grupoedisur.sharepoint.com/sites/AtencionalCliente/"
SITE_NAME = "AtencionalCliente"
DOC = "Documentos Compartidos"
ROOT_FOLDER = "Darwin"


class SharePoint_Conn():
    def __init__(self):
        self.conn = ClientContext(SITE).with_credentials(UserCredential(USER, PASSWORD))

    def check_credentials():
        print(f"""
        User: {USER}
        Password: {PASSWORD}
              """)
        
    def get_file_content(self, archivo: str):
        with open(archivo, 'rb') as f: return f.read()

    def get_file_name(self, archivo: str): return archivo.split('/')[-1]
    
    def _download_file(self, file_name):
        file_url = f'/sites/{SITE_NAME}/{DOC}/{ROOT_FOLDER}/{file_name}'
        file = File.open_binary(self.conn, file_url)
        return file.content

    def _download_save_file(self, file_url,filename ,local_folder_path):
        # Obtener el archivo desde SharePoint
        file = File.open_binary(self.conn, file_url)

        local_path = local_folder_path + '/' + filename
        # Guardar el archivo localmente
        with open(local_path, "wb") as local_file:
            local_file.write(file.content)
        
        return local_path 
    
    def _save_file(self, file_dir, file_name, file_obj):
        file_dir_path = file_dir + file_name
        with open(file_dir_path, 'wb') as f:
            f.write(file_obj)

    def _upload_file(self, file_name: str, dir_tar: str, dir_loc:str):
        """  
        :param file_name: Name target for SharePoint, str as 'Prueba.xlsx'
        :param dir_tar: str as 'Generacion VEPS/2025-01/Informes VEP'
        :param dir_loc: str'out/2025-01-16/INFORME VEPS AL 14-01-2025 robot.xlsx'
        """
        target_folder = f'/sites/{SITE_NAME}/{DOC}/{dir_tar}'
        try:
            root = self.conn.web.get_folder_by_server_relative_url(target_folder)
            with open(dir_loc, 'rb') as file_content:
                root.upload_file(file_name, file_content).execute_query()
        except Exception as err: print(err)

    def _upload_fold(self, path_folder, folder_dest):
        archivos_in_folder = os.listdir(path_folder)
        for archivo in tqdm(archivos_in_folder, desc="Subiendo archivos"):
            path_arch = path_folder + archivo
            self._upload_file(file_name=archivo, dir_tar=folder_dest, dir_loc=path_arch)

    def _upload_fold_from_list(self,path_folder, name_files, dir_tar):
        """  
        :param path_folder: path to local folder, str.
        :param name_files: list with only the names of local files to upload, [''].
        :param dir_tar: SharePoint path, str ''Generacion VEPS/2025-01/Informes VEP''
        """
        for archivo in tqdm(name_files, desc="Subiendo archivos"):
            path_arch = os.path.join(path_folder,archivo)
            self._upload_file(file_name=archivo, dir_tar=dir_tar, dir_loc=path_arch)

    def _create_folder_in_root(self,name_folder):
        """"
        """
        web = self.conn.web
        # Obtén la biblioteca de documentos
        tar_path = f'/sites/{SITE_NAME}/{DOC}/{ROOT_FOLDER}'
        library = web.get_folder_by_server_relative_path(tar_path)

        # Crea la nueva carpeta
        library.add(name_folder).execute_query()   
        return tar_path + '/' + name_folder
    
    def _create_folder(self,path,name_folder):
        """  
        path: 'folder_1/folder_2'
        name_folder: 'namefolder'
        """
        web = self.conn.web
        # Obtén la biblioteca de documentos
        tar_path = f'/sites/{SITE_NAME}/{DOC}/{ROOT_FOLDER}/{path}'
        library = web.get_folder_by_server_relative_path(tar_path)

        # Crea la nueva carpeta
        library.add(name_folder).execute_query()   
        return tar_path + '/' + name_folder        

    def _list_root_folder(self):
        """  
        returns: FOLDERS in root folder! NOT FILES
        """

        # Obtener la carpeta
        folder = self.conn.web.get_folder_by_server_relative_path(f'/sites/{SITE_NAME}/{DOC}/{ROOT_FOLDER}')
        items = folder.folders  # Cambia a `folder.folders` para obtener subcarpetas
        self.conn.load(items)
        self.conn.execute_query()

        folder_items = []
        for item in items:
            folder_items.append({
                "name": item.name,
                "url": item.serverRelativeUrl
            })
        return folder_items

    def _list_folder_files(self, folder_url):
        folder = self.conn.web.get_folder_by_server_relative_url(folder_url)
        files = folder.files.get().execute_query()
        return files

    def _listar_elementos(self):
        web = self.conn.web
        # Obtener la biblioteca de documentos
        library = web.lists.get_by_title('Documentos Compartidos/Datos')
        self.conn.load(library)
        self.conn.execute_query()

        # Obtener la carpeta anidada
        root_folder = library.root_folder
        print(root_folder.folders)
        subfolder = root_folder.folders.get_by_path('Datos')
        subfolder = subfolder.folders.get_by_path('Cedulones')
        self.conn.load(subfolder)
        self.conn.execute_query()

        # Listar el contenido de la carpeta anidada
        items = subfolder.files
        self.conn.load(items)
        self.conn.execute_query()

        for item in items:
            print(f"Nombre del archivo: {item.name}")


class SharePoint_Tools():
    def __init__(self):
        self.SP_conn = SharePoint_Conn()

    def find_month_folder(self):
        folders = self.SP_conn._list_root_folder()
        for folder in folders:
            if folder['name'] == str(datetime.now().strftime('%Y-%m')): return True
        return False

    def get_month_folder(self):
        """  
        Busca la carpeta en formato aaaa-mm, si no la encuentra, la crea y devuelve!
        """
        folders = self.SP_conn._list_root_folder()
        for folder in folders:
            if folder['name'] == str(datetime.now().strftime('%Y-%m')): return folder['url']
        folder_url = self.SP_conn._create_folder_in_root(name_folder=str(datetime.now().strftime('%Y-%m')))
        self.SP_conn._create_folder(path=str(datetime.now().strftime('%Y-%m')),name_folder='Docs VEPS')
        self.SP_conn._create_folder(path=str(datetime.now().strftime('%Y-%m')),name_folder='Informes VEPS')

        return folder_url

    def daily_check_file(self, last_check_time):
        """  
        Returns: 
        * True if new file in folder month
        * False if not new files
        """

        folder_url = self.get_month_folder()
        news_xlsx = self.check_new_xlsx_files(folder_url, last_check_time)

        if news_xlsx: return True
        if not news_xlsx: return False

    def check_new_xlsx_files(self, folder_url, last_check_time):
        """
        Verifica si hay nuevos archivos .xlsx en una carpeta de SharePoint.

        Args:
            folder_url (str): La URL relativa de la carpeta en SharePoint (e.g., "/sites/misitio/DocumentosCompartidos/micarpeta").
            last_check_time (datetime): Fecha y hora de la última vez que se revisaron los archivos.

        Returns:
            list: Lista de nombres de los nuevos archivos .xlsx encontrados.
        """
        # Obtener la carpeta
        files = self.SP_conn._list_folder_files(folder_url)
        
        new_files = []
        
        for file in files:
            # Convertir la fecha de modificación del archivo a datetime
            modified_time = file.time_last_modified        
            if isinstance(modified_time, datetime):pass
            else: modified_time = datetime.strptime(modified_time, "%Y-%m-%dT%H:%M:%SZ")
            # Verificar si es un archivo .xlsx y si es más reciente que el último chequeo
            if file.name.endswith(".xlsx") and modified_time > last_check_time:
                new_files.append(file.name)
        
        return new_files

    def get_new_xlsx_file(self, folder_tar,last_check_time):
        """  
        Descarga y guarda en la carpeta los xlsx nuevos del Sharepoint

        :param last_check_time: Che culiado mas vale que me pases un obj datetime datetime
        :return: paths locales de los archivos descargados
        """

        folder_url = self.get_month_folder()
        news_xlsx = self.check_new_xlsx_files(folder_url, last_check_time)
        local_paths = []
        for new in news_xlsx:
            path_new = folder_url + '/' + new
            local_path = self.SP_conn._download_save_file(path_new,new,folder_tar)
            local_paths.append(local_path)

        return local_paths

    def upload_filetype_from_folder(self, local_folder, folder_dest, filetype):
        """  
        :param local_folder: path to local folder
        :param folder_dest: SharePoint path to folder as '2025-01/Informes VEP'
        :param filetype: ending type of file as '.xlsx'
        """
        dir_tar = f'{ROOT_FOLDER}/{folder_dest}'
        # Filter and list all PDF files in the folder
        name_files = [
            archivo for archivo in os.listdir(local_folder)
            if archivo.endswith(f'{filetype}')
        ]

        self.SP_conn._upload_fold_from_list(local_folder, name_files, dir_tar)

if __name__ == '__main__':
    pass