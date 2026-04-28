from collections.abc import Iterator
from typing import TypedDict
from uuid import UUID

from langgraph.graph import END, StateGraph
from sqlalchemy.orm import Session

from app.core.config import get_vector_store
from app.core.dependencies import create_embeddings, create_model
from app.db.models import Conversation, Message
from app.repository.message_repository import MessageRepository

embeddings = create_embeddings()
model = create_model()


class RAGState(TypedDict):
    question: str
    collection_name: str
    conversation_id: UUID
    history: list[Message]
    context: str
    answer: str


def _retrieve_docs(state: RAGState) -> dict:
    question_embedding = embeddings.embed_query(state["question"])
    vector_store = get_vector_store(embeddings, state["collection_name"])
    results = vector_store.similarity_search_by_vector(question_embedding, k=2)
    context = "\n\n".join(doc.page_content for doc in results)
    return {"context": context}


def _build_prompt(state: RAGState) -> str:
    history_block = "\n".join(f"{m.role}: {m.content}" for m in state["history"])
    return (
        "Use the context below and the prior conversation to answer the question.\n\n"
        f"Context:\n{state['context']}\n\n"
        f"Conversation so far:\n{history_block}\n\n"
        f"Question: {state['question']}"
    )


def _generate_answer(state: RAGState) -> dict:
    prompt = _build_prompt(state)
    response = model.invoke(prompt)
    return {"answer": response.content}


def _build_graph() -> StateGraph:
    graph = StateGraph(RAGState)

    graph.add_node("retrieve", _retrieve_docs)
    graph.add_node("generate", _generate_answer)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()


rag_graph = _build_graph()


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

        return self._stream(conversation, question, collection_name, history)

    def _stream(
        self,
        conversation: Conversation,
        question: str,
        collection_name: str,
        history: list[Message],
    ) -> Iterator[str]:
        initial_state: RAGState = {
            "question": question,
            "collection_name": collection_name,
            "conversation_id": conversation.id,
            "history": history,
            "context": "",
            "answer": "",
        }

        buffer: list[str] = []
        try:
            for chunk in rag_graph.stream(initial_state):
                if "generate" in chunk:
                    answer = chunk["generate"].get("answer", "")
                    if answer:
                        buffer.append(answer)
                        yield answer
        finally:
            if buffer:
                self.message_repo.add(
                    Message(
                        conversation_id=conversation.id,
                        content="".join(buffer),
                        role="assistant",
                    )
                )
                self.db.commit()
