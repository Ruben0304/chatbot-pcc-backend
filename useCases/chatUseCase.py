from http.client import responses
from typing import Set
from datetime import datetime
import random
import string
import asyncio
import threading

from core.political_assistant import get_response
from model.Message import MessageCreate
from repository.messagesRepository import MessageRepository


def generate_random_id(length=10):
    """Generate a random alphanumeric ID of specified length"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def save_message_async(message):
    """Save message to database asynchronously"""
    try:
        message_id = MessageRepository.create_message(message)
        return message_id
    except Exception as e:
        print(f"Error saving message to database: {e}")
        return None


def sendMessage(question: str) -> dict[str, str | int]:
    # Obtener la respuesta del chatbot
    response = get_response(question)

    # Crear un objeto MessageCreate con la pregunta y la respuesta
    message = MessageCreate(question=question, answer=response)

    # Generate timestamp
    timestamp = datetime.now().strftime("%H:%M")
    
    # Generate a random ID in case DB storage fails
    message_id = generate_random_id()
    
    # Start a thread to save the message asynchronously
    threading.Thread(
        target=lambda: save_message_async(message),
        daemon=True
    ).start()

    # Devolver un diccionario con la respuesta y el ID
    return {
        "response": response,
        "message_id": message_id,
        "timestamp": timestamp
    }