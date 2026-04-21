from fastapi import APIRouter
from app.services.chat_service import chat_service
from app.schema.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def get_answer(request: ChatRequest):
    return ChatResponse(answer=chat_service(request.question, request.collection_name))