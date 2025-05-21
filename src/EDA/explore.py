import pandas as pd

def cargar_dataset(ruta_pkl: str) -> pd.DataFrame:
    """
    Carga un dataset desde un archivo .pkl y retorna un DataFrame.
    
    Parámetros:
    - ruta_pkl: Ruta al archivo pickle (.pkl)

    Retorna:
    - DataFrame cargado
    """
    df = pd.read_pickle(ruta_pkl)
    return df

def resumen_dataset(df: pd.DataFrame, mostrar: bool = True) -> pd.Series:
    """
    Muestra un resumen básico del dataset: dimensiones, tipos de datos y % de nulos.

    Parámetros:
    - df: DataFrame a analizar
    - mostrar: Si es True, imprime la información

    Retorna:
    - Serie con porcentaje de nulos por columna (solo las que tienen nulos)
    """
    if mostrar:
        print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
        print("\nTipos de datos:")
        print(df.dtypes.value_counts())

    nulos = df.isnull().mean().sort_values(ascending=False) * 100
    return nulos[nulos > 0]

def contar_variables_por_tipo(df: pd.DataFrame, mostrar: bool = True) -> tuple:
    """
    Cuenta y clasifica las variables del DataFrame en numéricas y categóricas.

    Parámetros:
    - df: DataFrame a analizar
    - mostrar: Si es True, imprime la cantidad de cada tipo

    Retorna:
    - Tuple con listas: (variables_numéricas, variables_categóricas)
    """
    num_vars = df.select_dtypes(include='number').columns.tolist()
    cat_vars = df.select_dtypes(exclude='number').columns.tolist()

    if mostrar:
        print("Variables numéricas:", len(num_vars))
        print("Variables categóricas:", len(cat_vars))

    return num_vars, cat_vars

 
def estadisticas_descriptivas(df: pd.DataFrame) -> dict:
    """
    Calcula estadísticas descriptivas para variables numéricas y categóricas.

    Parámetros:
    - df: DataFrame a analizar

    Retorna:
    - Diccionario con dos DataFrames:
        - 'numericas': estadísticas para variables numéricas
        - 'categoricas': estadísticas para variables categóricas
    """
    resumen = {
        'numericas': df.describe().T,
        'categoricas': df.describe(include='object').T
    }
    return resumen

 
import matplotlib.pyplot as plt
import seaborn as sns

def visualizar_variables_numericas(df: pd.DataFrame, columnas: list = None, guardar: bool = False, carpeta: str = None) -> None:
    """
    Genera histogramas y boxplots para cada variable numérica del DataFrame.

    Parámetros:
    - df: DataFrame a visualizar
    - columnas: Lista de columnas numéricas a graficar. Si es None, se usan todas las numéricas.
    - guardar: Si True, guarda los gráficos como archivos PNG.
    - carpeta: Ruta de la carpeta donde guardar los archivos.
    """
    if columnas is None:
        columnas = df.select_dtypes(include='number').columns

    for col in columnas:
        # Histograma
        plt.figure(figsize=(6, 4))
        sns.histplot(df[col].dropna(), kde=True, bins=30)
        plt.title(f'Distribución: {col}')
        plt.tight_layout()
        if guardar and carpeta:
            plt.savefig(f"{carpeta}/{col}_histograma.png")
        plt.show()

        # Boxplot
        plt.figure(figsize=(6, 2))
        sns.boxplot(x=df[col])
        plt.title(f'Boxplot: {col}')
        plt.tight_layout()
        if guardar and carpeta:
            plt.savefig(f"{carpeta}/{col}_boxplot.png")
        plt.show()


 
