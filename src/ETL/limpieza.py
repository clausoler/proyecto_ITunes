import re
import unicodedata

def limpieza_total_texto_final(df):
    """
    Limpia exhaustivamente todas las columnas de tipo texto (object) en un DataFrame para depurar datos contaminados
    provenientes de fuentes como APIs. Esta limpieza está especialmente diseñada para contenido musical (iTunes, etc.).

    ✔️ Operaciones que realiza:
    ---------------------------
    - Elimina cadenas con errores comunes como:
        '#¿NOMBRE?', '#¡VALOR!', '¿?', etc. que podrían provenir de errores de importación o codificación.
    - Detecta y elimina:
        • Números puros (como '123', '3235', '111.0') aunque estén en formato string (object)
        • Números rodeados de puntos o espacios (ej: '... 3235 ...')
        • Fechas mal formateadas del tipo '09-may', '10-abr', etc.
        • Entradas vacías, signos aislados o cadenas con solo símbolos (ej: '?', '!', '---')
    - Aplica normalización Unicode:
        Elimina acentos y convierte caracteres a ASCII usando `unicodedata`.
    - Limpia espacios extra y caracteres no deseados con expresiones regulares.
    - Elimina filas donde todas las columnas de texto hayan quedado vacías tras la limpieza.

    ❗ NOTA:
    -------
    - Esta función **no convierte a minúsculas**: respeta las mayúsculas originales.
    - Todos los filtros se aplican aún si los datos están en formato `object` (string no tipado).

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame que contiene columnas de texto potencialmente contaminadas.

    Retorna:
    --------
    pandas.DataFrame
        Un DataFrame limpio, con columnas texto depuradas y sin filas inútiles.
    """

    def limpiar_valor(val):
        if pd.isna(val):
            return ""

        val = str(val).strip()

        if any(pat in val.lower() for pat in ["¿", "¡", "nombre", "valor"]):
            return ""

        if re.fullmatch(r"\.*\s*\d+(\.\d+)?\s*\.*", val):
            return ""

        if re.fullmatch(r"\d{1,2}-[a-zA-Z]{3}", val):
            return ""

        if re.fullmatch(r"[^\w]*", val):
            return ""

        val = unicodedata.normalize("NFKD", val).encode("ascii", "ignore").decode("utf-8")
        val = re.sub(r"[^\w\s.,'&!?-]", "", val)
        val = re.sub(r"\s+", " ", val).strip()

        if len(val) < 2:
            return ""

        return val

    columnas_objetivas = df.select_dtypes(include=["object"]).columns
    for col in columnas_objetivas:
        df[col] = df[col].apply(limpiar_valor)

    mask = df[columnas_objetivas].apply(lambda row: all(val == "" for val in row), axis=1)
    df = df[~mask]

    return df
 
def limpiar_fechas_split(df):
    """
    Elimina la parte de hora, minutos y segundos de las columnas 'checked_at' y 'releaseDate'
    usando string split y reconvierte a datetime64[ns].

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame que contiene las columnas de fechas.

    Retorna:
    --------
    pandas.DataFrame
        DataFrame con 'checked_at' y 'releaseDate' en formato datetime64[ns], sin horas.
    """
    df["checked_at"] = pd.to_datetime(df["checked_at"].astype(str).str.split("T").str[0], errors="coerce")
    df["releaseDate"] = pd.to_datetime(df["releaseDate"].astype(str).str.split("T").str[0], errors="coerce")
    return df
 
def convertir_columnas_a_entero(df, columnas):
    """
    Convierte columnas numéricas a tipo entero truncando los decimales,
    sin modificar la secuencia de IDs original ni generar nuevos valores.

    Operaciones:
    - Reemplaza comas por puntos (si hay errores de separación decimal)
    - Convierte a numérico (coerción si hay errores)
    - Elimina parte decimal truncando (sin redondeo)
    - Convierte a tipo Int64 para mantener nulos

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame original.

    columnas : list[str]
        Columnas que deben convertirse a enteros sin parte decimal.

    Retorna:
    --------
    pandas.DataFrame
        El DataFrame con las columnas convertidas a enteros reales.
    """
    for col in columnas:
        df[col] = df[col].astype(str).str.replace(",", ".", regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].apply(lambda x: int(x) if pd.notna(x) else pd.NA)
        df[col] = df[col].astype("Int64")
    return df
 
