import asyncio
import io

from fastapi import UploadFile
from pypdf import PdfReader

from app.core.config import get_vector_store
from app.core.dependencies import create_chunks, create_embeddings
from app.schema.upload import UploadResponse


async def upload_pdf_service(collection_name: str, file: UploadFile) -> UploadResponse:
    content = await file.read()

    reader = PdfReader(io.BytesIO(content))
    text = "\n".join(page.extract_text() for page in reader.pages)

    embeddings = create_embeddings()
    chunks = create_chunks(text)

    vector_store = get_vector_store(embeddings, collection_name)
    await asyncio.to_thread(vector_store.create_collection)
    await asyncio.to_thread(vector_store.add_documents, chunks)

    return UploadResponse(message="PDF uploaded successfully")
