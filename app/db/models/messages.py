from sqlalchemy import Column, String, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, server_default=func.now())
    content = Column(Text, nullable=False)
    role = Column(String, nullable=False)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False, index=True)
    conversation = relationship("Conversation", back_populates="messages")