def convertir_a_booleano(df, columna):
    """
    Convierte una columna del DataFrame a tipo booleano (`True`, `False`, `<NA>`),
    manejando cadenas en mayúsculas/minúsculas y permitiendo valores nulos.

    Esta función también reemplaza valores vacíos o mal formateados como:
    "", " ", "nan", "NaN" por `pd.NA` antes de la conversión.

    Parámetros:
    -----------
    df : pandas.DataFrame
        El DataFrame a procesar.

    columna : str
        Nombre de la columna que se desea convertir a tipo booleano.

    Retorna:
    --------
    pandas.DataFrame
        El DataFrame con la columna convertida a tipo booleano y valores no válidos tratados como nulos.
    """
    # Reemplazar valores no informativos por pd.NA (vacíos o mal escritos)
    df.replace(["", " ", "nan", "NaN"], pd.NA, inplace=True)

    # Convertir columna a booleano interpretando correctamente "true"/"false"
    df.loc[:, columna] = df[columna].map(
        lambda x: True if str(x).strip().lower() == "true"
        else False if str(x).strip().lower() == "false"
        else pd.NA
    )

    # Forzar tipo boolean con soporte para nulos
    df[columna] = df[columna].astype("boolean")
    return df
 
def reporte_nulos(df):
    """
    Genera un reporte sobre los valores nulos de un DataFrame.

    Esta función analiza el DataFrame proporcionado y devuelve un nuevo DataFrame 
    con información detallada sobre la cantidad de valores nulos, el porcentaje 
    de valores nulos respecto al total de filas y el tipo de dato de cada columna.

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame que se desea analizar en busca de valores nulos.

    Retorna:
    --------
    pd.DataFrame
        Un DataFrame con las siguientes columnas:
        - "número_nulos": número de valores nulos en cada columna.
        - "porcentaje_nulos": porcentaje de valores nulos respecto al total de filas.
        - "tipo_variables": tipo de dato (dtype) de cada columna.

    """
    df_reporte = pd.DataFrame()
    df_reporte["número_nulos"] = df.isnull().sum()
    df_reporte["porcentaje_nulos"] = round((df.isnull().sum() / len(df)) * 100, 2)
    df_reporte["tipo_variables"] = df.dtypes
    return df_reporte
 
def eliminar_filas_nulas(df, columnas_obligatorias):
    """
    Elimina filas del DataFrame que tengan valores nulos en columnas clave.

    Parámetros:
    -----------
    df : pandas.DataFrame
        El DataFrame a procesar.

    columnas_obligatorias : list[str]
        Lista de columnas en las que no se permiten valores nulos.

    Retorna:
    --------
    pandas.DataFrame
        El DataFrame sin las filas que tenían nulos en las columnas especificadas.
    """
    return df.dropna(subset=columnas_obligatorias)
 
def rellenar_nulos_texto(df, columnas):
    """
    Rellena valores nulos en columnas de tipo texto (object) con 'Sin identificar'.

    Esta función asegura que:
    - Las columnas estén en tipo object (string)
    - Los valores nulos sean reemplazados de forma segura
    - Se evita el SettingWithCopyWarning usando `.loc`

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame a procesar.

    columnas : list[str]
        Columnas donde reemplazar valores nulos.

    Retorna:
    --------
    pandas.DataFrame
        El DataFrame con las columnas actualizadas.
    """
    for col in columnas:
        df.loc[:, col] = df[col].astype("object").fillna("Sin identificar")
    return df
 
