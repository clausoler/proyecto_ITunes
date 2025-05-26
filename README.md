
## 📌 Descripción del proyecto

Este proyecto tiene como objetivo analizar el catálogo de iTunes Store USA, identificando patrones en precios, duración de canciones, explicitud y otras características clave. Se realiza un proceso de extracción automática de datos desde la API de iTunes, su almacenamiento en una base de datos PostgreSQL y visualización mediante Power BI.

El proyecto permite realizar análisis históricos y estructurales sobre el catálogo, y está preparado para alimentar sistemas de alertas o recomendaciones futuras.

---

## 🔧 Cómo reproducir este proyecto

### 📁 Estructura general del proyecto

```
Proyecto-iTunes/
│
├── output/                   # Resultados generados (si aplica)

├── notebooks/                # Notebooks exploratorios opcionales

├── src/                      # Código fuente adicional (helpers, utilidades, etc.)

├── documentacion/
    ├── Esquema_Dashboard_iTunes  # Plantillas dashboard power bi
│   └── itunes_database.sql   # Script con el esquema de la base de datos PostgreSQL
    └── descripcion_columnas_itunes.md   # Descripción columnas de los datos
    └──ITunes_logo.svg       # Logo de la plataforma ITunes
    └──Script-22             # Scripts pruebas base de datos sql
     
├── Entregables/             # Entregables del proyecto
│   └── 1ºEntregable.md
    └── 2ºEntregable.md
    └── 3ºEntregable.md
    └── 4ºEntregable.md
     
├── main_ETL.py               # Script principal para la extracción y carga de datos
 
├── main_EDA.py               # Script principal de análisis exploratorio

├── requirements.txt          # Dependencias del entorno virtual

├── README.md                 # Instrucciones para reproducir el proyecto

├── dashboard_ITunes.pbix     # Dashboard interactivo
 
├── Informe_Final.md          # Informe final del proyecto

├── .gitignore                # Archivos no subidos a github
```

---

### 🐍 1. Configuración del entorno

Se recomienda crear un entorno virtual para aislar las dependencias del proyecto:

```bash
python -m venv venv
source venv/bin/activate      # En Linux/macOS
venv\Scripts\activate.bat     # En Windows
pip install -r requirements.txt
```

---

### 🗄️ 2. Crear la base de datos PostgreSQL

1. Asegúrate de tener PostgreSQL instalado y corriendo.
2. Crea una nueva base de datos, por ejemplo:

```sql
CREATE DATABASE itunes_store;
```

3. Ejecuta el script SQL proporcionado para crear las tablas necesarias:

```bash
psql -U tu_usuario -d itunes_store -f documentacion/itunes_database.sql
```

> 🔐 Si el proyecto utiliza credenciales/API keys, deberás configurarlas manualmente dentro del código o usar variables de entorno.

---

### 🧬 3. Ejecutar el proceso ETL

El script principal que extrae datos desde la API de iTunes y los carga en PostgreSQL es:

```bash
python main_ETL.py
```

> Este script realiza la recopilación, transformación y carga de datos en la base de datos que luego será usada por Power BI.

---

### 📊 4. Ejecutar el análisis exploratorio (EDA)

Una vez cargados los datos, puedes generar insights exploratorios con:

```bash
python main_EDA.py
```

---

### 📈 5. Visualización con Power BI

1. Abre el archivo `dashboard_ITunes.pbix`.
2. Power BI se conectará directamente a tu instancia local de PostgreSQL.
3. Si es necesario, actualiza las credenciales o el nombre de servidor/base de datos en las **fuentes de datos**.

---

### ✅ Requisitos del sistema

- Python 3.8+
- PostgreSQL (local o en servidor)
- Power BI Desktop