import time
import requests
import streamlit as st

from streamlit.runtime.uploaded_file_manager import UploadedFile

from typing import List, Optional, Tuple, Dict, Any

from app.frontend.utils.constants.endpoints import (
    DOCUMENTS_ENDPOINT,
    EMBEDDING_ENDPOINT,
    SEARCH_ENDPOINT,
    GET_DOCUMENT_NAMES_ENDPOINT,
)

from app.frontend.config.settings import get_settings

SETTINGS = get_settings()
base_url = f"http://{SETTINGS.api_host}:{SETTINGS.api_port}/api/v1/"


def upload_files(
    documents: Optional[List[UploadedFile]],
) -> Tuple[Optional[str], Optional[str]]:
    if not documents:
        return None, "No hay documentos"

    with st.spinner("Cargando documento(s)...", show_time=True):
        file_payload = [("files", (doc.name, doc, doc.type)) for doc in documents]

        try:
            response = requests.post(
                f"{base_url}{DOCUMENTS_ENDPOINT}",
                files=file_payload,
            )
            if response.status_code != 200:
                return None, f"Error {response.status_code}: {response.text}"

            response_json = response.json()
            total_pages = response_json.get("total_pages")
            total_chunks = response_json.get("total_chunks")
            total_documents = len(documents)

            return (
                f"Se han cargado {total_documents} documentos, con un total de {total_pages} páginas "
                f"divididas en {total_chunks} chunks.",
                None,
            )

        except requests.exceptions.RequestException:
            return None, "Error de conexión"


def get_agent_response(
    prompt: str,
    num_results: int,
    similarity_threshold: float,
    documents_name: Optional[List[str]] = None,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    payload = {
        "query": prompt,
        "num_results": num_results,
        "similarity_threshold": similarity_threshold,
        "documents_name": documents_name,
    }
    with st.spinner("Pensando...", show_time=True):
        try:
            response = requests.post(url=f"{base_url}{SEARCH_ENDPOINT}", json=payload)

            if response.status_code != 200:
                return None, f"Error {response.status_code}: {response.text}"
            return response.json(), None

        except requests.exceptions.RequestException:
            return None, "Error de conexión"


def get_embeddings() -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.get(
            url=f"{base_url}{EMBEDDING_ENDPOINT}",
        )

        if response.status_code != 200:
            return None, f"Error {response.status_code}: {response.text}"

        return response.json(), None

    except requests.exceptions.RequestException:
        return None, "Error de conexión"


def get_document_names() -> Tuple[Optional[List[str]], Optional[str]]:
    with st.spinner("Analizando documento(s)...", show_time=True):
        try:
            response = requests.get(
                url=f"{base_url}{GET_DOCUMENT_NAMES_ENDPOINT}",
            )

            if response.status_code != 200:
                return None, f"Error {response.status_code}: {response.text}"

            data = response.json()
            return data.get("names", []), None

        except requests.exceptions.RequestException:
            return None, "Error de conexión"


def firebase_sign_in(email: str, password: str) -> Tuple[Optional[str], Optional[str]]:
    """Sign in using Firebase REST API and return idToken on success or an error string."""
    api_key = SETTINGS.google_api_key
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return None, f"{response.status_code}: {response.text}"
        data = response.json()
        id_token = data.get("idToken")
        if not id_token:
            return None, "No idToken returned from firebase"
        return id_token, None
    except requests.exceptions.RequestException as e:
        return None, str(e)


import requests
from app.frontend.config.settings import get_settings

SETTINGS = get_settings()


def check_session():
    try:
        res = requests.get(
            f"http://{SETTINGS.api_host}:{SETTINGS.api_port}/api/v1/me",
            cookies=requests.utils.dict_from_cookiejar(
                requests.cookies.RequestsCookieJar()
            ),
        )
        return res.status_code == 200
    except:
        return False