def graficar_matriz_correlacion(df: pd.DataFrame, metodo: str = 'pearson', guardar: bool = False, ruta: str = None) -> None:
    """
    Muestra una matriz de correlación para variables numéricas con un mapa de calor.

    Parámetros:
    - df: DataFrame a analizar
    - metodo: Método de correlación ('pearson', 'spearman' o 'kendall')
    - guardar: Si True, guarda la figura como archivo
    - ruta: Ruta completa del archivo donde guardar (incluyendo .png)
    """
    corr_matrix = df.select_dtypes(include='number').corr(method=metodo)

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(f'Matriz de Correlación ({metodo.title()})')
    plt.tight_layout()

    if guardar and ruta:
        plt.savefig(ruta)

    plt.show()

 
def scatter_precio_vs_duracion(df: pd.DataFrame, guardar: bool = False, ruta: str = None) -> None:
    """
    Genera un scatter plot entre precio de la canción y su duración.

    Parámetros:
    - df: DataFrame con los datos
    - guardar: Si True, guarda el gráfico en un archivo
    - ruta: Ruta completa del archivo donde guardar (incluyendo .png)
    """
    plt.figure(figsize=(6, 4))
    sns.scatterplot(data=df, x='trackPrice', y='trackTimeMillis')
    plt.title('Precio vs Duración')
    plt.tight_layout()

    if guardar and ruta:
        plt.savefig(ruta)

    plt.show()


 
def graficar_categoricas_baja_cardinalidad(df: pd.DataFrame, max_valores: int = 10, guardar: bool = False, carpeta: str = None) -> None:
    """
    Genera gráficos de barras para variables categóricas con baja cardinalidad.

    Parámetros:
    - df: DataFrame a visualizar
    - max_valores: Máximo número de categorías únicas para considerar baja cardinalidad
    - guardar: Si True, guarda cada gráfico como archivo PNG
    - carpeta: Ruta de la carpeta donde guardar los archivos
    """
    cat_cols = df.select_dtypes(include='object').nunique()
    low_card = cat_cols[cat_cols <= max_valores].index.tolist()

    for col in low_card:
        plt.figure(figsize=(6, 4))
        df[col].value_counts().plot(kind='bar', title=col)
        plt.tight_layout()

        if guardar and carpeta:
            plt.savefig(f"{carpeta}/{col}_barras.png")

        plt.show()


