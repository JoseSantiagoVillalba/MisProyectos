import pandas as pd
import streamlit as st

# Cargar CSV
data_frame_del_cvs = pd.read_csv("paises.csv")

# ------------------------------
# Funciones de búsqueda y estadísticas
# ------------------------------

def busqueda_paises(nombre):
    coincidencias = data_frame_del_cvs[data_frame_del_cvs["Nombre"].str.lower().str.contains(nombre.lower())]
    if coincidencias.empty:
        return "No se encontraron países que coincidan."
    else:
        return coincidencias

def busqueda_poblacion(min_p, max_p):
    coincidencias = data_frame_del_cvs[(data_frame_del_cvs["Población (millones)"] >= min_p) & (data_frame_del_cvs["Población (millones)"] <= max_p)]
    if coincidencias.empty:
        return "No se encontraron países que coincidan con ese rango de población."
    else:
        return coincidencias

def busqueda_continente(continente):
    coincidencias = data_frame_del_cvs[data_frame_del_cvs["Continente"].str.lower().str.contains(continente.lower())]
    if coincidencias.empty:
        return "No se encontraron Continentes que coincidan."
    else:
        return coincidencias

def busqueda_superficie(min_s, max_s):
    coincidencias = data_frame_del_cvs[(data_frame_del_cvs["Superficie (km²)"] >= min_s) & (data_frame_del_cvs["Superficie (km²)"] <= max_s)]
    if coincidencias.empty:
        return "No se encontraron países que coincidan con ese rango de superficie."
    else:
        return coincidencias


def cantidad_paises_por_continente(datos=None):
    if datos is None:
        datos = data_frame_del_cvs
    if datos.empty:
        return "No hay datos cargados."
    
    conteo = datos["Continente"].value_counts()
    resultado = "Cantidad de países por continente: "
    for cont, cant in conteo.items():
        resultado += f"{cont}: {cant} "
    return resultado



def estadisticas_superficie(datos=None):
    if datos is None:
        datos = data_frame_del_cvs
    if datos.empty:
        return "No hay datos disponibles."

    pais_menor = datos.loc[datos["Superficie (km²)"].idxmin()]
    pais_mayor = datos.loc[datos["Superficie (km²)"].idxmax()]
    promedio = datos["Superficie (km²)"].mean()

    return f"""
País con menor Superficie: {pais_menor['Nombre']} ({pais_menor['Superficie (km²)']}
País con mayor Superficie: {pais_mayor['Nombre']} ({pais_mayor['Superficie (km²)']}
Promedio de Superficie: {round(promedio, 2)} millones
"""

def estadisticas_poblacion(datos=None):
    if datos is None:
        datos = data_frame_del_cvs
    if datos.empty:
        return "No hay datos disponibles."

    pais_menor = datos.loc[datos["Población (millones)"].idxmin()]
    pais_mayor = datos.loc[datos["Población (millones)"].idxmax()]
    promedio = datos["Población (millones)"].mean()

    return f"""
País con menor población: {pais_menor['Nombre']} ({pais_menor['Población (millones)']} millones)
País con mayor población: {pais_mayor['Nombre']} ({pais_mayor['Población (millones)']} millones)
Promedio de población: {round(promedio, 2)} millones
"""
