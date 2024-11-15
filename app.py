import streamlit as st
import streamlit.components.v1 as components
from components.chat import render_chat_messages
from components.audio_handler import handle_audio_input
from services.backend_service import iniciar_conversacion
from utils import css

def custom_video(video_path, key):
    components.html(
        f"""
        <video id="myVideo" width="100%" controls autoplay>
            <source src="{video_path}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        <script>
            var video = document.getElementById('myVideo');
            video.onended = function() {{
                window.parent.postMessage({{
                    type: "streamlit:setComponentValue",
                    value: true
                }}, "*");
            }};
        </script>
        """,
        height=300,
        key=key
    )

st.title("minstra")

# Inicializar el session_id y el historial de chat
if "session" not in st.session_state:
    st.session_state.session = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "video" not in st.session_state:
    st.session_state.video = None

if "idle_video" not in st.session_state:
    with open("./testVideo/idle_avatar.mp4", "rb") as file:
        st.session_state.idle_video = file.read()

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
        # Video
        if st.session_state.video:
            video_ended = custom_video(st.session_state.video, key="video_player")
            if video_ended:
                st.session_state.video = None
                st.rerun()
        else:
            st.video(st.session_state.idle_video, format="video/mp4", start_time=0, autoplay=True, loop=True)