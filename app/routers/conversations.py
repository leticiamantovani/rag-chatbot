from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_conversation_service
from app.schema.conversations import ConversationResponse, MessageResponse
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ConversationResponse)
def create_conversation(
    service: ConversationService = Depends(get_conversation_service),
):
    return service.create()


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: UUID,
    service: ConversationService = Depends(get_conversation_service),
):
    return service.get(conversation_id)


@router.get("/{conversation_id}/messages", response_model=list[MessageResponse])
def list_messages(
    conversation_id: UUID,
    service: ConversationService = Depends(get_conversation_service),
):
    return service.list_messages(conversation_id)
