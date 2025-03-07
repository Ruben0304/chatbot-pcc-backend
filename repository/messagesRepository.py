import sqlite3
from datetime import datetime
from model import Message
from model.Message import MessageCreate, FeedbackUpdate

DB_URL = "database/chatbot_pcc.db"


class MessageRepository:
    @staticmethod
    def _get_connection(db_path: str = DB_URL):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Para acceder a las filas como diccionarios
        return conn


    @staticmethod
    def create_message(message) -> int:
     with MessageRepository._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (question, answer) VALUES (?, ?)",
            (message.question, message.answer)
        )
        conn.commit()
        message_id = cursor.lastrowid
        # Devuelve el ID del mensaje insertado en lugar de intentar recuperarlo
        return message_id

    @staticmethod
    def update_feedback(message_id: int, feedback: FeedbackUpdate) -> Message:
        with MessageRepository._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE messages
                SET feedback = ?, feedback_type = ?
                WHERE id = ?
                """,
                (feedback.feedback, feedback.feedback_type, message_id)
            )
            if cursor.rowcount == 0:
                raise ValueError("Message not found")
            return message_id

    @staticmethod
    def get_message(message_id: int) -> Message:
        with MessageRepository._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM messages WHERE id = ?",
                (message_id,)
            )
            row = cursor.fetchone()
            if not row:
                raise ValueError("Message not found")

            return Message
