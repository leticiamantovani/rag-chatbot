from fastapi import APIRouter
from app.services.upload_service import upload_pdf_service
from app.schema.upload import UploadResponse
from fastapi import File, UploadFile, Form
router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(collection_name: str = Form(...),
                     file: UploadFile = File(...)):
    return await upload_pdf_service(collection_name, file)