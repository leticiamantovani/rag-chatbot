from sqlalchemy import Column, String, UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid

class LangchainPgCollection(Base):
    __tablename__ = "langchain_pg_collections"

    uuid = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    metadata = Column(JSONB, nullable=False)
    langchain_pg_embeddings = relationship("LangchainPgEmbedding", back_populates="langchain_pg_collection")