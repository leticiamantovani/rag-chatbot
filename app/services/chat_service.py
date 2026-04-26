from collections.abc import Iterator

from sqlalchemy.orm import Session

from app.core.config import get_vector_store
from app.core.dependencies import create_embeddings, create_model
from app.db.models import Conversation, Message
from app.repository.message_repository import MessageRepository

embeddings = create_embeddings()
model = create_model()


class ChatService:
    def __init__(self, db: Session, message_repo: MessageRepository):
        self.db = db
        self.message_repo = message_repo

    def stream_answer(
        self,
        conversation: Conversation,
        question: str,
        collection_name: str,
    ) -> Iterator[str]:
        history = self.message_repo.list_by_conversation(conversation.id)

        self.message_repo.add(
            Message(conversation_id=conversation.id, content=question, role="user")
        )
        self.db.commit()

        context = self._retrieve_context(collection_name, question)
        prompt = self._build_prompt(history, context, question)
        return self._stream(conversation, prompt)

    def _stream(self, conversation: Conversation, prompt: str) -> Iterator[str]:
        buffer: list[str] = []
        try:
            for chunk in model.stream(prompt):
                buffer.append(chunk.content)
                yield chunk.content
        finally:
            self.message_repo.add(
                Message(
                    conversation_id=conversation.id,
                    content="".join(buffer),
                    role="assistant",
                )
            )
            self.db.commit()

    @staticmethod
    def _retrieve_context(collection_name: str, question: str) -> str:
        question_embedding = embeddings.embed_query(question)
        vector_store = get_vector_store(embeddings, collection_name)
        results = vector_store.similarity_search_by_vector(question_embedding, k=2)
        return "\n\n".join(doc.page_content for doc in results)

    @staticmethod
    def _build_prompt(history: list[Message], context: str, question: str) -> str:
        history_block = "\n".join(f"{m.role}: {m.content}" for m in history)
        return (
            "Use the context below and the prior conversation to answer the question.\n\n"
            f"Context:\n{context}\n\n"
            f"Conversation so far:\n{history_block}\n\n"
            f"Question: {question}"
        )
