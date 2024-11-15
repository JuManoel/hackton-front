import streamlit as st
from services import backend_service

def end_call(id):
    st.session_state.analysis = backend_service.end_talk(id)

    st.session_state.messages.append({"role": "assistant", "content": "La conversación ha terminado. ¡Gracias por su tiempo!"})