import pandas as pd
import logging as log
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, 
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score
)

def entrenar_modelo_churn(df):
    if df is None:
        return None
    
    try:
        log.info("Inicio del entrenamiento analítico del modelo")
        print("--- Iniciando Entrenamiento del Modelo (Random Forest) ---")

        # 1. Separación de características (Features) y variable objetivo (Target)
        # Aseguramos eliminar columnas de ID si existieran para no meter ruido al árbol
        columnas_a_drop = ['Churn']
        if 'customerID' in df.columns:
            columnas_a_drop.append('customerID')
            
        X = df.drop(columnas_a_drop, axis=1)
        Y = df['Churn']

        # 2. Convertir variables categóricas faltantes mediante One-Hot Encoding
        X = pd.get_dummies(X)

        # 3. Partición de datos (80% Entrenamiento / 20% Validación Ciega)
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # 4. Creación e Inferencia del Modelo Random Forest
        modelo = RandomForestClassifier(n_estimators=100, random_state=42)
        modelo.fit(X_train, y_train)

        # 5. Evaluación de Predicciones en el Conjunto de Test
        predicciones = modelo.predict(X_test)
        
        # 6. Cálculo de Métricas Clave de Clasificación
        accuracy = accuracy_score(y_test, predicciones)
        precision = precision_score(y_test, predicciones, pos_label=1, zero_division=0)
        recall = recall_score(y_test, predicciones, pos_label=1, zero_division=0)
        f1 = f1_score(y_test, predicciones, pos_label=1, zero_division=0)

        # 7. Exportación estructurada a Logs (Facilita la lectura directa en Streamlit)
        log.info(
            f"METRICAS_MODELO | Algoritmo: Random Forest | "
            f"Accuracy: {accuracy:.4f} | "
            f"Precision: {precision:.4f} | "
            f"Recall: {recall:.4f} | "
            f"F1_Score: {f1:.4f}"
        )

        # 8. Despliegue de Resultados Detallados en Consola
        print("\n================ REPORTES DE EVALUACIÓN ================")
        print(f"Exactitud General (Accuracy): {accuracy:.2%}")
        print("\nInforme de Clasificación Completo:")
        print(classification_report(y_test, predicciones, zero_division=0))
        print("========================================================")

        # Mostrar importancia de las variables estructurales (Top 5)
        importancias = pd.Series(modelo.feature_importances_, index=X.columns).sort_values(ascending=False)
        print("\n🔥 Top 5 factores críticos que influyen en el Churn:")
        print(importancias.head(5))

        return modelo

    except Exception as e:
        log.error(f"Falla crítica durante el proceso de entrenamiento de IA: {e}")
        print(f"Error en el entrenamiento: {e}")
        return None