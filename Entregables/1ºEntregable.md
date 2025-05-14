# 📊 Propuesta de Proyecto — Seguimiento de Precios y Análisis de Metadatos en iTunes

## 1. Definición del Proyecto y Adquisición de Datos

### 1.1 Entender el problema

**Contexto de la empresa:**  
Apple Inc., a través de su plataforma iTunes Store, distribuye millones de canciones y álbumes digitales en más de 100 países. Esta plataforma permite a los usuarios comprar y descargar canciones, álbumes y contenido multimedia. Aunque Apple gestiona precios y disponibilidad de forma global, no existe una herramienta pública ni interna bien documentada que permita realizar un seguimiento histórico de los precios o analizar tendencias y comportamientos del catálogo a lo largo del tiempo.

**Problema del negocio:**  
El modelo actual de Apple para iTunes no cuenta con una herramienta analítica que le permita:
- Auditar el comportamiento de los precios a lo largo del tiempo.
- Detectar patrones de consumo en función de las variaciones de precios.
- Identificar oportunidades de promoción, campañas de marketing o ajustes automáticos de precios basados en datos históricos.

Esta carencia representa una oportunidad perdida para optimizar ingresos, responder a la competencia, y entender mejor el comportamiento del mercado.

---

### 1.2 Objetivos del proyecto

#### 🎯 Objetivo general:
Desarrollar un sistema automatizado de recopilación y análisis de datos que permita almacenar, organizar y estudiar los precios, géneros, metadatos y variaciones temporales del contenido musical disponible en el catálogo estadounidense de iTunes Store, con el fin de construir una base sólida para el análisis histórico de precios y tendencias del mercado musical digital en EE. UU.

#### 📌 Objetivos específicos:
- Diseñar y construir un modelo relacional SQL para almacenar canciones, álbumes, artistas, géneros y precios históricos.
- Automatizar el proceso de extracción de datos desde la API pública de iTunes utilizando Python.
- Generar un historial de cambios de precios con fecha de captura para cada pista.
- Posibilitar análisis estadísticos y visuales sobre tendencias de precios, géneros musicales predominantes, etc.
- Establecer la base para un sistema de alertas futuras sobre descuentos y promociones.

---

### 1.3 Definir el alcance

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

### 1.4 Identificar fuentes de datos

**Fuente principal:**
- [iTunes Search API (pública y gratuita)](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html)
  - Permite buscar canciones, álbumes, artistas, colecciones y más.
  - Devuelve información como: título, artista, precio, moneda, duración, género, URLs, previews, y fecha de publicación.

**Volumen y formato:**
- Se espera obtener hasta 135.000 canciones únicas en una sola semana, utilizando combinaciones de dos letras como términos de búsqueda ("aa" a "zz"), con una capacidad de extracción diaria de hasta 19.000 registros.

- Cada canción incluye todos los metadatos disponibles proporcionados por la API de iTunes, como título, artista, colección, género, precios, URLs, fecha de lanzamiento, entre otros.

- Los datos se extraen únicamente del catálogo estadounidense (country="US"), por lo que los análisis de precios y tendencias estarán limitados al mercado de Estados Unidos.

- Los datos se almacenan en archivos .csv diarios, organizados cronológicamente, con una columna checked_at que permite llevar un seguimiento histórico de los precios y cambios en los metadatos.

- Esta estructura permitirá construir una base de datos relacional posteriormente, orientada a análisis de evolución de precios, estrategias de mercado musical, y visualizaciones dinámicas.

