from fastapi import FastAPI
from app.routers import chat, upload, conversations

app = FastAPI()

app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(conversations.router)