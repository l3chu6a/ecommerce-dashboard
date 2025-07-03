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
