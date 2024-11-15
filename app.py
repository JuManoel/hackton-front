import streamlit as st
from components.chat import render_chat_messages
from components.audio_handler import handle_audio_input
from services.backend_service import iniciar_conversacion
from utils import css

st.title("minstra")

# Inicializar el session_id y el historial de chat
if "session" not in st.session_state:
    st.session_state.session = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "video" not in st.session_state:
    st.session_state.video = None

if "audio" not in st.session_state:
    st.session_state.audio = None

css.inyeccion_css()

def initiate_dialogue():
    session = iniciar_conversacion()
    if session:
        st.session_state.messages.append({"role": "assistant", "content": session.get("content")})
        st.session_state.session = session.get("newCallId")

# Si no hay session_id, mostrar el botón de inicio
if not st.session_state.session:
    st.button("Iniciar conversación", on_click=initiate_dialogue)

else:
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
        st.video("testVideo/idle_or.mp4", format="video/mp4", start_time=0, loop=True, autoplay=True)
        if st.session_state.audio:
            st.audio(st.session_state.audio, format='audio/mp3', start_time=0, autoplay=True)