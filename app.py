import streamlit as st
from components.chat import render_chat_messages
from components.audio_handler import handle_audio_input
from services.backend_service import iniciar_conversacion
from utils import css
from utils.end_call import end_call

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

if "analysis" not in st.session_state:
    st.session_state.analysis = None

css.inyeccion_css()

def initiate_dialogue():
    session = iniciar_conversacion()
    print(session)
    if session:
        st.session_state.messages.append({"role": "assistant", "content": session.get("content")})
        st.session_state.session = session.get("newCallId")

# Si no hay session_id, mostrar el botón de inicio
if not st.session_state.session:
    st.button("Iniciar conversación", on_click=initiate_dialogue)

else:
    col1, col2 = st.columns(2)

    with col1:

        col31, col32 = st.columns(2)
        with col31:
            # Captura de audio
            audio_value = st.audio_input("Comienza a hablar")
        with col32:
            if st.button("terminar la llamada"):
                end_call(st.session_state.session)
        # Renderizar el historial de mensajes de chat
        render_chat_messages()

        # Procesar entrada de audio
        handle_audio_input(audio_value)

    with col2:
        # Video de ejemplo
        st.video("testVideo/idle_or.mp4", format="video/mp4", start_time=0, loop=True, autoplay=True)
        if st.session_state.audio:
            st.audio(st.session_state.audio, format='audio/mp3', start_time=0, autoplay=True)

if st.session_state.analysis:

            analysis = st.session_state.analysis

            # Título
            st.title("Análisis de Datos")

            # Información general
            st.subheader("Información General")
            st.text(f"ID de la llamada: {analysis["callId"]}")
            st.text(f"Precio: ${analysis["precio"]:.5f}")
            st.text(f"Tokens utilizados: {analysis["tokens"]}")

            # Análisis
            st.subheader("Resultados del Análisis")

            st.metric("Tasa de Éxito", f"{analysis["analysis"]['successRate']}%")
            st.metric("Total de Mensajes", analysis["analysis"]["totalMessages"])