# components/chat.py
import streamlit as st

def render_chat_messages():
    """Renderiza el historial de mensajes en la interfaz de chat."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
