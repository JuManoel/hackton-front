import os
from groq import Groq
import streamlit as st
import requests

def generar_video(contenido):
            try:
                api_key_did = st.secrets["API_KEY_DID"]
                url = "https://api.d-id.com/talks"
                headers = {
                    "Authorization": f"Basic {api_key_did}",
                    "Content-Type": "application/json"
                }
                data = {
                    "source_url": "https://create-images-results.d-id.com/api_docs/assets/noelle.jpeg",
                    "script": {
                        "type": "text",
                        "input": contenido,
                        "provider": {
                            "type": "microsoft",
                            "voice_id": "en-US-JennyNeural"
                        }
                    },
                    "config": {
                        "fluent": "true"
                    }
                }
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                id = response.json().get("id")
                video = requests.get(f"{url}/{id}", headers=headers)
                url_video = video.json().get("result_url")
                return url_video
            except requests.exceptions.RequestException as e:
                st.error(f"Ocurrió un error: {str(e)}")
                return None