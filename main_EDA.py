import requests
import pandas as pd
import time
import os
from datetime import datetime, UTC
from itertools import product
from dotenv import load_dotenv

def main():
    # Cargar variables de entorno
    load_dotenv()
    API_URL = os.getenv("ITUNES_API_URL")

    # Configuración
    CARPETA_DATOS = "datos_diarios"
    LOG_TERMS = "terminos_usados.txt"
    os.makedirs(CARPETA_DATOS, exist_ok=True)

    # Generar combinaciones 'aa' a 'zz'
    TERMINOS = [''.join(p) for p in product('abcdefghijklmnopqrstuvwxyz', repeat=2)]
    TERMINOS_POR_DIA = 97  # Para completar en 7 días

    # Cargar términos ya usados
    def cargar_terminos_usados():
        if os.path.exists(LOG_TERMS):
            with open(LOG_TERMS, "r") as f:
                return set(line.strip() for line in f.readlines())
        return set()

    # Guardar término como usado
    def guardar_termino_usado(term):
        with open(LOG_TERMS, "a") as f:
            f.write(f"{term}\n")

    # Buscar en la API de iTunes y devolver todas las columnas disponibles
    def buscar_itunes(term, limit=200):
        params = {
            "term": term,
            "limit": limit,
            "country": "US",
            "media": "music"
        }

        try:
            response = requests.get(API_URL, params=params)
            if response.status_code == 200:
                results = response.json().get("results", [])
                df = pd.json_normalize(results)
                if not df.empty:
                    df["checked_at"] = datetime.now(UTC).isoformat()
                    return df
        except Exception as e:
            print(f"❌ Error con '{term}': {e}")
        return pd.DataFrame()

    # Ejecutar scraping para múltiples términos por día
    usados = cargar_terminos_usados()
    pendientes = [t for t in TERMINOS if t not in usados][:TERMINOS_POR_DIA]

    if not pendientes:
        print("✅ Todos los términos han sido usados.")
        return

    dfs = []

    for termino in pendientes:
        print(f"🔍 Buscando: '{termino}'")
        df = buscar_itunes(termino)
        if not df.empty:
            dfs.append(df)
            guardar_termino_usado(termino)
            print(f"✅ {len(df)} resultados para '{termino}'")
        else:
            print(f"⚠️ Sin resultados para '{termino}'")
        time.sleep(1)

    if dfs:
        df_total = pd.concat(dfs, ignore_index=True)
        hoy = datetime.now(UTC).strftime("%Y-%m-%d")
        archivo_salida = f"{CARPETA_DATOS}/itunes_{hoy}.csv"
        df_total.to_csv(archivo_salida, index=False)
        print(f"📦 Guardados {len(df_total)} registros en '{archivo_salida}'")

if __name__ == "__main__":
    main()
