from sqlalchemy import Column, String, JSONB, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid


class LangchainPgEmbedding(Base):
    __tablename__ = "langchain_pg_embeddings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    collection_id = Column(String, nullable=False)
    embedding = Column(JSONB, nullable=False)
    document = Column(String, nullable=False)
    cmetadata = Column(JSONB, nullable=False)
    langchain_pg_collection_id = Column(String, ForeignKey("langchain_pg_collections.id"), nullable=False)
    langchain_pg_collection = relationship("LangchainPgCollection", back_populates="langchain_pg_embeddings")