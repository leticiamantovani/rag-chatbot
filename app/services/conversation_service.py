from app.schema.conversations import ConversationCreate
from app.db.models.conversations import Conversation
from app.db.models.messages import Message
from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID


def create_conversation(db: Session, payload: ConversationCreate) -> Conversation:
    conversation = Conversation()

    db.add(conversation)
    db.flush()
    db.add(Message(conversation_id=conversation.id, content=payload.message, role="user"))
    db.commit()
    db.refresh(conversation)
    return conversation


def get_conversation(db: Session, conversation_id: UUID) -> Conversation:
    conversation = db.get(Conversation, str(conversation_id))
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation
