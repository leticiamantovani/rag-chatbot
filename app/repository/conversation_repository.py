from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Conversation


class ConversationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, conversation_id: UUID) -> Conversation | None:
        return await self.db.get(Conversation, conversation_id)

    def add(self, conversation: Conversation) -> None:
        self.db.add(conversation)
