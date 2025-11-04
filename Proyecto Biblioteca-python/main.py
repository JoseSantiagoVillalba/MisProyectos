import streamlit as st
import funciones

CSV_FILE = "catalogo.csv"

st.set_page_config(page_title="Biblioteca CSV", page_icon="📚", layout="wide")

st.title("📚 Biblioteca LOS LOPEZ")
st.caption("Administración simple de títulos y ejemplares usando CSV.")

if "catalogo" not in st.session_state:
    st.session_state.catalogo = funciones.cargar_catalogo_desde_csv()

# ----------------------------
# Pestañas de acciones
# ----------------------------

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "➕ Agregar título",
    "📦 Editar ejemplares",
    "📋 Mostrar catálogo",
    "🔍 Consultar disponibilidad",
    "⚠️ Listar agotados",
    "🧮 Venta / Devolución",
    "🗑️ Eliminar libros",
    "💾 Guardar cambios"
])

# --- TAB 1: Agregar título ---
with tab1:
    st.subheader("Agregar un nuevo título")
    titulo = st.text_input("Título del libro:")
    cantidad = st.number_input("Cantidad inicial:", min_value=0, step=1)

    if st.button("Agregar título"):
        if not funciones.titulo_valido(titulo):
            st.error("Ingrese un título válido.")
        elif funciones.existe_titulo(st.session_state.catalogo, titulo):
            st.warning("El título ya existe en el catálogo.")
        else:
            st.session_state.catalogo.append({
                "TITULO": titulo.strip(),
                "CANTIDAD": cantidad
            })
            st.success(f"'{titulo}' agregado con {cantidad} ejemplares.")
            funciones.guardar_catalogo_a_csv(st.session_state.catalogo)


# --- TAB 2: Ingresar ejemplares ---

with tab2:
    st.subheader("Sumar ejemplares a un título existente") 
    titulos = [libro["TITULO"] for libro in st.session_state.catalogo] 
    if titulos: 
        seleccionado = st.selectbox("Seleccionar título", titulos, key="select_agregar_ejemplares") 
        cantidad = st.number_input("Cantidad a sumar", min_value=0, step=1) 
        if st.button("Agregar ejemplares"):    
            idx = funciones.buscar_indice_por_titulo(st.session_state.catalogo, seleccionado)
            st.session_state.catalogo[idx]["CANTIDAD"] += cantidad 
            funciones.guardar_catalogo_a_csv(st.session_state.catalogo) 
            st.success(f"Se agregaron {cantidad} ejemplares a '{seleccionado}'.") 
    else: 
        st.info("El catálogo está vacío.")




# --- TAB 3: Mostrar catálogo ---
with tab3:
    st.subheader("Catálogo completo")
    if st.session_state.catalogo:
        st.table(st.session_state.catalogo)
    else:
        st.info("No hay libros cargados.")


# --- TAB 4: Consultar disponibilidad ---
with tab4:
    st.subheader("Consultar disponibilidad de un título")
    titulos = [libro["TITULO"] for libro in st.session_state.catalogo]
    if titulos:
        seleccionado = st.selectbox("Seleccionar título", titulos, key="select_disponibilidad")
        idx = funciones.buscar_indice_por_titulo(st.session_state.catalogo, seleccionado)
        cantidad = st.session_state.catalogo[idx]["CANTIDAD"]
        if cantidad > 0:
            st.success(f"'{seleccionado}' tiene {cantidad} ejemplar(es) disponible(s).")
        else:
            st.error(f"'{seleccionado}' no tiene ejemplares disponibles.")
    else:
        st.info("No hay libros cargados.")


# --- TAB 5: Listar agotados ---
with tab5:
    st.subheader("Libros agotados")
    agotados = [libro["TITULO"] for libro in st.session_state.catalogo if libro["CANTIDAD"] == 0]
    if agotados:
        st.warning("Los siguientes títulos están agotados:")
        st.write(agotados)
    else:
        st.success("No hay títulos agotados.")


# --- TAB 6: Préstamo / Devolución ---
with tab6:
    st.subheader("Actualizar ejemplares por préstamo o devolución")
    titulos = [libro["TITULO"] for libro in st.session_state.catalogo]
    if titulos:
        seleccionado = st.selectbox("Seleccionar título", titulos, key="select_prestamo")
        accion = st.radio("Acción:", ["Vender", "Devolver"])
        if st.button("Actualizar ejemplares"):
            idx = funciones.buscar_indice_por_titulo(st.session_state.catalogo, seleccionado)
            if accion == "Vender":
                if st.session_state.catalogo[idx]["CANTIDAD"] > 0:
                    st.session_state.catalogo[idx]["CANTIDAD"] -= 1
                    st.success(f"Se vendió 1 ejemplar de '{seleccionado}'.")
                else:
                    st.error("No quedan ejemplares para Vender.")
            else:
                st.session_state.catalogo[idx]["CANTIDAD"] += 1
                st.success(f"Se devolvió 1 ejemplar de '{seleccionado}'.")
            funciones.guardar_catalogo_a_csv(st.session_state.catalogo)
    else:
        st.info("No hay libros cargados.")

# --- TAB 7: Eliminar ---
with tab7:
    st.subheader("Eliminar un título del catálogo")
    titulos = [libro["TITULO"] for libro in st.session_state.catalogo]
    if titulos:
        seleccionado = st.selectbox("Seleccionar título a eliminar", titulos, key="select_eliminar_titulo")

        if st.button("Eliminar título"):
            # Buscar el índice del título seleccionado
            idx = funciones.buscar_indice_por_titulo(st.session_state.catalogo, seleccionado)
            # Confirmar antes de eliminar (opcional)
            if idx is not None:
                st.session_state.catalogo.pop(idx)
                funciones.guardar_catalogo_a_csv(st.session_state.catalogo)
                st.success(f"El título '{seleccionado}' fue eliminado del catálogo.")
            else:
                st.error("No se encontró el título en el catálogo.")
    else:
        st.info("El catálogo está vacío.")


# --- TAB 8: Guardar manualmente ---
with tab8:
    if st.button("💾 Guardar catálogo a CSV"):
        funciones.guardar_catalogo_a_csv(st.session_state.catalogo)
        st.success("Catálogo guardado correctamente.")
