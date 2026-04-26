from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import relationship
from app.db.session import Base
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, server_default=func.now())
    messages = relationship("Message", back_populates="conversation",cascade="all, delete-orphan")