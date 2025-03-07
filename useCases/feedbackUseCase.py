from fastapi import HTTPException

from model.Message import FeedbackUpdate
from repository.messagesRepository import MessageRepository

def give_feedback(message_id: int, feedback: FeedbackUpdate):
    try:
        updated_message = MessageRepository.update_feedback(message_id, feedback)
        return updated_message
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
