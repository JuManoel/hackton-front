from datetime import datetime
from backend.services.callService import CallService
from backend.services.customerService import CustomerService
from backend.services.accountService import AccountService
from backend.models.message import Message
from backend.models.call import Call
from backend.models.customer import Customer
from backend.apis.mistral import MistralChat
import re
import json

chat = MistralChat()
CallService = CallService()
CustomerService = CustomerService()
AccountService = AccountService()
hasLogin = False
isLoged = False
customer = None
def startCall():
    """
    Esta API se encarga de iniciar una llamada, generando un mensaje de bienvenida al usuario.
Returns:
    Response: mensaje de bienvenida al usuario, con un codigo de estado 201 (Created).
"""
    new_call = Call()
    wellcome = chat([{
        "role":"system",
        "content":"Quiero que genere un mensage de bienvenida al usuario"+
        "el mensaje tiene que ser corto y amigable, y debe incluir una pregunta"+
        "para que el usuario responda, con su cedula o documento"+
        "no puede tener emojis ni markdown, solo texto"+
        "Avisa que la llamada esta siendo grabada y monitoreada segun la RGPD"
    }])
    new_call.messages.append(Message(role="system", content=wellcome))
    call_id = CallService.createCall(new_call)

    return {"message": "ok", "content": wellcome, "newCallId": str(call_id.inserted_id)}

#Metodo para conseguir los mensajes de los usuarios
def analizeMessage(call_id):
    """
    Analiza los mensajes de una llamada y devuelve análisis de emociones, porcentaje de éxito y tokens.
    Args:
        callId (str): ID de la llamada.
    Returns:
        Response: JSON con análisis de emociones, porcentaje de éxito, tokens y total de mensajes.
    """
    if not call_id:
        return {"error": "No callId provided"}

    # Obtener la llamada usando el callId
    call = CallService.getCall(call_id)
    if not call:
        return {"error": "Call not found"}

    # Convertir los mensajes a un formato adecuado para el modelo
    messages = [{"role": msg.role, "content": msg.content} for msg in call.messages]
    # Asegurarse de que el último mensaje tenga el rol correcto
    if messages and messages[-1]["role"] == "assistant":
        messages[-1]["role"] = "user"

    # Construir el prompt de análisis
    analysis_prompt = MistralChat({
        "role": "system",
        "content": """
Analiza los mensajes de la conversación proporcionada. Responde exclusivamente con un JSON estructurado según las instrucciones:
1. *Desglose de emociones*:
    - Analiza cada mensaje del cliente (role: user) y clasifícalo con:
      - 1 para positivo,
      - 0 para neutro,
      - -1 para negativo.
    - Devuelve un desglose en forma de lista, donde cada posición representa un mensaje.

2. *Porcentaje de éxito*:
    - Evalúa el éxito de la conversación según:
      - La dificultad de persuadir al cliente (más difícil = menor éxito).
      - Las posibles pérdidas económicas para el banco.
    - Devuelve un porcentaje del 0 al 100.
    Se base en eses parametros:
Criterios para utilizar para calcular el índice:
    Flexibilidad del usuario,
    Propuestas ofrecidas por el bot,
    Ajustes durante la negociación,
    Rapidez en llegar a un acuerdo,
    Claridad del acuerdo final

Responde únicamente en este formato:
{
    "emotionAnalysis": [1, 0, -1, ...],
    "successRate": 85,
    "totalMessages": 15
}
"""
    })

    # Generar análisis usando el modelo
    print(messages)
    print(analysis_prompt)
    analysis_response = analysis_prompt(messages)
    print(analysis_response)
    tokens = analysis_prompt.full.usage.total_tokens
    precio = 0.045*(tokens/1000)
    # Convertir la respuesta del modelo en JSON
    match = re.search(r'{.*?}', analysis_response, re.DOTALL)
    if match:
        json_content = match.group(0)  # Extraer el JSON
        try:
            # Validar y convertir el JSON a un diccionario
            analisis = json.loads(json_content)
        except json.JSONDecodeError:
            print("Error: El contenido extraído no es un JSON válido.")
            return None
    else:
        print("Error: No se encontró un JSON en la respuesta.")
        return None

    # Respuesta final
    return {"callId": call_id, "analysis": analisis, "tokens": tokens, "precio": precio}

