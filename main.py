import time
import logging as log
from scripts.ingesta_datos import ejecutar_ingesta
from scripts.limpieza_datos import ejecutar_limpieza
from scripts.validacion import ejecutar_validacion # Verifica que el archivo se llame validacion_datos.py
from scripts.entrenamiento_ia import entrenar_modelo_churn

def run_pipeline():
    # Ruta del archivo (Fase 2)
    path_csv = 'data/datasetChurn.csv'

    #Proceso de dataOps
    dataPipeline(path_csv)
   


def dataPipeline(csv_path):
     
    df_raw = ejecutar_ingesta(csv_path)
    start_time = time.time()
    if df_raw is not None:
        total_inicial = len(df_raw)
        
        #FASE 3: LIMPIEZA
        df_clean = ejecutar_limpieza(df_raw)

        if df_clean is not None:
            #FASE 4: VALIDACIÓN 
            df_final = ejecutar_validacion(df_clean)

            if df_final is not None:
                total_final = len(df_final)

                # Guardar resultado final 
                df_final.to_csv('data/dataset_final_validado.csv', index=False)

                #FASE 6: MONITOREO (KPI)
                end_time = time.time()
                duracion = end_time - start_time
                completitud = (total_final / total_inicial) * 100


                modelo = entrenar_modelo_churn(df_final)
                
                print(f"Resumen de Ejecucion (KPI)")
                print(f"Latencia: {duracion:.2f} segundos")
                print(f"Completitud: {completitud:.2f}% (Validos: {total_final})")
                print(f"Archivo generado: data/dataset_final_validado.csv")
                
    else:
        print(" Error: No se pudo iniciar el pipeline por fallo en la ingesta.")
        return None

if __name__ == "__main__":
    run_pipeline()