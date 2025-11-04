import streamlit as st
import csv
import os

CSV_FILE = "catalogo.csv"

# ----------------------------
# Utilidades
# ----------------------------

def normalizar_titulo(t: str) -> str:
    return " ".join(t.strip().split()).lower()

def titulo_valido(t: str) -> bool:
    return len(normalizar_titulo(t)) > 0


# ----------------------------
# Persistencia CSV
# ----------------------------

def cargar_catalogo_desde_csv() -> list[dict]:
    catalogo = []
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding="utf-8") as archivo:
            campos = ["TITULO","CANTIDAD"]
            crear = csv.DictWriter(archivo, fieldnames=campos)
            crear.writeheader()
        return catalogo

    with open(CSV_FILE, 'r', newline='', encoding="utf-8") as archivo:
        leer = csv.DictReader(archivo)
        for fila in leer:
            try:
                catalogo.append({
                    "TITULO": fila["TITULO"],
                    "CANTIDAD": int(fila["CANTIDAD"])
                })
            except (ValueError, KeyError):
                continue
    return catalogo

def guardar_catalogo_a_csv(catalogo: list[dict]) -> None:
    with open(CSV_FILE, 'w', newline='', encoding="utf-8") as archivo:
        campos = ["TITULO", "CANTIDAD"]
        guardar = csv.DictWriter(archivo, fieldnames=campos)
        guardar.writeheader()
        for i in catalogo:
            guardar.writerow({
                "TITULO": i["TITULO"],
                "CANTIDAD": int(i["CANTIDAD"])
            })


# ----------------------------
# Reglas de negocio
# ----------------------------

def buscar_indice_por_titulo(catalogo: list[dict], titulo_busqueda: str) -> int:
    for i, libro in enumerate(catalogo):
        if normalizar_titulo(libro["TITULO"]) == normalizar_titulo(titulo_busqueda):
            return i
    return -1

def existe_titulo(catalogo: list[dict], titulo: str) -> bool:
    return buscar_indice_por_titulo(catalogo, titulo) != -1



