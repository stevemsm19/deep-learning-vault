import os
import streamlit as st
from app.frontend.utils.constants.sources import SOURCES

current_page = "sources"
st.session_state.last_page = current_page

st.set_page_config(page_title="Fuentes")
st.title("📚 Fuentes")
st.write("Aquí puedes descargar los recursos utilizados por el sistema:")

for name, filepath in SOURCES.items():

    if not os.path.exists(filepath):
        st.warning(f"El archivo **{name}** no está disponible para descarga.")
        continue

    with open(filepath, "rb") as f:
        file_bytes = f.read()

    with st.container():
        st.html(
            f"""
            <div style="
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                background-color: #f8f9fa;
                border: 1px solid #ddd;
            ">
                <b>{name}</b>
            </div>
            """
        )

        st.download_button(
            label=f"Descargar",
            data=file_bytes,
            file_name=os.path.basename(filepath),
            mime="application/pdf",
            icon=":material/download:",
        )
