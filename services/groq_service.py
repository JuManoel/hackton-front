import os
from groq import Groq
import streamlit as st

api_key_groq = st.secrets["API_KEY_GROQ"]

client = Groq(api_key=api_key_groq)

def transcribir_audio(audio_value):
    try:
        # Configura la solicitud de transcripción
        transcripcion = client.audio.transcriptions.create(
            file = ("audio.wav", audio_value),  # Nombre y contenido del archivo
            model = "whisper-large-v3",
            prompt="el audio es de una persona normal trabajando",
            response_format="text",
            language="es"
        )
        return transcripcion
    except Exception as e:
        st.error(f"Ocurrió un error: {str(e)}")
        return None