import pandas as pd
import psycopg2
from typing import List, Dict


def conectar_postgres(dbname: str, user: str, password: str, host: str = "localhost", port: str = "5432"):
    """
    Crea una conexión a la base de datos PostgreSQL.

    Args:
        dbname (str): Nombre de la base de datos.
        user (str): Usuario de PostgreSQL.
        password (str): Contraseña.
        host (str): Dirección del servidor. Por defecto, localhost.
        port (str): Puerto de conexión. Por defecto, 5432.

    Returns:
        psycopg2.connection: Objeto de conexión a la base de datos.
    """
    return psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )


def insertar_dataframe(df: pd.DataFrame, tabla_sql: str, columnas: List[str], conn) -> None:
    """
    Inserta un DataFrame en una tabla PostgreSQL utilizando executemany.
    Si hay conflicto de clave primaria, se ignora el registro duplicado.

    Args:
        df (pd.DataFrame): El DataFrame que contiene los datos.
        tabla_sql (str): Nombre de la tabla en la base de datos.
        columnas (List[str]): Lista de columnas que se insertarán.
        conn (psycopg2.connection): Conexión activa a la base de datos.
    """
    import pandas as pd  # Asegúrate de tener esto arriba si no está
    cursor = conn.cursor()

    # Sanitizar valores: convertir pd.NA y np.nan a None
    data_to_insert = df[columnas].where(pd.notna(df[columnas]), None).values.tolist()

    # Construir plantilla base
    placeholders = ", ".join(["%s"] * len(columnas))
    columnas_str = ", ".join(columnas)

    # === Manejo de conflictos según la tabla ===
    if tabla_sql in ["artist", "album", "track", "genre"]:
        # Clave primaria única → evitar error duplicado
        pk_col = columnas[0]  # Asumimos que la primera columna es la PK
        insert_query = f"""
            INSERT INTO {tabla_sql} ({columnas_str})
            VALUES ({placeholders})
            ON CONFLICT ({pk_col}) DO NOTHING
        """
    else:
        # Para tablas sin clave única definida (como track_prices)
        insert_query = f"""
            INSERT INTO {tabla_sql} ({columnas_str})
            VALUES ({placeholders})
        """

    # Ejecutar inserción
    cursor.executemany(insert_query, data_to_insert)
    conn.commit()
    cursor.close()



def insertar_multiples_tablas(tablas: Dict[str, pd.DataFrame], esquema_columnas: Dict[str, List[str]], conn) -> None:
    """
    Inserta múltiples DataFrames en sus respectivas tablas PostgreSQL.

    Args:
        tablas (dict): Diccionario con nombre_tabla -> DataFrame.
        esquema_columnas (dict): Diccionario con nombre_tabla -> lista de columnas.
        conn (psycopg2.connection): Conexión activa a la base de datos.
    """
    for nombre_tabla, df in tablas.items():
        columnas = esquema_columnas.get(nombre_tabla)
        if columnas is None:
            raise ValueError(f"Faltan columnas para la tabla '{nombre_tabla}'")
        print(f"Insertando datos en tabla '{nombre_tabla}'...")
        insertar_dataframe(df, nombre_tabla, columnas, conn)
    print("[COMPLETADO] Todas las tablas fueron insertadas correctamente.")
 
