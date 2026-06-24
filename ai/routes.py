from fastapi import APIRouter, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import os
import shutil
from ai.ingest import ingest_document
from ai.rag import answer_question
from backend.services.auth import get_current_user
from database.config import get_db

router = APIRouter(prefix='/api/ai')

# Pydantic models for request and response validation
class QueryRequest(BaseModel):
    query: str
    session_id: str
    user_id: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@router.post("/ingest", operation_id="ingestDocuments")
async def ingest_documents(
    file: UploadFile,
    session_id: str = Form(...),
    user_id: str = Form(...),
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        # Save the uploaded file to a temporary path
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.filename)
        
        with open(temp_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
        
        # Call the ingest_document function
        result = ingest_document(temp_path, session_id, user_id)
        
        # Clean up the temporary file
        os.remove(temp_path)
        
        return JSONResponse(content={"status": "success", "ingested_chunks": result["ingested_chunks"]})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document ingestion failed: {str(e)}")

@router.post("/query", response_model=QueryResponse, operation_id="aiQuery")
async def ai_query(
    request: QueryRequest,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        # Call the answer_question function
        result = answer_question(request.query, request.session_id, request.user_id)
        
        # Extract answer and sources
        answer = result["answer"]
        sources = result["sources"]
        
        return QueryResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")