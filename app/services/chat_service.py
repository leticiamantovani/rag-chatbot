from app.core.config import get_vector_store
from app.core.dependencies import create_embeddings, create_model
from sqlalchemy.orm import Session
from app.db.models.messages import Message
from app.db.models.conversations import Conversation
from fastapi import HTTPException
from uuid import UUID

embeddings = create_embeddings()
model = create_model()


def chat_service(db: Session, conversation: Conversation, question: str, collection_name: str):
    db.add(Message(conversation_id=conversation.id, content=question, role="user"))
    db.commit()

    context = get_context(collection_name, question)
    return generate_response(db, conversation, context, question)


def generate_response(db: Session, conversation: Conversation, context: str, question: str):
    buffer = []
    prompt = f"Use the context below to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}"
    try: 
        for chunk in model.stream(prompt):
            buffer.append(chunk.content)
            yield chunk.content
    finally:
        db.add(Message(conversation_id=conversation.id, content="".join(buffer), role="assistant"))
        db.commit()


def get_context(collection_name: str, question: str):
    question_embedding = embeddings.embed_query(question)
    vector_store = get_vector_store(embeddings, collection_name)
    results = vector_store.similarity_search_by_vector(
        question_embedding,
        k=2,
    )
    context = "\n\n".join([doc.page_content for doc in results])
    return context

def resolve_conversation(db: Session, conversation_id: UUID | None = None) -> Conversation:
    if conversation_id:
        conversation = db.get(Conversation, conversation_id)
        if not conversation:
            raise
        return conversation
    conversation = Conversation()
    db.add(conversation)
    db.flush()
    return conversation