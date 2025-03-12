import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from model.Message import Message, MessageCreate, FeedbackUpdate

JSON_FILE = "database/chatbot_pcc.json"

class MessageRepository:
    @staticmethod
    def _get_data() -> Dict:
        # Crear el directorio si no existe
        os.makedirs(os.path.dirname(JSON_FILE), exist_ok=True)

        # Si el archivo no existe, crear uno vacío con estructura inicial
        if not os.path.exists(JSON_FILE):
            with open(JSON_FILE, 'w') as f:
                json.dump({"messages": [], "last_id": 0}, f)

        # Leer datos del archivo
        with open(JSON_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # Si el archivo está corrupto, crear uno nuevo
                data = {"messages": [], "last_id": 0}
                with open(JSON_FILE, 'w') as f:
                    json.dump(data, f)
                return data

    @staticmethod
    def _save_data(data: Dict) -> None:
        with open(JSON_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def create_message(message: MessageCreate) -> int:
        data = MessageRepository._get_data()

        # Incrementar el último ID
        message_id = data["last_id"] + 1
        data["last_id"] = message_id

        # Crear nuevo mensaje
        new_message = {
            "id": message_id,
            "question": message.question,
            "answer": message.answer,
            "feedback": None,
            "feedback_type": None,
            "created_at": datetime.now().isoformat()
        }

        # Agregar el mensaje a la lista
        data["messages"].append(new_message)

        # Guardar los cambios
        MessageRepository._save_data(data)

        return message_id

    @staticmethod
    def update_feedback(message_id: int, feedback: FeedbackUpdate) -> int:
        data = MessageRepository._get_data()

        # Buscar el mensaje por ID
        found = False
        for message in data["messages"]:
            if message["id"] == message_id:
                message["feedback"] = feedback.feedback
                message["feedback_type"] = feedback.feedback_type
                found = True
                break

        if not found:
            raise ValueError("Message not found")

        # Guardar los cambios
        MessageRepository._save_data(data)

        return message_id

    @staticmethod
    def get_message(message_id: int) -> Message:
        data = MessageRepository._get_data()

        # Buscar el mensaje por ID
        for message in data["messages"]:
            if message["id"] == message_id:
                # Convertir el diccionario a un objeto Message
                return Message(
                    id=message["id"],
                    question=message["question"],
                    answer=message["answer"],
                    feedback=message["feedback"],
                    feedback_type=message["feedback_type"],
                    created_at=message["created_at"]
                )

        raise ValueError("Message not found")

    @staticmethod
    def get_all_messages() -> List[Message]:
        data = MessageRepository._get_data()

        # Convertir todos los mensajes a objetos Message
        messages = []
        for message_data in data["messages"]:
            messages.append(Message(
                id=message_data["id"],
                question=message_data["question"],
                answer=message_data["answer"],
                feedback=message_data["feedback"],
                feedback_type=message_data["feedback_type"],
                created_at=message_data["created_at"]
            ))

        return messages