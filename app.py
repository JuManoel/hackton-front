# main.py
import streamlit as st
from components.chat import render_chat_messages
from components.audio_handler import handle_audio_input

st.title("Asistente virtual")

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

col1, col2 = st.columns(2)

with col1:
    # Captura de audio
    audio_value = st.audio_input("Comienza a hablar")

    # Renderizar el historial de mensajes de chat
    render_chat_messages()

    # Procesar entrada de audio
    handle_audio_input(audio_value)

with col2:
    # Video de ejemplo
    st.video("./testVideo/Untitled video.mp4", format="video/mp4", start_time=0, autoplay=True)
