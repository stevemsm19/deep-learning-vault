import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from typing import List, Optional, Tuple

from app.frontend.services.api_service import upload_files
from app.frontend.utils.messages import show_temporary_message


def upload_documents_sidebar() -> Optional[List[UploadedFile]]:
    with st.sidebar:
        st.subheader("Tus documentos")
        documents = st.file_uploader(
            label="Haz click en 'Browse files' para subir tus archivos .pdf y/o .txt",
            type=["pdf", "txt"],
            accept_multiple_files=True,
            key="documents",
        )
        return documents


# def handle_upload_button(documents: Optional[List[UploadedFile]]) -> None:
#     with st.sidebar:
#         if st.button(
#             "Cargar Documentos",
#             type="primary",
#             disabled=getattr(st.session_state, "is_processing_answer", False),
#         ):
#             if documents:
#                 response_data, error = upload_files(documents)

#                 if error:
#                     show_temporary_message(error or "Error desconocido", "error")
#                     return

#                 show_temporary_message(
#                     response_data or "Documentos cargados", "success"
#                 )
#             else:
#                 show_temporary_message(
#                     "Por favor, sube al menos un archivo válido antes de continuar.",
#                     "error",
#                 )


def set_variables_sidebar() -> Tuple[int, float]:
    with st.sidebar:
        st.markdown("---")
        st.subheader("Parámetros del Bot")
        st.caption(
            "Estos valores se pasan al bot para ajustar cómo recupera y prioriza la información almacenada."
        )

        num_results: int = st.number_input(
            label="Número de resultados",
            min_value=1,
            max_value=30,
            value=3,
            step=1,
            help="Número de resultados más relevantes que el bot considerará en su respuesta.",
            disabled=getattr(st.session_state, "is_processing_answer", False),
        )

        threshold_options = {"Bajo": 0.8, "Medio": 0.5, "Alto": 0.3}

        label = st.selectbox(
            "Exactitud de Similitud",
            list(threshold_options.keys()),
            index=1,
            help="Nivel de similitud requerido.",
            disabled=getattr(st.session_state, "is_processing_answer", False),
        )

        similarity_threshold = threshold_options[label]

        return num_results, similarity_threshold


def handle_sidebar() -> Tuple[int, float]:
    upload_documents_sidebar()
    # handle_upload_button(documents)
    return set_variables_sidebar()
