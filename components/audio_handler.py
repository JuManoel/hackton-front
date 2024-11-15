# components/audio_handler.py
import streamlit as st

from services import groq_service
from services import backend_service
from services import did_service
from gtts import gTTS
import os

def handle_audio_input(audio_value):
    """Procesa la entrada de audio, genera una transcripción y una respuesta."""
    if audio_value:
        # Transcribir el audio
        prompt = groq_service.transcribir_audio(audio_value)

        # Agregar mensaje del usuario al historial de chat
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Mostrar mensaje del usuario en el contenedor de mensajes
        with st.chat_message("user"):
            st.markdown(prompt)

        data = {
            "content": prompt,
            "callId": st.session_state.session
        }

        # Generar una respuesta (aquí solo se devuelve un eco de la entrada del usuario)
        response = backend_service.send_prompt(data)


        url_video = did_service.generar_video(response.get("content"))
        st.session_state.video = url_video


        # Mostrar respuesta del asistente en el contenedor de mensajes
        with st.chat_message("assistant"):
            st.markdown(response.get("content"))

        # Agregar respuesta del asistente al historial de chat
        st.session_state.messages.append({"role": "assistant", "content": response.get("content")})
        # Reproducir el prompt generado usando Google Text-to-Speech

        tts = gTTS(text=response.get("content"), lang='es')
        tts.save("response.mp3")
        with open("response.mp3", "rb") as audio_file:
            st.session_state.audio = audio_file.read()