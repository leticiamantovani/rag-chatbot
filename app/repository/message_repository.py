from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Message


class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_conversation(self, conversation_id: UUID) -> list[Message]:
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )
        return list(result.scalars())

    def add(self, message: Message) -> None:
        self.db.add(message)
