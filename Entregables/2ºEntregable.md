
# 2. ETL y Preprocesamiento

## 🟠 Extracción

La fuente principal de datos del proyecto es la **API pública de iTunes**, la cual permite acceder a información detallada sobre canciones, álbumes y artistas. Sin embargo, esta API **no dispone de un endpoint que devuelva listados completos** de canciones o álbumes, por lo que se ha tenido que diseñar una estrategia alternativa para maximizar la cantidad de datos extraídos.

Para realizar la extracción:

- Se ha implementado una técnica de **combinaciones de términos**: se generan combinaciones de dos letras del alfabeto (de `aa` a `zz`) para usarlas como términos de búsqueda.
- Cada día se consultan **97 términos distintos**, lo que permite descargar hasta **19.400 canciones por día**, dada la limitación de 200 resultados por término impuesta por la API.
- Este proceso se ha ejecutado durante **7 días consecutivos**, para ampliar la cobertura de datos.

El acceso a la API se realiza mediante un archivo `.env` que contiene la URL de la API, la cual se carga dinámicamente en el código mediante `os.getenv()`, asegurando que las credenciales y configuraciones se mantengan seguras y fuera del código fuente.

Los datos extraídos incluyen, entre otros:

- Título de la canción
- Nombre del álbum
- Género musical
- Duración (en milisegundos)
- Precio de la canción
- Precio del álbum
- Fecha de publicación

---

## 🟡 Transformación

Una vez extraídos los datos desde la API de iTunes, se lleva a cabo un proceso de limpieza y transformación exhaustivo para garantizar su calidad y consistencia antes de ser cargados a la base de datos.

### 🧹 Limpieza de datos

Se han aplicado múltiples técnicas de depuración y estandarización:

- Se utiliza la librería **`unicodedata`** para limpiar todas las columnas de tipo texto (`object`) del `DataFrame`. Esta limpieza incluye:
  - Eliminación de tildes y conversión de caracteres Unicode a ASCII.
  - Supresión de espacios extra y caracteres especiales mediante expresiones regulares.
  - Eliminación de filas en las que todas las columnas de texto quedaron vacías tras el proceso.
- Las columnas de tipo **fecha** son procesadas para separar las partes de hora, minuto y segundo, convirtiéndolas luego al formato `datetime64[ns]`.
- Se realiza conversión de tipos:
  - De `float` a `int` para identificadores o cantidades.
  - De `str` a `bool` para columnas que representan valores lógicos.
- En cuanto a valores nulos:
  - Se eliminan registros con nulos en columnas que contienen identificadores únicos.
  - En columnas de texto, los nulos se reemplazan por `"Sin identificar"`.
  - En columnas de precios, los valores negativos se consideran erróneos, se reemplazan por `NaN` y luego se imputan usando la **media real** de los precios válidos.
- Para evitar duplicados:
  - Se carga un `DataFrame` maestro desde un archivo `.pkl`.
  - Se divide y normaliza la información en varias tablas: `Artist`, `Album`, `Track`, `Genre`, `Track_prices`, `Album_prices`.
  - Se garantiza la unicidad de claves primarias y se eliminan duplicados históricos (por ID + fecha).

### 🔧 Transformaciones aplicadas

- Se estandarizan los nombres de columnas para que coincidan exactamente con los nombres utilizados en la base de datos SQL destino.
- No se han realizado agregaciones estadísticas, ya que cada fila contiene información única y no repetida.

### 🧰 Librerías utilizadas

Además de **`pandas`**, se han utilizado las siguientes herramientas y librerías:

- `numpy`
- `re`
- `unicodedata`
- `glob`
- `matplotlib.pyplot`
- `seaborn`

---

## 🟢 Carga

Una vez transformados y depurados, los datos se cargan en dos formatos distintos:

1. **Archivos locales:**  
   Se guardan como archivos `.pkl` individuales, uno por cada tabla del modelo de datos. Esto permite un acceso rápido para análisis exploratorios o pruebas sin necesidad de consultar la base de datos. Están omitidos en el archivo .gitignore porque exceden el límite de GB en GitHub. 

2. **Base de datos relacional PostgreSQL:**  
   Los datos limpios se cargan también en una base de datos PostgreSQL, estructurada en un esquema relacional que facilita su consulta y análisis posterior.

### 🗃️ Estructura de la base de datos

Los datos están organizados en múltiples tablas normalizadas que siguen una arquitectura de base de datos clásica. Entre ellas:

- `artist`
- `album`
- `track`
- `genre`
- `track_prices`
- `album_prices`

Cada tabla contiene claves primarias y, en algunos casos, claves foráneas que establecen relaciones entre entidades (por ejemplo, entre `track` y `album`, o entre `album` y `artist`).

### 🔌 Carga con `psycopg2`

Para cargar los datos en PostgreSQL se ha utilizado la librería `psycopg2`, que permite ejecutar sentencias SQL directamente desde Python. La conexión se configura de forma segura a través de variables de entorno, evitando exponer credenciales en el código.

Este proceso incluye:

- Inserciones seguras con control de duplicados.
- Validación de integridad referencial mediante claves foráneas.
- Conversión automática de tipos (`datetime`, `int`, `float`, `str`) en la inserción.

---

## 🔵 Documentación técnica y reproducibilidad

El proyecto ha sido diseñado para ser modular, reproducible y mantenible. Aunque actualmente el pipeline se ejecuta desde un conjunto de notebooks, está planificado migrar su ejecución hacia un script principal `main.py` que orqueste todo el flujo desde `src/`.

### 🗂️ Estructura del proyecto

El proyecto sigue una organización clara de carpetas:

```
project-root/
├── data/
│   ├── data_raw/       # Datos originales extraídos desde la API
│   └── data_clean/     # Datos transformados y listos para el análisis
├── notebooks/          # Notebooks para exploración y pruebas (extracción, limpieza, carga)
├── src/                # Scripts Python con funciones modulares
│   ├── extraccion.py
│   ├── limpieza.py
│   └── carga.py
├── .env                # Variables de entorno (API URL, credenciales)
└── entregables/        # Archivos para entrega del proyecto final
```

### 🔐 Reproducibilidad

Para garantizar la reproducibilidad del pipeline:

- Se utiliza un archivo `.env` para manejar variables sensibles (como la URL de la API o parámetros de conexión a la base de datos).
- Las funciones están modularizadas y separadas por archivo en la carpeta `src/`, lo que facilita su reutilización.
- Se registra el avance del scraping mediante un archivo de log de términos ya utilizados (`terminos_usados.txt`), evitando redundancias.
- Está previsto incluir un `requirements.txt` con todas las dependencias del entorno, asegurando que el entorno pueda recrearse fácilmente en otras máquinas o entornos virtuales.

### ⏱️ Tiempo de ejecución

Cada notebook (o script equivalente) tarda menos de **1 minuto** en ejecutarse, gracias a una lógica optimizada y uso de estructuras eficientes como `DataFrames`, acceso por lotes, y tratamiento vectorizado.
