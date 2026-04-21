from pydantic import BaseModel

class ChatResponse(BaseModel):
    answer: str

class ChatRequest(BaseModel):
    question: str
    collection_name: str