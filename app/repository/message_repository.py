from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Message


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_conversation(self, conversation_id: UUID) -> list[Message]:
        return list(
            self.db.scalars(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at)
            )
        )

    def add(self, message: Message) -> None:
        self.db.add(message)
