import os
from typing import List, Dict, Optional
from pypdf import PdfReader
from docx import Document
import pandas as pd
from .embeddings import get_embedding
from .vector_store import VectorStore

def chunk(document: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """
    Chunk the document text using overlapping strategy.
    """
    chunks = []
    start = 0
    while start < len(document):
        end = min(start + chunk_size, len(document))
        chunks.append(document[start:end])
        start += chunk_size - chunk_overlap
    return chunks

def ingest_document(file_path: str, session_id: str, user_id: str) -> Dict[str, int]:
    """
    Ingest a document by reading its content, chunking, embedding, and storing in the vector store.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_extension = os.path.splitext(file_path)[1].lower()
    vector_store = VectorStore()
    chunks_count = 0

    if file_extension == ".pdf":
        reader = PdfReader(file_path)
        text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())
        chunks = chunk(text)
        embeddings = get_embedding(chunks)
        for i, embedding in enumerate(embeddings):
            metadata = {
                "session_id": session_id,
                "user_id": user_id,
                "source": file_path,
                "sheet_name": None,
                "row_range": None,
                "chunk_text": chunks[i],
            }
            vector_store.upsert(f"{session_id}_{user_id}_{i}", embedding, metadata)
        chunks_count = len(chunks)

    elif file_extension == ".docx":
        doc = Document(file_path)
        text = " ".join(paragraph.text for paragraph in doc.paragraphs)
        chunks = chunk(text)
        embeddings = get_embedding(chunks)
        for i, embedding in enumerate(embeddings):
            metadata = {
                "session_id": session_id,
                "user_id": user_id,
                "source": file_path,
                "sheet_name": None,
                "row_range": None,
                "chunk_text": chunks[i],
            }
            vector_store.upsert(f"{session_id}_{user_id}_{i}", embedding, metadata)
        chunks_count = len(chunks)

    elif file_extension in [".xls", ".xlsx"]:
        sheets = pd.read_excel(file_path, sheet_name=None)
        for sheet_name, df in sheets.items():
            for start_row in range(0, len(df), chunk_size):
                end_row = min(start_row + chunk_size, len(df))
                chunk_text = df.iloc[start_row:end_row].to_string(index=False)
                chunks = chunk(chunk_text)
                embeddings = get_embedding(chunks)
                for i, embedding in enumerate(embeddings):
                    metadata = {
                        "session_id": session_id,
                        "user_id": user_id,
                        "source": file_path,
                        "sheet_name": sheet_name,
                        "row_range": f"rows {start_row + 1}-{end_row}",
                        "chunk_text": chunks[i],
                    }
                    vector_store.upsert(f"{session_id}_{user_id}_{sheet_name}_{start_row}_{i}", embedding, metadata)
                chunks_count += len(chunks)

    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

    return {"chunks": chunks_count}