import os
from mistralai import Mistral
import streamlit as st

class MistralChat:
    def __init__(self, modelInfo = { "role": "system",
                      "content":
            "Eres un asistente virtual de una llamada telefonica de un banco llamado Indra Bank. Su funcion es atender el"+
            " siempre con respetas y amabilidad, pero recuerde, su funcion es cobrar y o negociar la deuda. Esta proibdo contar chistes, y responder pregunta"+
            "que no esten relacionadas con el banco. Su principal propocito es negociar la deuda y cobrar"+
            "de los cliente. Sus respuestas solo pueden ser texto, ni emojis y ni markdown."+
            "Sus respuestas deben ser claras, concisas y cortas. maximo 50 palabras"
            
             
                      }):

        self.api_key = st.secrets["MISTRAL_API_KEY"]
        self.modelInfo = modelInfo
        self.client = Mistral(api_key = self.api_key)
        self.model = "mistral-large-latest"

    def __call__(self, mensajes, temp = None):
        historial = []
        cont = 0
        for i in mensajes:
            if(cont % 4 == 0):
                historial.append(self.modelInfo)
            historial.append(i)
            cont += 1
        if not temp:
            chat_response = self.client.chat.complete(
                model = self.model,
                messages = historial)
        else:
            chat_response = self.client.chat.complete(
                model = self.model,
                messages = historial,
                temperature=temp)
        self.full = chat_response
        respuestaAsistente = chat_response.choices[0].message.content
        return respuestaAsistente