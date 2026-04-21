from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector
from langchain.chat_models import init_chat_model
from app.core.config import get_vector_store
from app.core.dependencies import create_embeddings, create_model

embeddings = create_embeddings()
model = create_model()


def chat_service(question: str, collection_name: str):
    question_embedding = embeddings.embed_query(question)
    vector_store = get_vector_store(embeddings, collection_name)

    results = vector_store.similarity_search_by_vector(
        question_embedding,
        k=2,
    )

    context = "\n\n".join([doc.page_content for doc in results])
    prompt = f"Use the context below to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}"

    result = model.invoke(prompt)
    return result.content