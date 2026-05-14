import pandas as pd
import logging as log

def ejecutar_validacion(df):
    #Fase 4: Validacion de datos
    #Aplicar reglas semanticas

    if df is None:
        return None
    
    try:
        log.info("Iniciando validacion semantica")
        print("Iniciando validacion Semantica")

        #Regla 1 Tenure (No puede ser negativo)

        filas_iniciales = len(df)
        df = df[df['tenure'] >= 0]

        #Regla 2 MontlyCharges > 0 
        df = df[df['MonthlyCharges'] > 0]

        servicios_it = [
            'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
            'TechSupport', 'StreamingTV', 'StreamingMovies'
        ]

        # Transformar Internet Service
        if 'InternetService' in df.columns:
            mask_no_internet = (df['InternetService'] == 'No')
            for col in servicios_it:
                if col in df.columns:
                    df.loc[mask_no_internet, col] = 'No internet service'

        # 4. Validación Estructural: SeniorCitizen debe ser 0 o 1
        if 'SeniorCitizen' in df.columns:
            df['SeniorCitizen'] = df['SeniorCitizen'].astype(int)

        filas_finales = len(df)
        descartados = filas_iniciales - filas_finales
        
        log.info(f"Validación exitosa. Registros descartados: {descartados}")
        print(f"✅ Validación terminada. Registros válidos: {filas_finales}")
        
        return df

    except Exception as e:
        error_msg = f"ERROR en fase 4 validación: {str(e)}"
        log.error(error_msg)
        print(f"{error_msg}")
        return None