import streamlit as st
import pandas as pd
import re
import os

# Configuración de la página del Dashboard
st.set_page_config(
    page_title="DataOps Dashboard - Performance",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Panel de Monitoreo Cloud & DataOps")
st.markdown("Este dashboard analiza en tiempo real las métricas de hardware (CPU y RAM) consumidas por cada etapa del pipeline extraídas de `pipeline_performance.log`.")

# Función interna para parsear el archivo de logs de forma limpia
def cargar_datos_log(ruta_log="data/pipeline_performance.log"):
    if not os.path.exists(ruta_log):
        st.error(f"El archivo de logs no se encuentra en la ruta: {ruta_log}. Asegúrate de ejecutar el pipeline principal primero.")
        return pd.DataFrame()
    
    registros = []
    
    # Expresión regular para extraer las métricas de forma exacta
    patron = r"METRICAS \| Etapa: (.*?) \| RAM_Script: (.*?) MB \| RAM_Sistema: (.*?)% \| CPU_Uso: (.*?)%"
    
    with open(ruta_log, "r", encoding="utf-8") as f:
        for linea in f:
            if "METRICAS" in linea:
                coincidencia = re.search(patron, linea)
                if coincidencia:
                    etapa = coincidencia.group(1)
                    ram_script = float(coincidencia.group(2))
                    ram_sistema = float(coincidencia.group(3))
                    cpu_uso = float(coincidencia.group(4))
                    
                    registros.append({
                        "Etapa": etapa,
                        "RAM Script (MB)": ram_script,
                        "RAM Sistema (%)": ram_sistema,
                        "Uso CPU (%)": cpu_uso
                    })
                    
    return pd.DataFrame(registros)

# Carga de datos
df_metricas = cargar_datos_log()

if not df_metrics.empty:
    # ---------------------------------------------------------
    # SECCIÓN 1: KPIs RESUMEN (Última iteración del Pipeline)
    # ---------------------------------------------------------
    st.subheader("🚀 Estado Actual del Último Pipeline Ejecutado")
    
    # Obtenemos las métricas de las etapas críticas de la última corrida
    ultima_ejecucion = df_metrics.tail(6) # Tomamos las últimas etapas registradas
    
    max_cpu = ultima_ejecucion["Uso CPU (%)"].max()
    max_ram_script = ultima_ejecucion["RAM Script (MB)"].max()
    ram_sistema_final = ultima_ejecucion["RAM Sistema (%)"].iloc[-1]
    
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric(label="Pico Máximo de CPU", value=f"{max_cpu}%", delta="Controlado")
    with kpi2:
        st.metric(label="Memoria RAM Máxima por Script", value=f"{max_ram_script:.2f} MB")
    with kpi3:
        st.metric(label="Uso RAM General del Sistema", value=f"{ram_sistema_final}%")
    
    st.markdown("---")
    
    # ---------------------------------------------------------
    # SECCIÓN 2: GRÁFICOS INTERACTIVOS DE RENDIMIENTO
    # ---------------------------------------------------------
    st.subheader("📈 Comportamiento de Recursos de Hardware por Etapa")
    
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.markdown("**Consumo de CPU por Etapa del Proceso**")
        # Gráfico de líneas dinámico nativo de Streamlit
        st.line_chart(df_metrics, x="Etapa", y="Uso CPU (%)", use_container_width=True)
        
    with col_der:
        st.markdown("**Uso de Memoria RAM (Script vs Sistema)**")
        # Graficamos el porcentaje de RAM ocupado en el entorno cloud
        st.line_chart(df_metrics, x="Etapa", y="RAM Sistema (%)", use_container_width=True)

    # ---------------------------------------------------------
    # SECCIÓN 3: TABLA DE DATOS CRUDA
    # ---------------------------------------------------------
    st.subheader("📋 Tabla Consolidada de Registros")
    st.dataframe(df_metrics, use_container_width=True)
    
    # Botón para forzar la actualización manual en el navegador
    if st.button("🔄 Actualizar Métricas"):
        st.rerun()

else:
    st.info("Esperando nuevos datos del pipeline... Ejecuta `main.py` para poblar el archivo de rendimiento.")