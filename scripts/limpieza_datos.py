import pandas as pd
import logging as log 

def ejecutar_limpieza(df):
    #Fase 3 Limpieza de datos
    #Verifica nulls, duplicados y codifica variables segun metadata

    if df is None:
        return None
    
    try:
        log.info('Inicio de limpieza y transformacion de datos')
        print("Inicio de limpieza y transformacion de datos")

        #Eliminacion de duplicados
        df = df.drop_duplicates()
        log.info("duplicados eliminados")

        #Tratamiento de TotalCharges (Estandarizacion de datos)
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

        #Regla de negocio Si encuentra nulo en TotalCharges lo convierte en 0, Posible cliente nuevo.
        df['TotalCharges'] = df['TotalCharges'].fillna(0)
        log.info("Variable TotalCharges normalizada a float")

        #Codificacion de variables binarias a numericas
        #Campos afectados PArtner, Dependents, PhoneService, PaperLessBilling y Churn

        cols_binarias = [
            'Partner', 'Dependents', 'PhoneService', 'PaperLessBilling', 'Churn'
        ]

        for col in cols_binarias:
            if col in df.columns:
                df[col] = df[col].map({'Yes': 1, 'No': 0})

        log.info(f"Variables binarias codificadas: {cols_binarias}")

        #Ajuste de SeniorCitizen (asegurar tipo entero)
        
        if 'SeniorCitizen' in df.columns:
            df['SeniorCitizen'] = df['SeniorCitizen'].astype(int)

        print(f"Limpieza de datos completada")

       
        

        return df
    except Exception as e:
        error_msg = f"ERROR en fase 3 limpieza {e}"
        log.error(error_msg)
        print(f"{error_msg}")
        return None
    