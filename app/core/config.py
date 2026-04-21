from langchain_postgres import PGVector
from dotenv import load_dotenv
load_dotenv()
import os

def get_vector_store(embeddings, collection_name):
    return PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=os.getenv("DATABASE_URL")
    )