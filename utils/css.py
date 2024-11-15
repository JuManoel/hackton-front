import streamlit as st

def inyeccion_css():
    # CSS personalizado para ocultar los controles del video
    custom_css = """
    <style>
        video::-webkit-media-controls {
            display: none !important;
        }
        video {
            pointer-events: none;
        }
    </style>
    """

    # Inyectar el CSS en la aplicación Streamlit
    st.markdown(custom_css, unsafe_allow_html=True)