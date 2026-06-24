from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import time
import logging as log
import psutil                                        

load_dotenv()

from scripts.ingesta_datos import ejecutar_ingesta
from scripts.limpieza_datos import ejecutar_limpieza
from scripts.validacion import ejecutar_validacion 
from scripts.entrenamiento_ia import entrenar_modelo_churn

# 1. Limpiamos cualquier configuración previa que hayan hecho los sub-scripts importados
for handler in log.root.handlers[:]:
    log.root.removeHandler(handler)

# 2. Forzamos la configuración correcta para el Pipeline y Streamlit
log.basicConfig(
    level=log.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        log.FileHandler("data/pipeline_performance.log", mode='a', encoding='utf-8'),
        log.StreamHandler()  # Mantiene la salida visual en la consola de EC2
    ]
)

def run_pipeline():
    path_csv = 'data/datasetChurn.csv'
    log.info("=== INICIANDO EJECUCIÓN DEL PIPELINE DATAOPS ===")
    dataPipeline(path_csv)
    log.info("=== PIPELINE FINALIZADO EXITOSAMENTE ===")
   
def registrar_metricas(etapa, proceso):
    """
    Captura métricas de hardware y las exporta estructuradamente al log.
    El formato 'METRICAS | ...' facilita el filtrado y lectura en Streamlit.
    """
    # RAM consumida específicamente por este script y sus subprocesos (en MB)
    ram_script = proceso.memory_info().rss / (1024**2)
    # Porcentaje de uso de la RAM total del servidor/sistema
    ram_sistema_pct = psutil.virtual_memory().percent
    # Uso de CPU (interval=0.1 evita lecturas en 0.0 bloqueando levemente para medir el diferencial)
    cpu_uso_pct = psutil.cpu_percent(interval=0.1)
    
    log.info(
        f"METRICAS | Etapa: {etapa} | "
        f"RAM_Script: {ram_script:.2f} MB | "
        f"RAM_Sistema: {ram_sistema_pct:.1f}% | "
        f"CPU_Uso: {cpu_uso_pct:.1f}%"
    )

def dataPipeline(csv_path):
    proceso = psutil.Process(os.getpid())
    start_time = time.time()
    
    registrar_metricas('Inicio', proceso)
    df_raw = ejecutar_ingesta(csv_path)
    
    registrar_metricas('Ingesta', proceso)
    if df_raw is not None:
        total_inicial = len(df_raw)
        
        # FASE 3: LIMPIEZA
        df_clean = ejecutar_limpieza(df_raw)
        registrar_metricas('Limpieza', proceso)
        
        if df_clean is not None:
            # FASE 4: VALIDACIÓN 
            df_final = ejecutar_validacion(df_clean)
            registrar_metricas('Validacion', proceso)
            
            if df_final is not None:
                total_final = len(df_final)
            
                # Guardar resultado final intermedio
                df_final.to_csv('data/dataset_final_validado.csv', index=False)

                # FASE 6: MONITOREO (KPI)
                end_time = time.time()
                duracion = end_time - start_time
                completitud = (total_final / total_inicial) * 100

                # Ejecución del Entrenamiento de Modelos
                log.info("Iniciando entrenamiento analítico de modelos de IA...")
                modelo = entrenar_modelo_churn(df_final)
                registrar_metricas('Entrenamiento_IA', proceso)
                
                # Registro de KPIs de Negocio en Logs
                log.info(f"KPI_NEGOCIO | Latencia_Total: {duracion:.2f}s | Completitud: {completitud:.2f}% | Registros_Validos: {total_final}")
                log.info("Archivo local generado de manera correcta en data/dataset_final_validado.csv")
    else:
        log.error("Error crítico: No se pudo iniciar el pipeline por fallo en la ingesta de datos.")
        return None
    
    log.info("Iniciando subida del set de datos final a la base de datos distribuida RDS...")
    try:
        db_host = os.getenv("DB_HOST")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME", "postgres")
        db_port = os.getenv("DB_PORT", "5432")

        connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(connection_string)
        
        df_final.to_sql('dataset_churn_final', engine, if_exists='replace', index=False)
        log.info("¡Dataset persistido exitosamente en Amazon RDS PostgreSQL!")
        registrar_metricas('Carga_RDS', proceso)
        
    except Exception as e:
        log.error(f"Falla crítica en la conexión o carga hacia la base de datos: {e}")

if __name__ == "__main__":
    run_pipeline()