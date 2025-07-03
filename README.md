# 📦 Ecommerce Data Pipeline

Este proyecto permite cargar archivos de settlement de Amazon (en formato CSV), normalizar los datos por cliente y almacenarlos en una base de datos PostgreSQL con un modelo tipo copo de nieve. Luego se puede usar para reporting y visualización web.

---

## 🔧 Requisitos

- Python 3.8+
- PostgreSQL (local o remoto)
- pgAdmin (para ejecutar stored procedures)
- pip + virtualenv
- Archivo `.env` con conexión a PostgreSQL

---

## 📁 Estructura del proyecto

```
ecommerce-dashboard/
├── api/                       # API Flask para recibir archivos
├── data/                      # Carpeta donde se guarda 1 subcarpeta por cliente
│   └── prune/
│       └── upload_settlement.csv
├── etl/
│   ├── load_all_clients.py    # ETL multi-cliente desde archivos
│   └── run_all_procedures.py  # Ejecuta stored procedures por cliente
├── .env                       # Configuración de conexión a PostgreSQL
├── app.py                     # Script para correr la API
└── README.md
```

---

## ⚙️ 1. Configuración inicial

Crear archivo `.env`:

```env
DATABASE_URL=postgresql://usuario:clave@localhost:5432/ecommerce
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## 🚀 2. Correr la API localmente

```bash
python app.py
```

Luego, podés subir archivos usando Postman:

- Endpoint: `POST http://localhost:5000/upload`
- Body → form-data:
  - `client_id`: nombre del cliente (ej: `prune`)
  - `file`: archivo CSV de settlement

El archivo se guarda como:  
`data/<client_id>/upload_<original_filename>.csv`

---

## 🛠️ 3. ETL - Cargar datos a PostgreSQL

Ejecutá este script para recorrer todas las carpetas de `data/` y cargar el archivo a la tabla `raw_amazon_settlement` dentro del esquema del cliente:

```bash
python etl/load_all_clients.py
```

Este script:
- Crea el esquema si no existe
- Crea la tabla `raw_amazon_settlement` si no existe
- Inserta los datos desde el CSV

---

## 🧠 4. Stored Procedures

### Los SPs en pgAdmin están en el schema public.

#### 📌 SP 1: `etl_raw_to_stg`
- Limpia y mueve datos desde `raw` a `stg`
- Reemplaza vacíos por NULL
- Aplica tipos de datos

#### 📌 SP 2: `etl_stg_to_prod`
- Crea `dim_catalog`, `dim_mapping_table`
- Pobla `prod_settlement_fact` con FK y datos de negocio

📌 Ejecutalos una vez por esquema en pgAdmin:

```sql
CALL prune.etl_raw_to_stg();
CALL prune.etl_stg_to_prod();
```
o todos juntos:
```bash
python etl/run_all_procedures.py
```

---

## 🤖 5. Automatizar ejecución de Stored Procedures

Ejecutá este script para llamar a los SPs por cada cliente en `data/`:

```bash
python etl/run_all_procedures.py
```

---

## 🕒 6. Automatizar por cron (opcional, en Linux/WSL)

Editar crontab:

```bash
crontab -e
```

Agregar:

```cron
0 3 * * * /usr/bin/python3 /ruta/al/proyecto/etl/run_all_procedures.py >> /ruta/log_etl.log 2>&1
```

---

## 📊 Próximamente

- Visualización web (dashboard por cliente)
- Gráficos con indicadores clave




# 🛠 Ecommerce Dashboard Portal

Este proyecto es un portal web construido con **Flask** y **Plotly.js** que permite visualizar reportes de Profit & Loss para distintos clientes en base a datos procesados previamente en una base de datos PostgreSQL.

---

## 🚀 Estructura del Proyecto

```
ecommerce-dashboard/
├── app.py                    # Lanza la app Flask
├── portal/
│   ├── __init__.py           # Blueprint 'portal'
│   ├── views.py              # Renderiza el dashboard HTML
│   ├── data_api.py           # Devuelve datos filtrados para gráficos
│   └── db.py (opcional)      # Conexión a la base de datos
├── templates/
│   └── dashboard.html        # HTML con filtros y contenedores de gráficos
├── static/
│   └── dashboard.js          # JavaScript con filtros + llamadas a API + Plotly.js
├── .env                      # DATABASE_URL y otras variables
├── requirements.txt
```

---

## 📊 ¿Qué hace este portal?

- Visualiza reportes para cada cliente vía URL: `/dashboard/<client_id>`
- Se conecta a la base PostgreSQL y usa la vista:
  - `<client_id>.vw_dashboard_settlement`
- Renderiza 4 gráficos:
  - Ventas totales por fecha
  - Ventas por SKU
  - Distribución por `amount_description`
  - Tendencia de ventas
- Filtros disponibles:
  - Fecha (`start_date`, `end_date`)
  - SKU
  - amount_description

---

## ⚙️ Cómo ejecutar el portal

1. Cloná el repositorio y activá tu entorno virtual

```bash
cd ecommerce-dashboard
pip install -r requirements.txt
```

2. Configurá el archivo `.env` con tu cadena de conexión PostgreSQL:

```
DATABASE_URL=postgresql://usuario:password@host:puerto/db
```

3. Ejecutá Flask:

```bash
python app.py
```

4. Accedé en el navegador:

```
http://localhost:5000/dashboard/prune
```

(reemplazá `prune` por el nombre del cliente deseado)

---

## 🧱 Requisitos para que funcione

- La base debe tener por cada cliente:
  - `schema_name.prod_settlement_fact`
  - `schema_name.dim_catalog`
  - `public.dim_mapping_table`
  - `schema_name.vw_dashboard_settlement` ✅ (vista usada por el portal)

---

## 🧩 Stored Procedure para crear la vista

```sql
CALL public.create_dashboard_view('cliente_id');
```

---

## 📎 Notas

- Este proyecto solo **visualiza datos ya procesados**. El ETL y la API de carga están en otro proyecto separado (`ecommerce-etl`).
- Podés agregar autenticación, exportación, y métricas adicionales.

---

¡Listo para visualizar resultados! 📊✨