def resumen_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el número y porcentaje de outliers por columna numérica usando la regla del IQR.

    Parámetros:
    - df: DataFrame a analizar

    Retorna:
    - DataFrame con columnas: 'columna', 'outliers (abs)', 'outliers (%)'
    """
    outlier_summary = []
    n_rows = df.shape[0]

    for col in df.select_dtypes(include='number').columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        mask = (df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)
        total_outliers = mask.sum()
        percent_outliers = 100 * total_outliers / n_rows
        outlier_summary.append({
            'columna': col,
            'outliers (abs)': total_outliers,
            'outliers (%)': round(percent_outliers, 2)
        })

    return pd.DataFrame(outlier_summary).sort_values(by='outliers (%)', ascending=False)

def histograma_precio(df: pd.DataFrame, columna: str = 'trackPrice', guardar: bool = False, ruta: str = None) -> None:
    """
    Muestra un histograma de la columna de precio especificada y permite guardarlo.

    Parámetros:
    - df: DataFrame que contiene los datos
    - columna: Nombre de la columna de precios (por defecto 'trackPrice')
    - guardar: Si True, guarda el gráfico en un archivo
    - ruta: Ruta completa del archivo donde guardar (incluyendo .png)
    """
    plt.figure(figsize=(6, 4))
    df[columna].dropna().hist(bins=30)
    plt.title("Distribución de Precio de Canciones")
    plt.xlabel("Precio (USD)")
    plt.ylabel("Frecuencia")
    plt.tight_layout()

    if guardar and ruta:
        plt.savefig(ruta)

    plt.show()


from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt

def graficar_residuos_lineales(df: pd.DataFrame,
                                variable_independiente: str = 'trackTimeMillis',
                                variable_dependiente: str = 'trackPrice',
                                guardar: bool = False,
                                ruta: str = None) -> None:
    """
    Ajusta un modelo lineal simple y grafica los residuos.

    Parámetros:
    - df: DataFrame con los datos
    - variable_independiente: Nombre de la variable X
    - variable_dependiente: Nombre de la variable Y
    - guardar: Si True, guarda el gráfico como archivo PNG
    - ruta: Ruta completa del archivo donde guardar (incluyendo .png)
    """
    df_model = df[[variable_dependiente, variable_independiente]].dropna()
    X = df_model[[variable_independiente]]
    y = df_model[variable_dependiente]

    model = LinearRegression()
    model.fit(X, y)
    preds = model.predict(X)
    residuals = y - preds

    # Gráfico de residuos
    plt.figure(figsize=(6, 4))
    sns.scatterplot(x=preds, y=residuals)
    plt.axhline(0, linestyle='--', color='red')
    plt.title("Residuos del modelo lineal")
    plt.xlabel("Precio estimado")
    plt.ylabel("Residuos")
    plt.tight_layout()

    if guardar and ruta:
        plt.savefig(ruta)

    plt.show()


def histograma_precio_albumes(df: pd.DataFrame, columna: str = 'collectionPrice', guardar: bool = False, ruta: str = None) -> None:
    """
    Muestra un histograma de precios de álbumes y permite guardar el gráfico.

    Parámetros:
    - df: DataFrame con los datos
    - columna: Nombre de la columna de precio (por defecto 'collectionPrice')
    - guardar: Si True, guarda el gráfico en un archivo
    - ruta: Ruta completa del archivo donde guardar (incluyendo .png)
    """
    plt.figure(figsize=(6, 4))
    df[columna].dropna().hist(bins=30)
    plt.title("Distribución de Precio de Álbumes")
    plt.xlabel("Precio (USD)")
    plt.ylabel("Frecuencia")
    plt.tight_layout()

    if guardar and ruta:
        plt.savefig(ruta)

    plt.show()


from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt

def graficar_residuos_lineales_album(df: pd.DataFrame,
                                     variable_independiente: str = 'trackTimeMillis',
                                     variable_dependiente: str = 'collectionPrice',
                                     guardar: bool = False,
                                     ruta: str = None) -> None:
    """
    Ajusta un modelo lineal simple entre duración y precio del álbum y grafica los residuos.

    Parámetros:
    - df: DataFrame con los datos
    - variable_independiente: Variable predictora (X)
    - variable_dependiente: Variable objetivo (Y, por defecto 'collectionPrice')
    - guardar: Si True, guarda el gráfico como archivo PNG
    - ruta: Ruta completa del archivo donde guardar (incluyendo .png)
    """
    df_model = df[[variable_dependiente, variable_independiente]].dropna()
    X = df_model[[variable_independiente]]
    y = df_model[variable_dependiente]

    model = LinearRegression()
    model.fit(X, y)
    preds = model.predict(X)
    residuals = y - preds

    # Gráfico de residuos
    plt.figure(figsize=(6, 4))
    sns.scatterplot(x=preds, y=residuals)
    plt.axhline(0, linestyle='--', color='red')
    plt.title("Residuos del modelo lineal (Álbum)")
    plt.xlabel("Precio estimado")
    plt.ylabel("Residuos")
    plt.tight_layout()

    if guardar and ruta:
        plt.savefig(ruta)

    plt.show()


def graficar_precio_medio_por_genero(genre_price: pd.Series, guardar: bool = False, ruta: str = None) -> None:
    """
    Grafica el precio medio por género musical.

    Parámetros:
    - genre_price: Serie con índices como géneros y valores como precios medios
    - guardar: Si True, guarda el gráfico como archivo PNG
    - ruta: Ruta completa del archivo donde guardar (incluyendo .png)
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(x=genre_price.values, y=genre_price.index)
    plt.title("Precio medio por Género Musical (Top 15)")
    plt.xlabel("Precio medio (USD)")
    plt.ylabel("Género")
    plt.tight_layout()

    if guardar and ruta:
        plt.savefig(ruta)

    plt.show()


