from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.core.config import get_vector_store
from langchain_ollama import OllamaEmbeddings
from langchain.chat_models import init_chat_model

def create_vector_store(chunks, embeddings, collection_name):
    vector_store = get_vector_store(embeddings, collection_name)
    vector_store.create_collection()
    vector_store.add_documents(chunks)
    return vector_store

def semantic_search(question, embeddings, collection_name):
    question_embedding = embeddings.embed_query(question)
    vector_store = get_vector_store(embeddings, collection_name)
    results = vector_store.similarity_search_by_vector(
        question_embedding,
        k=2,
    )
    return results

def create_chunks(pdf_text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_text(pdf_text)
    return [Document(page_content=t) for t in texts]

def create_embeddings():
    return OllamaEmbeddings(model="nomic-embed-text")

def create_model():
    return init_chat_model("ollama:llama3.1")