from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ConversationNotFoundError
from app.db.models import Conversation, Message
from app.repository.conversation_repository import ConversationRepository
from app.repository.message_repository import MessageRepository


class ConversationService:
    def __init__(
        self,
        db: Session,
        conversation_repo: ConversationRepository,
        message_repo: MessageRepository,
    ):
        self.db = db
        self.conversation_repo = conversation_repo
        self.message_repo = message_repo

    def get(self, conversation_id: UUID) -> Conversation:
        conversation = self.conversation_repo.get(conversation_id)
        if not conversation:
            raise ConversationNotFoundError(f"Conversation not found: {conversation_id}")
        return conversation

    def create(self) -> Conversation:
        conversation = Conversation()
        self.conversation_repo.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def resolve(self, conversation_id: UUID | None) -> Conversation:
        """Get an existing conversation or create a new one (uncommitted)."""
        if conversation_id:
            return self.get(conversation_id)
        conversation = Conversation()
        self.conversation_repo.add(conversation)
        self.db.flush()
        return conversation

    def list_messages(self, conversation_id: UUID) -> list[Message]:
        self.get(conversation_id)
        return self.message_repo.list_by_conversation(conversation_id)
