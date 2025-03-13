from datetime import datetime
from typing import Dict, List, Optional
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from model.Message import Message, MessageCreate, FeedbackUpdate

class MessageRepository:
    @staticmethod
    def _get_connection():
        uri = "mongodb+srv://ruben:Zixelowe1@personal.yycznyk.mongodb.net/?retryWrites=true&w=majority&appName=personal"
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client['chatbot_pcc']
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

        # Convertir string ID a ObjectId para MongoDB
        object_id = ObjectId(message_id)

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

        # Convertir string ID a ObjectId para MongoDB
        object_id = ObjectId(message_id)

        # Buscar el mensaje
        message_data = collection.find_one({"_id": object_id})

        if not message_data:
            raise ValueError("Message not found")

        # Convertir el documento de MongoDB a un objeto Message
        return Message(
            id=str(message_data["_id"]),
            question=message_data["question"],
            answer=message_data["answer"],
            feedback=message_data.get("feedback"),
            feedback_type=message_data.get("feedback_type"),
            created_at=message_data["created_at"].isoformat() if isinstance(message_data["created_at"], datetime) else message_data["created_at"]
        )

    @staticmethod
    def get_all_messages() -> List[Message]:
        collection = MessageRepository._get_connection()

        # Obtener todos los mensajes
        messages_data = collection.find()

        # Convertir documentos a objetos Message
        messages = []
        for message_data in messages_data:
            messages.append(Message(
                id=str(message_data["_id"]),
                question=message_data["question"],
                answer=message_data["answer"],
                feedback=message_data.get("feedback"),
                feedback_type=message_data.get("feedback_type"),
                created_at=message_data["created_at"].isoformat() if isinstance(message_data["created_at"], datetime) else message_data["created_at"]
            ))

        return messages

    @staticmethod
    def delete_message(message_id: str) -> bool:
        collection = MessageRepository._get_connection()

        # Convertir string ID a ObjectId para MongoDB
        object_id = ObjectId(message_id)

        # Eliminar el mensaje
        result = collection.delete_one({"_id": object_id})

        if result.deleted_count == 0:
            raise ValueError("Message not found")

        return True