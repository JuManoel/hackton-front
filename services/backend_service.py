# services/backend_service.py
import streamlit as st
import requests
import json

urlBackend = st.secrets["URL_BACKEND"]

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

def send_prompt(data):
    try:
        response = requests.put(f"{urlBackend}/call/talking", json=data)
        response.raise_for_status()
        data = response.json()

        return data
    except requests.exceptions.RequestException as e:
        st.error("Error al enviar el mensaje")
        return None
