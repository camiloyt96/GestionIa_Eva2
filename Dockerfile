# 1. Usar una imagen oficial de Python compacta y estable
FROM python:3.9-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Instalar dependencias del sistema necesarias para compilar psutil y conectar a RDS (PostgreSQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# 4. Copiar el archivo de requerimientos primero para aprovechar la caché de Docker
COPY requirements.txt .

# 5. Instalar todas las librerías del proyecto sin almacenar caché para reducir el tamaño de la imagen
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar el resto del código del proyecto (scripts, data, main.py, streamlit_dashboard.py)
COPY . .

# 7. Exponer el puerto estándar que utilizará Streamlit
EXPOSE 8501

# 8. Configurar variables de entorno globales para Streamlit en entornos Cloud/Docker
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# 9. Comando por defecto para arrancar el servidor del Dashboard de forma persistente
CMD ["streamlit", "run", "streamlit_dashboard.py"]