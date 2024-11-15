# services/backend_service.py
import streamlit as st
import requests
import json
from backend.views import *
urlBackend = st.secrets["URL_BACKEND"]

def iniciar_conversacion():
    """Envía una solicitud al backend para iniciar la conversación y obtener un session_id."""
    try:
        data = startCall()
        return data
    except requests.exceptions.RequestException as e:
        st.error("Error al conectar con el servidor.")
        return None

def send_prompt(data):
    try:
        data =   callTalking(data)
        return data
    except requests.exceptions.RequestException as e:
        st.error("Error al enviar el mensaje")
        return None

def end_talk(id):
    try:
        data = analizeMessage(id)
        return data
    except requests.exceptions.RequestException as e:
        st.error("Error al terminar la llamada")
        return None