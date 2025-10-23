import pandas as pd
import streamlit as st
import os
import requests

def existe_archivo_paises():
    nombre_archivo = "paises.csv"
    if os.path.exists(nombre_archivo):
        return True
    else:
        crear_csv_paises()
        return os.path.exists(nombre_archivo)

def crear_csv_paises():
    try:
        url = "https://restcountries.com/v3.1/independent?status=true"
        response = requests.get(url)
        response.raise_for_status()

        datos = response.json()
        paises = []
        for pais in datos:
            nombre = pais.get("name", {}).get("common", "Desconocido")
            poblacion = round(pais.get("population", 0) / 1_000_000, 2)
            # ‘continents’ es una lista en v3.1:
            continente = pais.get("continents", ["Desconocido"])[0]
            superficie = pais.get("area", 0)

            paises.append({
                "Nombre": nombre,
                "Población (millones)": poblacion,
                "Continente": continente,
                "Superficie (km²)": superficie
            })

        data_frame_del_cvs = pd.DataFrame(paises)
        data_frame_del_cvs.to_csv("paises.csv", index=False, encoding="utf-8")
        st.success("✅ Archivo 'paises.csv' creado exitosamente.")
        return data_frame_del_cvs

    except requests.RequestException as e:
        st.error(f"❌ Error al conectar con la API: {e}")
        return None
    except Exception as e:
        st.error(f"⚠️ Error inesperado: {e}")
        return None



# ------------------------------
# Funciones de búsqueda y estadísticas
# ------------------------------

def busqueda_paises(nombre,data_frame_del_cvs):
    coincidencias = data_frame_del_cvs[data_frame_del_cvs["Nombre"].str.lower().str.contains(nombre.lower())]
    if coincidencias.empty:
        return "No se encontraron países que coincidan."
    else:
        return coincidencias

def busqueda_poblacion(min_p, max_p,data_frame_del_cvs):
    coincidencias = data_frame_del_cvs[(data_frame_del_cvs["Población (millones)"] >= min_p) & (data_frame_del_cvs["Población (millones)"] <= max_p)]
    if coincidencias.empty:
        return "No se encontraron países que coincidan con ese rango de población."
    else:
        return coincidencias

def busqueda_continente(continente,data_frame_del_cvs):
    coincidencias = data_frame_del_cvs[data_frame_del_cvs["Continente"].str.lower().str.contains(continente.lower())]
    if coincidencias.empty:
        return "No se encontraron Continentes que coincidan."
    else:
        return coincidencias

def busqueda_superficie(min_s, max_s,data_frame_del_cvs):
    coincidencias = data_frame_del_cvs[(data_frame_del_cvs["Superficie (km²)"] >= min_s) & (data_frame_del_cvs["Superficie (km²)"] <= max_s)]
    if coincidencias.empty:
        return "No se encontraron países que coincidan con ese rango de superficie."
    else:
        return coincidencias
    




#Estadisticas

def cantidad_paises_por_continente(data_frame_del_cvs,datos=None):
    if datos is None:
        datos = data_frame_del_cvs
    if datos.empty:
        return "No hay datos cargados."
    
    conteo = datos["Continente"].value_counts()
    resultado = "Cantidad de países por continente:\n"

    for continente, cantidad in conteo.items():
        resultado += f"{continente}: {cantidad}\n"
    return resultado

def estadisticas_superficie(data_frame_del_cvs,datos=None):
    if datos is None:
        datos = data_frame_del_cvs
    if datos.empty:
        return "No hay datos disponibles."

    pais_menor = datos.loc[datos["Superficie (km²)"].idxmin()]
    pais_mayor = datos.loc[datos["Superficie (km²)"].idxmax()]
    promedio = datos["Superficie (km²)"].mean()

    return f"""
País con menor Superficie: {pais_menor['Nombre']} ({pais_menor['Superficie (km²)']} km²)
País con mayor Superficie: {pais_mayor['Nombre']} ({pais_mayor['Superficie (km²)']} km²)
Promedio de Superficie: {round(promedio, 2)} km² \n \n
"""

def estadisticas_poblacion(data_frame_del_cvs,datos=None):
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
Promedio de población: {round(promedio, 2)} millones \n \n
"""
