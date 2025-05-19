import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
 
pd.set_option('display.max_columns', None)
 
def cargar_datos_itunes(directorio="data/data_raw", patron="itunes_*.csv"):
    """
    Carga y concatena archivos CSV de iTunes desde un directorio dado que cumplan con un patrón.

    Parámetros:
    - directorio (str): Ruta relativa al directorio donde se encuentran los archivos CSV.
    - patron (str): Patrón de búsqueda de archivos CSV.

    Retorna:
    - DataFrame concatenado con todos los registros encontrados.
    """
    # Calcula la ruta base absoluta (3 niveles desde src/ETL/)
    base_path = Path(__file__).resolve().parents[2]  # sube desde src/ETL/ hasta raíz del proyecto
    ruta = base_path / directorio

    archivos_csv = sorted(ruta.glob(patron))
    if not archivos_csv:
        print(f"[ADVERTENCIA] No se encontraron archivos en: {ruta} con patrón: {patron}")
        return pd.DataFrame()

    df = pd.concat([pd.read_csv(f) for f in archivos_csv], ignore_index=True)
    print(f"Total de registros cargados: {df.shape[0]}")
    return df
 
def guardar_df(df: pd.DataFrame, ruta: str = "../data/data_limpio/itunes.pkl") -> None:
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    df.to_pickle(ruta)
     
def guardar_tablas_en_pickle(tablas: dict, carpeta_salida: str) -> None:
    """
    Guarda cada DataFrame de un diccionario como archivo .pkl en una carpeta.
    
    Args:
        tablas (dict): Diccionario {nombre: DataFrame}.
        carpeta_salida (str): Ruta a la carpeta donde se guardarán los .pkl.
    """
    os.makedirs(carpeta_salida, exist_ok=True)

    for nombre, df in tablas.items():
        ruta = os.path.join(carpeta_salida, f"{nombre.lower()}.pkl")
        df.to_pickle(ruta)