from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.core.dependencies import get_chat_service, get_conversation_service
from app.schema.chat import ChatRequest
from app.services.chat_service import ChatService
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_class=StreamingResponse)
async def get_answer(
    request: ChatRequest,
    conversation_id: UUID | None = None,
    chat_service: ChatService = Depends(get_chat_service),
    conversation_service: ConversationService = Depends(get_conversation_service),
):
    conversation = await conversation_service.resolve(conversation_id)
    stream = await chat_service.stream_answer(
        conversation, request.question, request.collection_name
    )
    return StreamingResponse(
        stream,
        media_type="text/plain",
        headers={"X-Conversation-ID": str(conversation.id)},
    )
