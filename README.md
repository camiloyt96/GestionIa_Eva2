# 🤖 IA predictiva de Churn para empresa de Telecomunicaciones

> Documento técnico de diseño del sistema — Versión 2.0 · 2026  
> **Integrantes:** Galio Soto & Camilo Yañez

---

## 📌 Tabla de Contenidos

- [Introducción](#introducción)
- [Descripción Técnica del Sistema](#descripción-técnica-del-sistema)
  - [Componentes Técnicos](#componentes-técnicos)
  - [Estructura General](#estructura-general)
  - [Tecnologías Utilizadas](#tecnologías-utilizadas)
  - [Relación entre Componentes](#relación-entre-componentes)
- [Diagrama Técnico de la Solución](#diagrama-técnico-de-la-solución)
- [Modelo de Datos y Diccionario](#modelo-de-datos-y-diccionario)
  - [Entidades y Relaciones](#entidades-y-relaciones)
  - [Diccionario de Datos](#diccionario-de-datos)
- [Instrucciones de Instalación](#instrucciones-de-instalación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Ejemplo de Uso de la API](#ejemplo-de-uso-de-la-api)
- [Contribución y Versionado](#contribución-y-versionado)

---

## Introducción

Este proyecto desarrolla un sistema de inteligencia artificial orientado a la prediccion de abandono de clientes(Customer Churn) en una empresa de telecomunicaciones.

El objetivo principal es identificar patrones de comportamiento y variables criticas que permitan anticipar que clientes tienen mayor porabilidad de cancelar sus servicios, facilitando la implementacion de estrategias de retencion personalizadas.

El sistema es capaz de:
Analizar datos demograficos, financieros y servicios contratados de los clientes.
Procesar y transformar grandes volumenes de datos.
Detectar patrones asociados al abandono del servicio.
Generar predicciones de Churn mediante modelos de DeepLearning (Random Forest)
Entregar insights accionables para areas comerciales y de retencion.
Exponer resultados mediante una API y Dashboard Interactivo.
---

## Descripción Técnica del Sistema

### Componentes Técnicos

| # | Componente | Descripción |
|---|-----------|-------------|
| 1 | **Ingesta de datos** | Scripts para procesar CSV  |
| 2 | **Limpieza y validación** | Normalización y control de calidad de los datos, limpieza de datos nulos e inconsistencias. |
| 3 | **Transformacion de datos** | Enconding de variables categoricas y feature engineering |
| 4 | **Analisis exploratorio (EDA)** | Deteccion de Patrones y correlacion relevante |
| 5 | **Modelo predictivo** | Algoritmo ML para clasificacion de clientes con Churn |
| 6 | **API Backend** | Servicio para consultar predicciones y resultados a traves de http |
| 7 | **Base de datos** | PostgreSQL para almacenamiento de datos persistente |
| 8 | **Frontend** | Dashboard web/app para visualización en React |

---

### Estructura General

El sistema sigue una arquitectura **modular basada en pipeline de datos y microservicios**:

```
┌─────────────┐    ┌──────────────┐    ┌───────────────┐
│   Ingesta   │───▶│ Procesamiento│───▶│   Modelado    │
│ CSV/API/    │    │ Limpieza,    │    │ Predicciones  │
│ Manual      │    │ Transformac. │    │ Recomendac.   │
└─────────────┘    └──────────────┘    └───────┬───────┘
                                               │
                   ┌──────────────┐    ┌───────▼───────┐
                   │  Frontend    │◀───│   API Layer   │
                   │ React /      │    │  FastAPI /    │
                   │ Streamlit    │    │  Flask        │
                   └──────────────┘    └───────────────┘
```

Cada capa opera de forma independiente, lo que permite **escalabilidad**, fácil mantenimiento e integración con nuevas fuentes de datos.

---

### Tecnologías Utilizadas

| Área | Tecnología |
|------|-----------|
| **Lenguaje** | Python 3 |
| **Procesamiento de datos** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn, TensorFlow |
| **Base de datos** | PostgreSQL |
| **Backend / API** | FastAPI o Flask |
| **Frontend** | React o Streamlit |
| **Control de versiones** | GitHub |
| **Despliegue** | Docker *(opcional)* |

---

### Relación entre Componentes

El flujo completo del sistema es:

```
Ingesta → Limpieza → Transformación → Modelado → Recomendación → API → Usuario
```

1. Los datos ingresan desde múltiples fuentes (CSV, APIs bancarias, input manual)
2. Se limpian, transforman y almacenan en **PostgreSQL**
3. Los modelos generan **predicciones financieras** (ahorro, gasto, riesgo)
4. El motor de recomendaciones traduce los resultados en **consejos accionables**
5. La API entrega estos resultados al **frontend** para su visualización

---

## Diagrama Técnico de la Solución

> ⚠️ **Pendiente:** Incluir diagrama que represente:
> - Flujo de datos completo
> - Componentes principales del sistema
> - Conexiones entre base de datos, modelos y API
> - Interacción con el usuario
>
> **Herramientas sugeridas:** [draw.io](https://draw.io) · [Lucidchart](https://lucidchart.com) · [Figma](https://figma.com)

---

## Modelo de Datos y Diccionario

### Entidades y Relaciones

```
Usuario (1) ──────────── (N) Transacciones
                               │
                               └──── (1) Categorías

Usuario (1) ──────────── (N) Recomendaciones
Usuario (1) ──────────── (N) Predicciones (por periodo)
```

**Entidades principales:**
- `Usuario` — Perfil e identificación del usuario
- `Transacciones` — Movimientos financieros del usuario
- `Categorías` — Clasificación de gastos e ingresos
- `Recomendaciones` — Consejos generados por la IA
- `Predicciones` — Proyecciones financieras por periodo

---

### Diccionario de Datos

| Campo | Tipo | Descripción | Restricciones | ¿Obligatorio? |
|-------|------|-------------|---------------|:-------------:|
| `usuario_id` | `INT` | Identificador único del usuario | Entero positivo | ✅ |
| `fecha` | `DATE` | Fecha de la transacción | Formato `yyyy-mm-dd` | ✅ |
| `monto` | `FLOAT` | Monto de la transacción | Positivo o negativo | ✅ |
| `categoria` | `VARCHAR` | Tipo de gasto o ingreso | Alimentación, transporte, etc. | ✅ |
| `descripcion` | `TEXT` | Detalle libre de la transacción | Texto libre | ❌ |
| `ingreso` | `BOOLEAN` | Indica si es ingreso o gasto | `0`: gasto · `1`: ingreso | ✅ |
| `ahorro_estimado` | `FLOAT` | Ahorro proyectado | `>= 0` | ❌ |
| `riesgo_financiero` | `FLOAT` | Score de riesgo del usuario | Rango `0` a `1` | ❌ |
| `recomendacion` | `TEXT` | Consejo generado por la IA | Texto libre | ❌ |

---

## Instrucciones de Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/<usuario>/<repositorio>.git
cd <repositorio>

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con las credenciales de PostgreSQL y APIs

# 5. Inicializar la base de datos
python scripts/init_db.py

# 6. Ejecutar la aplicación
uvicorn app.main:app --reload  # Con FastAPI
# o
python app.py                   # Con Flask
```

> **Nota:** Para despliegue con Docker, consultar `docker-compose.yml` en la raíz del proyecto.

---

## Estructura del Proyecto

```
📁 GestionIa_Eva2/
├── 📁 data/
│   ├── raw/                  # Datos crudos (CSV, exports)
│   └── processed/            # Datos limpios listos para modelar
├── 📁 scripts/
│   ├── ingest.py             # Script de ingesta de datos
│   ├── clean.py              # Limpieza y validación
│   ├── categorize.py         # Categorización de gastos
│   └── init_db.py            # Inicialización de la base de datos
├── 📁 models/
│   ├── predictor.py          # Modelo de predicción financiera
│   └── recommender.py        # Motor de recomendaciones
├── 📁 app/
│   ├── main.py               # Punto de entrada de la API
│   ├── routes/               # Endpoints de la API
│   └── schemas/              # Modelos Pydantic / validación
├── 📁 frontend/              # React o Streamlit dashboard
├── 📁 tests/                 # Tests unitarios e integración
├── 📄 requirements.txt
├── 📄 docker-compose.yml
├── 📄 .env.example
└── 📄 README.md
```

---

## Ejemplo de Uso de la API

### Obtener recomendaciones para un usuario

```http
GET /api/v1/recomendaciones/{usuario_id}
```

**Respuesta exitosa (`200 OK`):**

```json
{
  "usuario_id": 42,
  "periodo": "2026-04",
  "recomendaciones": [
    {
      "tipo": "ahorro",
      "mensaje": "Podrías ahorrar $35,000 reduciendo gastos en entretenimiento.",
      "prioridad": "alta"
    },
    {
      "tipo": "inversion",
      "mensaje": "Tu perfil de riesgo es moderado. Se sugiere diversificar en fondos indexados.",
      "prioridad": "media"
    }
  ],
  "riesgo_financiero": 0.34,
  "ahorro_estimado": 35000.0
}
```

### Registrar una transacción

```http
POST /api/v1/transacciones
Content-Type: application/json

{
  "usuario_id": 42,
  "fecha": "2026-04-01",
  "monto": -8500.0,
  "categoria": "alimentación",
  "descripcion": "Supermercado",
  "ingreso": false
}
```

---

## Contribución y Versionado

Este proyecto sigue el estándar de **Semantic Versioning** (`MAJOR.MINOR.PATCH`).

```bash
# Crear una nueva rama para cada feature
git checkout -b feature/nombre-del-feature

# Commit con mensajes descriptivos
git commit -m "feat: agregar categorización automática por ML"

# Abrir Pull Request hacia main con descripción del cambio
```

**Convención de commits recomendada:**

| Prefijo | Uso |
|---------|-----|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de bugs |
| `docs:` | Cambios en documentación |
| `refactor:` | Refactorización de código |
| `test:` | Adición o modificación de tests |

---

> 📄 Este documento debe actualizarse continuamente conforme evolucionen los modelos, se integren nuevas fuentes de datos o cambie la arquitectura del sistema.  
> **Última actualización:** Abril 2026 · Galio Soto & Camilo Yañez
