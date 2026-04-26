from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import chat, upload, conversations
from app.core.exceptions import DomainError

app = FastAPI()


@app.exception_handler(DomainError)
def domain_error_handler(_request: Request, exc: DomainError):
    return JSONResponse(status_code=exc.status_code, content={"detail": str(exc)})


app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(conversations.router)