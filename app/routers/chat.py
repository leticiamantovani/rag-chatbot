from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.services.chat_service import chat_service, resolve_conversation
from app.schema.chat import ChatRequest
from app.core.dependencies import get_db
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_class=StreamingResponse)
def get_answer(request: ChatRequest, db: Session = Depends(get_db), conversation_id: UUID | None = None):
    conversation = resolve_conversation(db, conversation_id)

    response = chat_service(db, conversation, request.question, request.collection_name)

    return StreamingResponse(response, media_type="text/plain", headers={"X-Conversation-ID": str(conversation.id)})