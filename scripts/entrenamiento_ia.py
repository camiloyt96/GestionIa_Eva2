import pandas as pd
import logging as log
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def entrenar_modelo_churn(df):
    if df is None:
        return None
    
    try:
        log.info("Inicio del entrenamiento")
        print("Entrenando modelo con Random Forest")

        #1 Seleccion de variables Feature y Objetivo Target
        
        X = df.drop(['Churn'], axis=1)
        Y = df['Churn']

        X = pd.get_dummies(X)

        #2 Convertir variables categoricas restantes (Contract o InternetService)
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state=42)

        #creacion y entrenamiento de modelo
        modelo = RandomForestClassifier(n_estimators=100, random_state=42)
        modelo.fit(X_train, y_train)

        #4 Evaluacion
        preddicciones = modelo.predict(X_test)
        accuracy = accuracy_score(y_test, preddicciones)

        log.info(f"modelo Entrenado . accuracy: {accuracy:.4}")

        # Mostrar importancia de las variables (Top 5)
        importancias = pd.Series(modelo.feature_importances_, index=X.columns).sort_values(ascending=False)
        print("\nTop 5 factores que influyen en el Churn:")
        print(importancias.head(5))

        return modelo

    except Exception as e:
        print(f"Error en el entrenamiento: {e}")
        return None