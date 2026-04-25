from fastapi import APIRouter, status, Depends
from app.schema.conversations import ConversationCreate, ConversationResponse
from app.services import conversation_service
from app.core.dependencies import get_db
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ConversationResponse)
def create_conversation(request: ConversationCreate, db: Session = Depends(get_db)):
    return conversation_service.create_conversation(db, request)

@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(conversation_id: UUID, db: Session = Depends(get_db)):
    return conversation_service.get_conversation(db, conversation_id)
