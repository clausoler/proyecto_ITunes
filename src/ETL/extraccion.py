import requests
import pandas as pd
import time
import os
from datetime import datetime, UTC
from itertools import product
from dotenv import load_dotenv

def configurar_extraccion():
    load_dotenv()
    API_URL = os.getenv("ITUNES_API_URL")

    CARPETA_DATOS = "../data/data_raw"
    LOG_TERMS = "terminos_usados.txt"
    os.makedirs(CARPETA_DATOS, exist_ok=True)

    TERMINOS = [''.join(p) for p in product('abcdefghijklmnopqrstuvwxyz', repeat=2)]
    TERMINOS_POR_DIA = 97

    return {
        "API_URL": API_URL,
        "CARPETA_DATOS": CARPETA_DATOS,
        "LOG_TERMS": LOG_TERMS,
        "TERMINOS": TERMINOS,
        "TERMINOS_POR_DIA": TERMINOS_POR_DIA
    }

def cargar_terminos_usados(log_path):
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            return set(line.strip() for line in f.readlines())
    return set()

def guardar_termino_usado(term, log_path):
    with open(log_path, "a") as f:
        f.write(f"{term}\n")

def buscar_itunes(term, api_url, limit=200):
    params = {
        "term": term,
        "limit": limit,
        "country": "US",
        "media": "music"
    }

    try:
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            results = response.json().get("results", [])
            df = pd.json_normalize(results)
            if not df.empty:
                df["checked_at"] = datetime.now(UTC).date()
                return df
    except Exception as e:
        print(f"❌ Error con '{term}': {e}")
    return pd.DataFrame()

def ejecutar_scrape_diario(config):
    usados = cargar_terminos_usados(config["LOG_TERMS"])
    pendientes = [t for t in config["TERMINOS"] if t not in usados][:config["TERMINOS_POR_DIA"]]

    if not pendientes:
        print("✅ Todos los términos han sido usados.")
        return

    dfs = []

    for termino in pendientes:
        print(f"🔍 Buscando: '{termino}'")
        df = buscar_itunes(termino, config["API_URL"])
        if not df.empty:
            dfs.append(df)
            guardar_termino_usado(termino, config["LOG_TERMS"])
            print(f"✅ {len(df)} resultados para '{termino}'")
        else:
            print(f"⚠️ Sin resultados para '{termino}'")
        time.sleep(1)

    if dfs:
        df_total = pd.concat(dfs, ignore_index=True)
        hoy = datetime.now().strftime("%Y-%m-%d")
        archivo_salida = f"{config['CARPETA_DATOS']}/itunes_{hoy}.csv"
        df_total.to_csv(archivo_salida, index=False)
        print(f"📦 Guardados {len(df_total)} registros en '{archivo_salida}'")