import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

client = Groq(api_key=os.getenv("API_KEY_GROQ"))

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