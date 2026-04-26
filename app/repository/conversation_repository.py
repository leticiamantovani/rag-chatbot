from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models import Conversation


class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, conversation_id: UUID) -> Conversation | None:
        return self.db.get(Conversation, conversation_id)

    def add(self, conversation: Conversation) -> None:
        self.db.add(conversation)
