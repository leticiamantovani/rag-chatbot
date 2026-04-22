from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.chat_service import chat_service
from app.schema.chat import ChatRequest

router = APIRouter()

@router.post("/chat", response_class=StreamingResponse)
def get_answer(request: ChatRequest):
    return StreamingResponse(chat_service(request.question, request.collection_name), media_type="text/plain")