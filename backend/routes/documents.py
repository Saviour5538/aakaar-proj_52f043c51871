from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from database.models import Document
from database.config import get_db
from backend.services.auth_service import get_current_user

router = APIRouter(prefix="/documents")

class DocumentResponse(BaseModel):
    id: str
    filename: str
    status: str

    class Config:
        orm_mode = True

@router.get("/", response_model=List[DocumentResponse], operation_id="listDocuments")
async def list_documents(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user["id"]
        documents = db.query(Document).filter(Document.user_id == user_id).all()
        return documents
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve documents"
        )