def limpiar_columnas_precio(df):
    """
    Limpia y normaliza las columnas 'trackPrice' y 'collectionPrice':
    - Convierte a numérico
    - Reemplaza -1 y strings nulos por NaN
    - Imputa TODOS los NaN con la media real
    - Redondea a 2 decimales
    - Imprime estadísticas descriptivas finales

    Parámetros:
    -----------
    df : pandas.DataFrame
        El DataFrame original.

    Retorna:
    --------
    pandas.DataFrame
        DataFrame limpio con columnas de precio sin nulos.
    """
    columnas_precio = ["trackPrice", "collectionPrice"]

    for col in columnas_precio:
        df.loc[:, col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[:, col] = df[col].replace([-1, "", " ", "nan", "NaN"], np.nan)
        media = df[col].dropna().mean()
        df.loc[:, col] = df[col].fillna(media).round(2)

    print("\n📊 Estadísticas descriptivas de precios:")
    print(df[columnas_precio].describe())

    return df
 
def asignar_id_incremental(df, columna, inicio=1):
    """
    Reemplaza completamente una columna con un ID incremental único.

    Esto es útil cuando se requiere generar una clave primaria válida para SQL,
    incluso si la columna original contenía nulos o valores inconsistentes.

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame original (o una copia del original).

    columna : str
        Nombre de la columna a sobrescribir con IDs únicos.

    inicio : int (default=1)
        Valor inicial del ID incremental.

    Retorna:
    --------
    pandas.DataFrame
        El DataFrame con la columna reemplazada por IDs únicos de tipo Int64.
    """
    df.loc[:, columna] = pd.Series(range(inicio, inicio + len(df)), index=df.index, dtype="Int64")
    return df
 
def procesar_dataframe_maestro(ruta_pickle):
    """
    Carga un DataFrame maestro desde un archivo pickle, lo limpia y separa en tablas normalizadas:
    Artist, Album, Track, Genre, Track_prices, Album_prices.
    Garantiza que no haya duplicados por ID en tablas principales y limpia registros duplicados
    por ID + fecha en las tablas históricas.

    Parámetros:
    -----------
    ruta_pickle : str
        Ruta del archivo pickle con el DataFrame completo.

    Retorna:
    --------
    dict
        Diccionario con las tablas limpias separadas por nombre.
    """
    # Renombrar columnas para que coincidan con el esquema SQL
    df = pd.read_pickle(ruta_pickle)
    df = df.rename(columns={
        "artistId": "artist_id",
        "artistName": "artistname",
        "artistViewUrl": "artistviewurl",
        "collectionId": "collection_id",
        "collectionName": "collectionname",
        "collectionCensoredName": "collectioncensoredname",
        "releaseDate": "release_date",
        "collectionExplicitness": "collectionexplicitness",
        "contentAdvisoryRating": "contentadvisoryrating",
        "collectionPrice": "collectionprice",
        "currency": "currency",
        "trackCount": "trackcount",
        "discCount": "disccount",
        "collectionViewUrl": "collectionviewurl",
        "collectionArtistId": "collectionartist_id",
        "collectionArtistName": "collectionartistname",
        "collectionArtistViewUrl": "collectionartistviewurl",
        "trackId": "track_id",
        "trackName": "trackname",
        "trackNumber": "tracknumber",
        "trackPrice": "trackprice",
        "discNumber": "discnumber",
        "trackTimeMillis": "tracktimemillis",
        "trackExplicitness": "trackexplicitness",
        "trackViewUrl": "trackviewurl",
        "isStreamable": "is_streamable",
        "kind": "kind",
        "primaryGenreName": "primarygenrename"
    })

    # Tablas principales
    artist_df = (
        df.groupby("artist_id")[["artistname", "artistviewurl"]]
        .agg(lambda x: x.dropna().value_counts().idxmax() if not x.dropna().empty else pd.NA)
        .reset_index()
    )

    album_cols = [
        "collection_id", "collectionname", "collectioncensoredname", "release_date",
        "collectionexplicitness", "contentadvisoryrating", "collectionprice", "currency",
        "trackcount", "disccount", "collectionviewurl", "collectionartist_id",
        "collectionartistname", "collectionartistviewurl", "artist_id"
    ]
    album_df = df[album_cols].drop_duplicates(subset=["collection_id"]).copy()

    track_cols = [
        "track_id", "trackname", "tracknumber", "trackprice", "discnumber", "tracktimemillis",
        "trackexplicitness", "release_date", "trackviewurl", "is_streamable", "kind",
        "artist_id", "collection_id", "primarygenrename"
    ]
    track_df = df[track_cols].drop_duplicates(subset=["track_id"]).copy()

    genre_df = (
        df[["primarygenrename"]]
        .drop_duplicates()
        .reset_index(drop=True)
        .reset_index()
        .rename(columns={"index": "genre_id"})
    )
    track_df = track_df.merge(genre_df, on="primarygenrename", how="left").drop(columns="primarygenrename")

    track_prices_df = (
        df[["track_id", "trackprice", "checked_at"]]
        .dropna(subset=["track_id", "trackprice", "checked_at"])
        .drop_duplicates(subset=["track_id", "checked_at"])
    )

    album_prices_df = (
        df[["collection_id", "collectionprice", "checked_at"]]
        .dropna(subset=["collection_id", "collectionprice", "checked_at"])
        .drop_duplicates(subset=["collection_id", "checked_at"])
    )

    return {
        "artist": artist_df,
        "album": album_df,
        "track": track_df,
        "genre": genre_df,
        "track_prices": track_prices_df,
        "album_prices": album_prices_df
    }
 
