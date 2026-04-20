import streamlit as st
import requests

API = "http://localhost:8000"  # cuando lo subas a EC2 cambias esto por la IP pública

st.title("Sistema de Reservas de Salas")

menu = st.sidebar.selectbox("Menú", ["Usuarios", "Salas", "Reservas"])

# ─── USUARIOS ───────────────────────────────────────────
if menu == "Usuarios":
    st.header("Usuarios")

    with st.form("nuevo_usuario"):
        nombre = st.text_input("Nombre")
        submitted = st.form_submit_button("Crear usuario")
        if submitted and nombre:
            res = requests.post(f"{API}/usuarios/", json={"nombre": nombre})
            if res.status_code == 200:
                st.success(f"Usuario '{nombre}' creado")
            else:
                st.error("Error al crear usuario")

# ─── SALAS ──────────────────────────────────────────────
elif menu == "Salas":
    st.header("Salas")

    with st.form("nueva_sala"):
        numero = st.number_input("Número de sala", min_value=1, step=1)
        capacidad = st.number_input("Capacidad", min_value=1, step=1)
        ubicacion = st.text_input("Ubicación")
        submitted = st.form_submit_button("Crear sala")
        if submitted and ubicacion:
            res = requests.post(f"{API}/salas/", json={
                "numero_de_sala": numero,
                "capacidad": capacidad,
                "ubicacion": ubicacion
            })
            if res.status_code == 200:
                st.success("Sala creada")
            elif res.status_code == 400:
                st.warning("Esa sala ya está registrada")
            else:
                st.error("Error al crear sala")

    st.divider()
    st.subheader("Salas registradas")
    salas = requests.get(f"{API}/salas/").json()
    if salas:
        st.table(salas)
    else:
        st.info("No hay salas registradas")

# ─── RESERVAS ───────────────────────────────────────────
elif menu == "Reservas":
    st.header("Reservas")

    salas = requests.get(f"{API}/salas/").json()

    with st.form("nueva_reserva"):
        usuario_id = st.number_input("ID de usuario", min_value=1, step=1)
        sala_id = st.selectbox(
            "Sala",
            options=[s["id"] for s in salas],
            format_func=lambda x: next(
                f"Sala {s['numero_de_sala']} - {s['ubicacion']}"
                for s in salas if s["id"] == x
            )
        ) if salas else st.warning("No hay salas disponibles")
        fecha = st.date_input("Fecha")
        hora_inicio = st.time_input("Hora inicio")
        hora_fin = st.time_input("Hora fin")
        submitted = st.form_submit_button("Reservar")

        if submitted and salas:
            res = requests.post(f"{API}/reservas/", json={
                "usuario_id": usuario_id,
                "sala_id": sala_id,
                "fecha": str(fecha) + "T00:00:00",
                "hora_inicio": str(hora_inicio),
                "hora_fin": str(hora_fin)
            })
            if res.status_code == 200:
                st.success("Reserva creada")
            elif res.status_code == 404:
                st.error("La sala no existe")
            else:
                st.error("Error al crear reserva")

    st.divider()
    st.subheader("Reservas registradas")
    reservas = requests.get(f"{API}/reservas/").json()
    if reservas:
        for r in reservas:
            st.markdown(f"""
            **Reserva #{r['id']}**  
            👤 {r['usuario']['nombre']} — 🏠 Sala {r['sala']['numero_de_sala']} ({r['sala']['ubicacion']})  
            📅 {r['fecha'][:10]} | ⏰ {r['hora_inicio']} - {r['hora_fin']}
            """)
            st.divider()
    else:
        st.info("No hay reservas registradas")