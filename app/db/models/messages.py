from sqlalchemy import Column, String, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, server_default=func.now())
    content = Column(Text, nullable=False)
    role = Column(String, nullable=False)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False, index=True)
    conversation = relationship("Conversation", back_populates="message")