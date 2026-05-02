from langchain_postgres import PGVector
from dotenv import load_dotenv
load_dotenv()
import os

def get_vector_store(embeddings, collection_name):
    sync_url = (
        os.getenv("DATABASE_URL", "")
        .replace("postgresql+asyncpg://", "postgresql://", 1)
        .replace("ssl=require", "sslmode=require")
    )
    return PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=sync_url,
    )