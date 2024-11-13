import streamlit as st
from services import groqService

st.title("Asistente virtual")

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

col1, col2, col3 = st.columns([1,2,1])

with col1:
    audio_value = st.audio_input("Comienza a hablar")
with col2:
    # Mostrar mensajes de chat desde el historial
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Procesar entrada de audio si se ha grabado algo
    if audio_value:
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

with col3:
    st.markdown('espacio para video')