def callTalking(data):
    ''' Esta API se encarga de recibir los mensajes del usuario y responderlos
    Returns:
    Response: mensaje de respuesta al usuario, con un codigo de estado 200 (OK).
    '''
    global hasLogin
    global isLoged
    global customer
    global chat
    if not data or not data.get("callId") or not data.get("content"):
        return {"error": "Invalid data"}
    
    # Obtener la llamada actual usando el callId
    call = CallService.getCall(data.get("callId"))
    if not call:
        return {"error": "Call not found"}
    # Crear el mensaje del usuario
    message = Message(role="user",content=data.get("content"))
    call.messages.append(message)
    CallService.addMessage(data.get("callId"), message)
    if not isLoged:
        customer_data = getUserData(call.messages)
        customer_data_base = CustomerService.getCustomer(customer_data.get("customerId"))
        print(customer_data_base)
        print(customer_data.get("customerId"))
        if(not customer_data_base):
            if(not customer_data.get("customerId")):
                print("no se encontro")
                answer = chat([{"role":"system","conten":"Pide al usuario que ingrese su cedula, por poder"+
                                "proseguir con la acesoria"}], temp=0.5)
                chatMessage = Message(role="assistant", content=answer)
                call.messages.append(chatMessage)
                CallService.addMessage(data.get("callId"), chatMessage)
            else:
                print("no existe")
                answer = chat([{"role":"system","content":"El usuario no existe, diga un mensaje de despedida"}], temp=0.3)
                chatMessage = Message(role="assistant", content=answer)
                call.messages.append(chatMessage)
                CallService.addMessage(data.get("callId"), chatMessage)
        else:
            print("empiezo a negociar")
            isLoged = True
            account = AccountService.getAccount(customer_data_base.get("customerId"))
            print(account)
            answer = chat([{"role":"system", 
                    "content":"Haga un cordial saludo de la empresa Indra Bank para la persona: "+
                    customer_data_base.get("name")+
                    f"considere ese historial de la deuda que el tiene {account}"+
                    "e intente renegociar la deuda"+
                    "tenga en cuenta el total de la deuda y el que tanto tardo en pagar la deuda"+
                    "no hagas despedidas y siempre muestre el valor de la deuda"}], temp = 0.2)
            chatMessage = Message(role="assistant", content=answer)
            call.messages.append(chatMessage)
            CallService.addMessage(data.get("callId"), chatMessage)
    else:
        print("charlando")
        answer = chat([message.toDictChat() for message in call.messages], temp = 0.5)
        chatMessage = Message(role="assistant", content=answer)
        call.messages.append(chatMessage)
        CallService.addMessage(data.get("callId"), chatMessage)
    return {"message": "ok", "content": answer, "close":False}

def getAllCall(callId):
    call = CallService.getCall(callId)
    return call

def getUserData(messages):
    """
    Esta función se encarga de extraer la cédula del usuario y otros datos relevantes.
    """
    if not hasLogin:
        # Solicitud al modelo Mistral
        getDataChat = MistralChat({
            "role": "system",
            "content": """
Quiero que respondas exclusivamente con un JSON válido. Solo responde con un string que 
contenga el JSON, sin usar formato Markdown, etiquetas adicionales, o texto explicativo. 
Aquí está el contexto:
Entrada:
Hola, mi nombre es Juan Manoel, tengo 20, mi teléfono es 3004121952 y mi identidad es 1055761669
Salida esperada:
{"customerId": "1055761669" o None}
"""
        })
        
        # Obtener la respuesta del modelo
        patrones = getDataChat([mensaje.toDict() for mensaje in messages])
        
        # Expresión regular para extraer solo el contenido JSON
        match = re.search(r'{.*?}', patrones, re.DOTALL)
        if match:
            json_content = match.group(0)  # Extraer el JSON
            try:
                # Validar y convertir el JSON a un diccionario
                user_data = json.loads(json_content)
                print(user_data)
                return user_data
            except json.JSONDecodeError:
                print("Error: El contenido extraído no es un JSON válido.")
                return None
        else:
            print("Error: No se encontró un JSON en la respuesta.")
            return None
    return False

