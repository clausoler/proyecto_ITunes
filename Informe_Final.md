
# 🎵 Informe Final del Proyecto: Seguimiento de Precios y Análisis del Catálogo de iTunes

## 1. 📌 Resumen Ejecutivo

Apple Inc., a través de iTunes Store, gestiona un catálogo musical global sin herramientas analíticas que permitan auditar precios ni estudiar el comportamiento del mercado a lo largo del tiempo. Este proyecto desarrolló un sistema completo de recopilación, limpieza y análisis de datos del catálogo de iTunes EE. UU., centrado en géneros musicales, con el objetivo de detectar patrones clave, justificar precios y apoyar decisiones estratégicas.

Como resultado, se construyó un dashboard interactivo en Power BI que permite visualizar KPIs como el total de canciones y álbumes, así como comparaciones de precio y duración por género musical, evolución histórica de precios y comportamiento de álbumes deluxe.

---

## 2. 🧾 Descripción del Caso de Negocio

iTunes Store carecía de una herramienta que:
- Auditara el comportamiento de precios a lo largo del tiempo.
- Identificara patrones de consumo ligados a variaciones de precios.
- Detectara oportunidades de promociones y ajustes comerciales.

Esto representa una pérdida de oportunidad para optimizar ingresos y mejorar la competitividad del servicio. La propuesta busca construir una base sólida de análisis a partir de precios históricos, metadatos, géneros y estructura de las canciones y álbumes.
 
### 2.1 Objetivos del proyecto

#### 🎯 Objetivo general:
Desarrollar un sistema automatizado de recopilación y análisis de datos que permita almacenar, organizar y estudiar los precios, géneros, metadatos y variaciones temporales del contenido musical disponible en el catálogo estadounidense de iTunes Store, con el fin de construir una base sólida para el análisis histórico de precios y tendencias del mercado musical digital en EE. UU.

#### 📌 Objetivos específicos:
- Diseñar y construir un modelo relacional SQL para almacenar canciones, álbumes, artistas, géneros y precios históricos.
- Automatizar el proceso de extracción de datos desde la API pública de iTunes utilizando Python.
- Generar un historial de cambios de precios con fecha de captura para cada pista.
- Posibilitar análisis estadísticos y visuales sobre tendencias de precios, géneros musicales predominantes, etc.
- Establecer la base para un sistema de alertas futuras sobre descuentos y promociones.
 
### 2.2 Definir el alcance

**Resumen del caso de negocio:**  
Este proyecto propone construir una base de datos estructurada y automatizada que registre diariamente los precios y metadatos musicales extraídos desde la API pública de iTunes. La solución permitirá a Apple generar una vista histórica del comportamiento de precios de su catálogo digital, permitiendo análisis avanzados y toma de decisiones informadas para mejorar su estrategia comercial.

**Impacto esperado:**
- Mejora en la toma de decisiones de pricing por parte del equipo de Apple Music/iTunes.
- Identificación rápida de oportunidades de ajuste de precios.
- Mejora en campañas de marketing basadas en datos reales.
- Reducción de pérdidas asociadas a precios inadecuados o promociones no optimizadas.
- Potencial integración futura con plataformas de business intelligence internas.

**Tecnologías complementarias:**
- Base de datos SQL (PostgreSQL para producción).
- Python (con `requests`, `pandas`, `numpy` , `psycopg2`) para scraping, limpieza y carga.
- Dashboard  en Power BI.

---

## 3. 🔄 Pipeline ETL

### 🔸 Extracción

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

### 🔸 Transformación
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

### 🔸 Carga
Los datos se almacenaron tanto en archivos `.pkl` como en una base de datos relacional PostgreSQL, lista para análisis exploratorios y visualización en Power BI.

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

El proyecto ha sido diseñado para ser modular, reproducible y mantenible. El pipeline se ejecuta desde un script principal `main_ETL.py` que orqueste todo el flujo desde `src/`.

---

## 4. 🔍 Análisis de los Datos (EDA)

Los hallazgos clave fueron:

- **Precios:** Mayoría de canciones entre 0.99 y 1.29 USD. Álbumes con valores atípicos por colecciones deluxe.
- **Duración:** Canciones fuera del estándar (>10 min) ligadas a géneros como clásica o jazz.
- **Correlaciones:** Relación moderada entre número de discos y precio del álbum.
- **Explícito vs. no explícito:** Las canciones no explícitas tienden a ser más largas y caras.
- **Evolución temporal:** Los precios se mantienen estables, lo cual permite detectar con facilidad futuras promociones.
- **Distribución por género:** Hip-Hop/Rap y Pop dominan el catálogo; géneros instrumentales tienden a tener canciones más largas pero no más caras.


---

## 5. 📈 Impacto de Negocio y Recomendaciones

### 🎯 Valor generado:
- Primer dashboard que permite analizar el catálogo musical de iTunes desde una perspectiva de datos históricos y de género musical.
- Visualización clara del posicionamiento de cada género según duración, precio y número de artistas.
- Capacidad de auditoría visual y alerta ante cambios atípicos o promociones.

### ✅ Recomendaciones:
1. **Campañas por género premium:** Explotar géneros como clásica o jazz en bundles o contenido exclusivo.
2. **Optimización de promociones:** Detectar géneros con baja representación pero alto precio medio para campañas personalizadas.
3. **Identificación de artistas premium:** Usar el ranking de precio medio por artista para destacar colecciones valiosas.
4. **Monitoreo periódico:** Continuar capturando datos a lo largo del tiempo para habilitar alertas y predicciones de comportamiento.
5. **Ampliación internacional:** Repetir el análisis para otros países clave y comparar dinámicas de catálogo.

---

## 6. 📌 Conclusiones y Próximos Pasos

Este proyecto demuestra que, con una arquitectura ligera pero eficiente, es posible transformar datos públicos de una API como la de iTunes en conocimiento estratégico. El enfoque por género musical permite una segmentación clara del catálogo y genera valor para decisiones de pricing, marketing y curaduría editorial.

### Próximos pasos:
- Automatizar el pipeline ETL de forma que se extraigan datos diarios y se alimente la base de datos.
- Ampliar el historial temporal.
- Crear modelos predictivos de precio y comportamiento.
- Expandir el análisis a otros mercados regionales.
