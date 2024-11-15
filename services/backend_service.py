# services/backend_service.py
import os
import streamlit as st
import requests
from dotenv import load_dotenv
import json

load_dotenv()

urlBackend = os.getenv("URL_BACKEND")

def iniciar_conversacion():
    """Envía una solicitud al backend para iniciar la conversación y obtener un session_id."""
    try:
        response = requests.post(f"{urlBackend}/startCall")
        response.raise_for_status()
        data = response.json()

        return data
    except requests.exceptions.RequestException as e:
        st.error("Error al conectar con el servidor.")
        return None
