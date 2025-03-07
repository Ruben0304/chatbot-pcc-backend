from http.client import responses
from typing import Set
from datetime import datetime

from core.political_assistant import get_response
from model.Message import MessageCreate
from repository.messagesRepository import MessageRepository


def sendMessage(question: str) -> dict[str, str | int]:
    # Obtener la respuesta del chatbot
    response = get_response(question)

    # Crear un objeto MessageCreate con la pregunta y la respuesta
    message = MessageCreate(question=question, answer=response)

    # Guardar el mensaje en la base de datos y obtener el ID
    message_id = MessageRepository.create_message(message)

    # Genera un timestamp (por ejemplo, en formato "HH:MM")
    timestamp = datetime.now().strftime("%H:%M")
    # Devolver un diccionario con la respuesta y el ID
    return {
        "response": response,
        "message_id": message_id,
        "timestamp": timestamp
    }