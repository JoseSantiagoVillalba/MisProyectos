import streamlit as st
import pandas as pd
import funciones_streamlit as fs


st.title("🌍 Buscador de Países")
if fs.existe_archivo_paises():
    data_frame_del_cvs = pd.read_csv("paises.csv")
else:
    data_frame_del_cvs = fs.crear_csv_paises()
    if data_frame_del_cvs is None:
        st.error("No se pudo crear o cargar el archivo 'paises.csv'.")
        st.stop()  # detener la app o hacer algo para avisar

# Inicializar session_state para resultados
if "resultado" not in st.session_state:
    st.session_state.resultado = None

opcion = st.selectbox(
    "Seleccione una opción:",
    ["", "1 - Buscar país por nombre", "2 - Filtrar por población", "3 - Filtrar por superficie", "4 - Filtrar por continente"]
)

# BUSQUEDA POR NOMBRE
if opcion.startswith("1"):
    pais = st.text_input("Ingrese nombre o letras del país:")

    if st.button("Buscar nombre"):
        st.session_state.resultado = fs.busqueda_paises(pais,data_frame_del_cvs)

# BUSQUEDA POR POBLACION
elif opcion.startswith("2"):
    min_p = st.number_input("Población mínima (millones):", min_value=0.0)
    max_p = st.number_input("Población máxima (millones):", min_value=0.0)

    if st.button("Buscar población"):
        st.session_state.resultado = fs.busqueda_poblacion(min_p, max_p,data_frame_del_cvs)

# BUSQUEDA POR SUPERFICIE
elif opcion.startswith("3"):
    min_s = st.number_input("Superficie mínima (km²):", min_value=0.0)
    max_s = st.number_input("Superficie máxima (km²):", min_value=0.0)

    if st.button("Buscar superficie"):
        st.session_state.resultado = fs.busqueda_superficie(min_s, max_s,data_frame_del_cvs)

# BUSQUEDA POR CONTINENTE
elif opcion.startswith("4"):
    continente = st.text_input("Ingrese continente:")

    if st.button("Buscar continente"):
        st.session_state.resultado = fs.busqueda_continente(continente,data_frame_del_cvs)

# MOSTRAR RESULTADOS
if st.session_state.resultado is not None:
    if isinstance(st.session_state.resultado, pd.DataFrame):
        st.dataframe(st.session_state.resultado)
    else:
        st.write(st.session_state.resultado)

    # Botón de estadísticas
    if st.button("Mostrar estadísticas"):
        st.text(fs.estadisticas_poblacion(st.session_state.resultado))
        st.text(fs.estadisticas_superficie(st.session_state.resultado))
        st.text(fs.cantidad_paises_por_continente(st.session_state.resultado))
