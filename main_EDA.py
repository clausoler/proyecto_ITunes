from src.EDA.explore import *
import os

RUTA_DATOS = "data/data_limpio/itunes.pkl"
CARPETA_SALIDA = "output/plots"
os.makedirs(CARPETA_SALIDA, exist_ok=True)

def main():
    # 1. Carga de datos
    df = cargar_dataset(RUTA_DATOS)

    # 2. Información general
    resumen_dataset(df)
    contar_variables_por_tipo(df)
    estadisticas = estadisticas_descriptivas(df)
    print("\nEstadísticas numéricas:\n", estadisticas['numericas'].head())
    print("\nEstadísticas categóricas:\n", estadisticas['categoricas'].head())

    # 3. Visualizaciones generales
    visualizar_variables_numericas(df, guardar=True, carpeta=CARPETA_SALIDA)
    graficar_matriz_correlacion(df, guardar=True, ruta=f"{CARPETA_SALIDA}/matriz_correlacion.png")
    scatter_precio_vs_duracion(df, guardar=True, ruta=f"{CARPETA_SALIDA}/scatter_precio_vs_duracion.png")
    graficar_categoricas_baja_cardinalidad(df, guardar=True, carpeta=CARPETA_SALIDA)

    # 4. Outliers
    df_outliers = resumen_outliers(df)
    print("\nResumen de outliers:\n", df_outliers)

    # 5. Histogramas y residuos
    histograma_precio(df, guardar=True, ruta=f"{CARPETA_SALIDA}/hist_precio_canciones.png")
    graficar_residuos_lineales(df, guardar=True, ruta=f"{CARPETA_SALIDA}/residuos_precio_cancion.png")
    histograma_precio_albumes(df, guardar=True, ruta=f"{CARPETA_SALIDA}/hist_precio_albumes.png")
    graficar_residuos_lineales_album(df, guardar=True, ruta=f"{CARPETA_SALIDA}/residuos_precio_album.png")

    # 6. Género y explicitud
    genre_price = df.groupby('primaryGenreName')['trackPrice'].mean().sort_values(ascending=False).head(15)
    graficar_precio_medio_por_genero(genre_price, guardar=True, ruta=f"{CARPETA_SALIDA}/precio_por_genero.png")

    explicit_stats_df = df.groupby('trackExplicitness')[['trackPrice', 'trackTimeMillis']].mean()
    explicit_stats_df['trackTimeMinutes'] = explicit_stats_df['trackTimeMillis'] / 60000
    graficar_precio_y_duracion_por_explicitud(explicit_stats_df, guardar=True, ruta=f"{CARPETA_SALIDA}/precio_duracion_explicitud.png")

    top_artists_df = df.groupby('artistName')['trackPrice'].mean().sort_values(ascending=False).head(10).to_frame(name='Precio medio (USD)')
    graficar_precio_medio_por_artista(top_artists_df, guardar=True, ruta=f"{CARPETA_SALIDA}/precio_por_artista.png")

    # 7. Canciones largas y géneros comunes
    generos_10min = df[df['trackTimeMillis'] > 600000]['primaryGenreName'].value_counts()
    graficar_generos_canciones_largas(generos_10min, guardar=True, ruta=f"{CARPETA_SALIDA}/generos_largos.png")

    # 8. Colecciones premium
    colecciones_caras = obtener_colecciones_outliers(df)
    print("\nColecciones premium (outliers):\n", colecciones_caras)

    # 9. Duración y precio por género
    graficar_duracion_y_precio_por_genero(df, guardar=True, ruta=f"{CARPETA_SALIDA}/duracion_precio_por_genero.png")

    # 10. Evolución temporal de precios
    graficar_precio_medio_diario(df, columna_precio='trackPrice', guardar=True, ruta=f"{CARPETA_SALIDA}/evolucion_precio_track.png")
    graficar_precio_medio_diario(df, columna_precio='collectionPrice', guardar=True, ruta=f"{CARPETA_SALIDA}/evolucion_precio_album.png")
    
    # 11. Streaming
    graficar_streaming_disponible(df, guardar=True, carpeta=CARPETA_SALIDA)

if __name__ == "__main__":
    main()
