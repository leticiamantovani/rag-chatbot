from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, server_default=func.now())
    messages = relationship("Message", back_populates="conversation",cascade="all, delete-orphan")