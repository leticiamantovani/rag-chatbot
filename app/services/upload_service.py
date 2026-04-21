from pypdf import PdfReader
from app.core.dependencies import create_chunks, create_vector_store, create_embeddings
from app.schema.upload import UploadResponse
from fastapi import UploadFile
import io

async def upload_pdf_service(collection_name: str, file: UploadFile):
    content = await file.read()
    reader = PdfReader(io.BytesIO(content))
    text = "\n".join(page.extract_text() for page in reader.pages)
    chunks = create_chunks(text)
    embeddings = create_embeddings()
    create_vector_store(chunks, embeddings, collection_name)
    return UploadResponse(message="PDF uploaded successfully")



