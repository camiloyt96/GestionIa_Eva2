import pandas as pd
import logging 
import os 


#Configuracion de logs 
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename="logs/pipeline.log",
    level= logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def ejecutar_ingesta(path_csv):
    try:
        logging.info("Iniciando Ingesta de datos")

        #Lectura inicial del dataset
        df = pd.read_csv(path_csv)

        logging.info(f"Ingesta exitosa, registros cargados: {len(df)}")
        print(f"Ingesta exitosa registros cargados: {len(df)}")
        return df
    except Exception as e:
        logging.error(f"Error en la ingesta {e}")
        print(f"Error en la ingesta {e}")
        return None


if __name__ == "__main__":
    #prueba local
    df_raw = ejecutar_ingesta('data/datasetChurn.csv')
