# components/audio_handler.py
import streamlit as st
from services import groqService

def handle_audio_input(audio_value):
    """Procesa la entrada de audio, genera una transcripción y una respuesta."""
    if audio_value:
        # Transcribir el audio
        prompt = groqService.transcribir_audio(audio_value)

        # Agregar mensaje del usuario al historial de chat
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Mostrar mensaje del usuario en el contenedor de mensajes
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generar una respuesta (aquí solo se devuelve un eco de la entrada del usuario)
        response = f"Echo: {prompt}"

        # Mostrar respuesta del asistente en el contenedor de mensajes
        with st.chat_message("assistant"):
            st.markdown(response)

        # Agregar respuesta del asistente al historial de chat
        st.session_state.messages.append({"role": "assistant", "content": response})
