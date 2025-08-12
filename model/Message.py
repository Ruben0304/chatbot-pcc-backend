from pydantic import BaseModel
from typing import Optional

class MessageBase(BaseModel):
    question: str
    answer: str

class MessageCreate(MessageBase):
    pass  # No necesita campos adicionales para la creación

class ChatRequest(BaseModel):
    message: str

class FeedbackUpdate(BaseModel):
    feedback: Optional[str] = None
    feedback_type: Optional[str] = None

class Message(MessageBase):
    id: int
    feedback: Optional[str]
    feedback_type: Optional[str]

    class Config:
        from_attributes = True  # Cambia orm_mode a from_attributes