import subprocess
import os
import zipfile
import db.db_data as dbData
import pandas as pd

def verify_credencials():
    if os.path.exists(os.getcwd() + "/API/kaggle.json"):
        return True
    else:
        return False

def unzip_dataset():
    with zipfile.ZipFile("./downloadedDataSet/predict-people-personality-types.zip", 'r') as zip_ref:
        zip_ref.extractall("./downloadedDataSet")  # Extrai todos os arquivos para o diretório especificado

    
def add_dataset_db():
    dbData.add_data_from_dataframe("./downloadedDataSet/data.csv")
    dbData.display_data_info()
    
def download_kaggle_dataset():
    if(verify_credencials()):
        os.environ['KAGGLE_CONFIG_DIR'] = os.getcwd()
        destination = "./downloadedDataSet"

        command = f'kaggle datasets download -d stealthtechnologies/predict-people-personality-types -p {destination}'
        try:
            subprocess.run(command, check=True, shell=True)
            unzip_dataset()
            add_dataset_db()
            return 200, "Sucesso"
        except subprocess.CalledProcessError as e:
            return 500, str(e)
    else:
        return 500, "Arquivo de credenciais não encontrado"
    

    