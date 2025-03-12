from fastapi import APIRouter, HTTPException,Request


from model.Message import FeedbackUpdate
from useCases.chatUseCase import sendMessage
from useCases.feedbackUseCase import give_feedback

router = APIRouter()
@router.post("/chat")
async def chat_endpoint(message: str):
    return sendMessage(message)


@router.patch("/messages/{message_id}/feedback")
def update_feedback(message_id: int, feedback: FeedbackUpdate):
    give_feedback(message_id, feedback)

@router.get("/")
async def root():
    return {"message": "Hello World"}
