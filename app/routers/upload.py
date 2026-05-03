from fastapi import APIRouter, Depends, File, UploadFile

from app.core.dependencies import get_current_user_id
from app.schema.upload import UploadResponse
from app.services.upload_service import upload_pdf_service

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
):
    return await upload_pdf_service(f"user_{user_id}", file)