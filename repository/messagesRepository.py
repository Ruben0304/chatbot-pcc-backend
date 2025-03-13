from datetime import datetime
from typing import Dict, List, Optional
import os

# Importaciones más básicas para evitar conflictos
import pymongo
from bson.objectid import ObjectId
from model.Message import Message, MessageCreate, FeedbackUpdate

class MessageRepository:
    @staticmethod
    def _get_connection():
        uri = "mongodb+srv://ruben:zixelowe1@personal.yycznyk.mongodb.net/?retryWrites=true&w=majority&appName=personal"

        # Crear cliente sin usar ServerApi para mayor compatibilidad
        client = pymongo.MongoClient(uri)
        db = client['chatbot-pcc']
        return db.messages

    @staticmethod
    def create_message(message: MessageCreate) -> str:
        collection = MessageRepository._get_connection()

        # Crear nuevo mensaje
        new_message = {
            "question": message.question,
            "answer": message.answer,
            "feedback": None,
            "feedback_type": None,
            "created_at": datetime.now()
        }

        # Insertar el mensaje y obtener el ID
        result = collection.insert_one(new_message)
        message_id = str(result.inserted_id)

        return message_id

    @staticmethod
    def update_feedback(message_id: str, feedback: FeedbackUpdate) -> str:
        collection = MessageRepository._get_connection()

        # Convertir string ID a ObjectId
        try:
            object_id = ObjectId(message_id)
        except:
            raise ValueError("Invalid message ID format")

        # Actualizar el mensaje
        result = collection.update_one(
            {"_id": object_id},
            {"$set": {
                "feedback": feedback.feedback,
                "feedback_type": feedback.feedback_type
            }}
        )

        if result.matched_count == 0:
            raise ValueError("Message not found")

        return message_id

    @staticmethod
    def get_message(message_id: str) -> Message:
        collection = MessageRepository._get_connection()

        # Convertir string ID a ObjectId
        try:
            object_id = ObjectId(message_id)
        except:
            raise ValueError("Invalid message ID format")

        # Buscar el mensaje
        message_data = collection.find_one({"_id": object_id})

        if not message_data:
            raise ValueError("Message not found")

        # Convertir el documento de MongoDB a un objeto Message
        created_at = message_data["created_at"]
        if isinstance(created_at, datetime):
            created_at = created_at.isoformat()

        return Message(
            id=str(message_data["_id"]),
            question=message_data["question"],
            answer=message_data["answer"],
            feedback=message_data.get("feedback"),
            feedback_type=message_data.get("feedback_type"),
            created_at=created_at
        )

    @staticmethod
    def get_all_messages() -> List[Message]:
        collection = MessageRepository._get_connection()

        # Obtener todos los mensajes
        messages_data = collection.find()

        # Convertir documentos a objetos Message
        messages = []
        for message_data in messages_data:
            created_at = message_data["created_at"]
            if isinstance(created_at, datetime):
                created_at = created_at.isoformat()

            messages.append(Message(
                id=str(message_data["_id"]),
                question=message_data["question"],
                answer=message_data["answer"],
                feedback=message_data.get("feedback"),
                feedback_type=message_data.get("feedback_type"),
                created_at=created_at
            ))

        return messages

    @staticmethod
    def delete_message(message_id: str) -> bool:
        collection = MessageRepository._get_connection()

        # Convertir string ID a ObjectId
        try:
            object_id = ObjectId(message_id)
        except:
            raise ValueError("Invalid message ID format")

        # Eliminar el mensaje
        result = collection.delete_one({"_id": object_id})

        if result.deleted_count == 0:
            raise ValueError("Message not found")

        return True