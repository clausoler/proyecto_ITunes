# main_ETL.py
print("[OK] Comenzando proceso ETL...")

import os
import pandas as pd
from dotenv import load_dotenv

from src.ETL.file_utils import (
    cargar_datos_itunes,
    guardar_df,
    guardar_tablas_en_pickle
)
from src.ETL.transform import (
    limpieza_total_texto_final,
    limpiar_fechas_split,
    convertir_columnas_a_entero,
    convertir_a_booleano,
    eliminar_filas_nulas,
    rellenar_nulos_texto,
    limpiar_columnas_precio,
    asignar_id_incremental,
    procesar_dataframe_maestro
)
from src.ETL.load import conectar_postgres, insertar_dataframe

# 1. Cargar configuración
print("[INFO] Cargando configuración de entorno (.env)...")
load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
print("[INFO] Configuración cargada correctamente.")

# 2. Cargar todos los CSV acumulados
print("\n[OK] Cargando archivos CSV acumulados...")
df = cargar_datos_itunes()
print(f"Total de registros cargados: {df.shape[0]}")

# 3. Limpieza de datos
print("\n[OK] Limpiando datos brutos...")
df = limpieza_total_texto_final(df)
df = limpiar_fechas_split(df)
df = convertir_columnas_a_entero(df, [
    "collectionId", "collectionArtistId", "trackTimeMillis", "discCount",
    "discNumber", "trackCount", "trackNumber"
])
df = convertir_a_booleano(df, "isStreamable")
df = eliminar_filas_nulas(df, ["collectionId", "releaseDate", "trackTimeMillis", "isStreamable"])
df = rellenar_nulos_texto(df, [
    "artistName", "collectionName", "trackName", "collectionCensoredName", "trackCensoredName",
    "artistViewUrl", "collectionViewUrl", "trackViewUrl", "previewUrl",
    "collectionArtistName", "collectionArtistViewUrl", "contentAdvisoryRating"
])
df = limpiar_columnas_precio(df)
df = asignar_id_incremental(df, "collectionArtistId")

# 4. Guardar DataFrame limpio
print("\n[OK] Guardando DataFrame limpio...")
guardar_df(df, "../data/data_limpio/itunes_limpio.pkl")

# 5. Normalizar a tablas
print("\n[OK] Normalizando tablas...")
tablas = procesar_dataframe_maestro("../data/data_limpio/itunes_limpio.pkl")

# 6. Guardar tablas individualmente
print("\n[OK] Guardando tablas por separado...")
guardar_tablas_en_pickle(tablas, "../data/data_limpio")

# 7. Ver resumen de registros antes de insertar
print("\n[INFO] Registros por tabla antes de insertar:")
for tabla, df_tabla in tablas.items():
    print(f"  - {tabla}: {len(df_tabla)} registros")

# 8. Conexión a la base de datos
print("\n[OK] Cargando tablas en PostgreSQL...")
conn = conectar_postgres(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

# 8.1 Verificar restricción UNIQUE en genre
with conn.cursor() as cur:
    cur.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint WHERE conname = 'unique_genrename'
            ) THEN
                ALTER TABLE genre ADD CONSTRAINT unique_genrename UNIQUE (primarygenrename);
            END IF;
        END$$;
    """)
    conn.commit()
print("[INFO] Restricción UNIQUE en genre.primarygenrename verificada.")

# 8.2 Insertar géneros (sin genre_id, lo autogenera la base)
insertar_dataframe(tablas["genre"], "genre", ["primarygenrename"], conn)

# 8.3 Leer genre_id reales desde la base
df_genres_db = pd.read_sql("SELECT genre_id, primarygenrename FROM genre", conn)

# 8.4 Merge con tabla track para asignar genre_id
tablas["track"] = tablas["track"].merge(df_genres_db, how="left", on="primarygenrename")

# 8.5 Validar que no haya tracks sin genre_id
faltantes = tablas["track"]["genre_id"].isna().sum()
if faltantes > 0:
    print(f"[ERROR] {faltantes} filas en 'track' no pudieron mapear un genre_id desde la base de datos.")
    raise ValueError("❌ Abortando carga de 'track' por fallo en mapeo de género.")

# 8.6 Definir columnas para cada tabla
esquema_columnas = {
    "artist": ["artist_id", "artistname", "artistviewurl"],
    "album": ["collection_id", "collectionname", "collectioncensoredname", "release_date",
              "collectionexplicitness", "contentadvisoryrating", "collectionprice", "currency",
              "trackcount", "disccount", "collectionviewurl",
              "collectionartistname", "collectionartistviewurl", "artist_id"],
    "track": ["track_id", "trackname", "tracknumber", "trackprice", "discnumber", "tracktimemillis",
              "trackexplicitness", "release_date", "trackviewurl", "is_streamable", "kind",
              "artist_id", "collection_id", "genre_id"],
    "album_prices": ["collection_id", "collectionprice", "checked_at"],
    "track_prices": ["track_id", "trackprice", "checked_at"]
}

# 8.7 Cargar en orden
orden_insercion = ["artist", "album", "track", "album_prices", "track_prices"]
for nombre_tabla in orden_insercion:
    print(f"Insertando datos en tabla '{nombre_tabla}'...")
    insertar_dataframe(tablas[nombre_tabla], nombre_tabla, esquema_columnas[nombre_tabla], conn)

conn.close()
print("\n[OK] Proceso ETL completado con éxito.")






 