def graficar_precio_y_duracion_por_explicitud(explicit_stats_df: pd.DataFrame, guardar: bool = False, ruta: str = None) -> None:
    """
    Grafica el precio y duración media por tipo de explicitud.

    Parámetros:
    - explicit_stats_df: DataFrame con columnas 'trackPrice' y 'trackTimeMinutes', indexado por tipo de explicitud
    - guardar: Si True, guarda el gráfico como archivo PNG
    - ruta: Ruta completa del archivo donde guardar (incluyendo .png)
    """
    explicit_stats_df = explicit_stats_df.sort_values(by="trackPrice", ascending=False)

    fig, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(x=explicit_stats_df.index, y=explicit_stats_df['trackPrice'], ax=ax1, color="skyblue")
    ax1.set_ylabel("Precio medio (USD)")
    ax1.set_title("Precio y Duración media por Tipo de Explicitud")

    ax2 = ax1.twinx()
    sns.lineplot(x=explicit_stats_df.index, y=explicit_stats_df['trackTimeMinutes'], ax=ax2, color="orange", marker="o")
    ax2.set_ylabel("Duración media (minutos)")

    plt.tight_layout()

    if guardar and ruta:
        plt.savefig(ruta)

    plt.show()


def graficar_precio_medio_por_artista(top_artists_df: pd.DataFrame, guardar: bool = False, ruta: str = None) -> None:
    """
    Grafica el precio medio por artista (Top 10).

    Parámetros:
    - top_artists_df: DataFrame con índice como nombres de artistas y columna 'Precio medio (USD)'
    - guardar: Si True, guarda el gráfico como archivo PNG
    - ruta: Ruta completa del archivo donde guardar (incluyendo .png)
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_artists_df['Precio medio (USD)'], y=top_artists_df.index)
    plt.title("Artistas con Precio Medio más Alto (Top 10)")
    plt.xlabel("Precio medio (USD)")
    plt.ylabel("Artista")
    plt.tight_layout()

    if guardar and ruta:
        plt.savefig(ruta)

    plt.show()


def graficar_generos_canciones_largas(generos_10min: pd.Series, top_n: int = 10, guardar: bool = False, ruta: str = None) -> None:
    """
    Grafica los géneros más comunes entre canciones de más de 10 minutos.

    Parámetros:
    - generos_10min: Serie con géneros como índice y cantidad de canciones como valores
    - top_n: Número de géneros a mostrar (por defecto 10)
    - guardar: Si True, guarda el gráfico como archivo PNG
    - ruta: Ruta completa del archivo donde guardar (incluyendo .png)
    """
    top_generos = generos_10min.head(top_n).sort_values()

    plt.figure(figsize=(8, 6))
    sns.barplot(x=top_generos.values, y=top_generos.index, palette="crest")
    plt.title(f"Géneros más comunes en canciones de más de 10 minutos (Top {top_n})")
    plt.xlabel("Número de canciones")
    plt.ylabel("Género")
    plt.tight_layout()

    if guardar and ruta:
        plt.savefig(ruta)

    plt.show()


def obtener_colecciones_outliers(df: pd.DataFrame, columna: str = 'collectionPrice', top_n: int = 20) -> pd.DataFrame:
    """
    Identifica colecciones con precios outliers y devuelve las más caras.

    Parámetros:
    - df: DataFrame a analizar
    - columna: Columna numérica sobre la que aplicar detección de outliers (por defecto 'collectionPrice')
    - top_n: Número de colecciones a devolver

    Retorna:
    - DataFrame con las colecciones más caras consideradas outliers
    """
    Q1 = df[columna].quantile(0.25)
    Q3 = df[columna].quantile(0.75)
    IQR = Q3 - Q1
    limite_superior = Q3 + 1.5 * IQR

    outliers_precio = df[df[columna] > limite_superior].copy()

    colecciones_caras = (
        outliers_precio
        .groupby(['collectionName', 'artistName'])[columna]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .to_frame(name='Precio colección (USD)')
    )

    return colecciones_caras

def graficar_duracion_y_precio_por_genero(df: pd.DataFrame, top_n: int = 15, guardar: bool = False, ruta: str = None) -> None:
    """
    Calcula duración y precio medio por género musical, y lo grafica.

    Parámetros:
    - df: DataFrame que contiene las columnas 'primaryGenreName', 'trackTimeMillis', y 'trackPrice'
    - top_n: Número de géneros a mostrar en el gráfico (ordenados por duración)
    - guardar: Si True, guarda el gráfico como archivo PNG
    - ruta: Ruta completa del archivo donde guardar (incluyendo .png)
    """
    genero_stats = df.groupby('primaryGenreName')[['trackTimeMillis', 'trackPrice']].mean()
    genero_stats['duracion_minutos'] = genero_stats['trackTimeMillis'] / 60000
    genero_stats = genero_stats[['duracion_minutos', 'trackPrice']].sort_values(by='duracion_minutos', ascending=False).head(top_n)

    fig, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=genero_stats['duracion_minutos'], y=genero_stats.index, ax=ax1, color="skyblue")
    ax1.set_xlabel("Duración media (minutos)")
    ax1.set_ylabel("Género")
    ax1.set_title(f"Duración y Precio medio por Género (Top {top_n} por duración)")

    ax2 = ax1.twiny()
    sns.lineplot(x=genero_stats['trackPrice'], y=genero_stats.index, ax=ax2, color="orange", marker="o", label="Precio medio (USD)")
    ax2.set_xlabel("Precio medio (USD)")
    ax2.legend(loc='lower right')

    plt.tight_layout()

    if guardar and ruta:
        plt.savefig(ruta)

    plt.show()


def graficar_precio_medio_diario(df: pd.DataFrame,
                                  columna_precio: str = 'trackPrice',
                                  columna_fecha: str = 'checked_at',
                                  guardar: bool = False,
                                  ruta: str = None) -> None:
    """
    Convierte la columna de fecha a datetime y grafica el precio medio diario.

    Parámetros:
    - df: DataFrame que contiene las columnas de precio y fecha
    - columna_precio: Nombre de la columna de precio a analizar
    - columna_fecha: Nombre de la columna de fecha
    - guardar: Si True, guarda el gráfico como archivo PNG
    - ruta: Ruta completa del archivo donde guardar
    """
    df[columna_fecha] = pd.to_datetime(df[columna_fecha], errors='coerce')
    precios_diarios = df.groupby(columna_fecha)[columna_precio].mean().sort_index()

    plt.figure(figsize=(10, 5))
    precios_diarios.plot(marker='o')
    plt.title(f"Evolución del precio medio de '{columna_precio}' por fecha de scrapeo")
    plt.xlabel("Fecha de scrapeo")
    plt.ylabel("Precio medio (USD)")
    plt.grid(True)
    plt.tight_layout()

    if guardar and ruta:
        plt.savefig(ruta)

    plt.show()
     
def graficar_streaming_disponible(df: pd.DataFrame, guardar: bool = False, carpeta: str = None) -> None:
    """
    Genera visualizaciones sobre la disponibilidad para streaming.

    Parámetros:
    - df: DataFrame que contiene la columna 'is_streamable'
    - guardar: Si True, guarda los gráficos como archivos PNG
    - carpeta: Ruta donde guardar los archivos (si guardar=True)
    """

    # Gráfico circular
    plt.figure(figsize=(5, 5))
    df['is_streamable'].value_counts().plot(
        kind='pie', labels=['Sí', 'No'], autopct='%1.1f%%', startangle=90,
        colors=['#66c2a5', '#fc8d62']
    )
    plt.title("Proporción de canciones disponibles para streaming")
    plt.ylabel("")
    plt.tight_layout()
    if guardar and carpeta:
        plt.savefig(f"{carpeta}/streaming_pie.png")
    plt.show()
