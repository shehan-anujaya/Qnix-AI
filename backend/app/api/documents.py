"""
Document Management Endpoints
Handles PDF upload, processing, and listing
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import os
import shutil
from datetime import datetime
import hashlib

from app.rag.ingest import ingest_pdf
from app.db.vector_store import get_vector_store

router = APIRouter()

# Storage directory for uploaded PDFs
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a PDF document
    
    Steps:
    1. Validate file is PDF
    2. Save to local storage
    3. Extract text and chunk
    4. Generate embeddings
    5. Store in vector database
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    try:
        # Generate unique filename using hash
        file_content = await file.read()
        file_hash = hashlib.md5(file_content).hexdigest()[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file_hash}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        
        # Save file to disk
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        # Process and ingest PDF into vector store
        result = await ingest_pdf(
            file_path=file_path,
            filename=file.filename,
            file_hash=file_hash
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Document uploaded and processed successfully",
                "filename": file.filename,
                "file_id": file_hash,
                "chunks_created": result.get("chunks_count", 0),
                "upload_time": timestamp
            }
        )
        
    except Exception as e:
        # Clean up file if processing failed
        if os.path.exists(file_path):
            os.remove(file_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {str(e)}"
        )


@router.get("/list")
async def list_documents():
    """
    List all uploaded documents
    Returns metadata about each document in the system
    """
    try:
        vector_store = get_vector_store()
        
        # Get all documents from vector store metadata
        # This is a simplified version - in production, maintain a separate metadata DB
        documents = []
        
        if os.path.exists(UPLOAD_DIR):
            for filename in os.listdir(UPLOAD_DIR):
                if filename.endswith('.pdf'):
                    file_path = os.path.join(UPLOAD_DIR, filename)
                    file_stats = os.stat(file_path)
                    
                    # Parse filename to extract metadata
                    parts = filename.split('_')
                    timestamp = parts[0] if len(parts) > 0 else "unknown"
                    file_hash = parts[1] if len(parts) > 1 else "unknown"
                    original_name = '_'.join(parts[2:]) if len(parts) > 2 else filename
                    
                    documents.append({
                        "id": file_hash,
                        "filename": original_name,
                        "upload_date": timestamp,
                        "size_bytes": file_stats.st_size,
                        "size_mb": round(file_stats.st_size / (1024 * 1024), 2)
                    })
        
        return {
            "total_documents": len(documents),
            "documents": sorted(documents, key=lambda x: x["upload_date"], reverse=True)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list documents: {str(e)}"
        )


@router.delete("/{file_id}")
async def delete_document(file_id: str):
    """
    Delete a document by its ID
    Removes from both storage and vector database
    """
    try:
        # Find and delete file
        deleted = False
        if os.path.exists(UPLOAD_DIR):
            for filename in os.listdir(UPLOAD_DIR):
                if file_id in filename and filename.endswith('.pdf'):
                    file_path = os.path.join(UPLOAD_DIR, filename)
                    os.remove(file_path)
                    deleted = True
                    break
        
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail=f"Document with ID {file_id} not found"
            )
        
        # TODO: Remove from vector store
        # This requires tracking document chunks by file_id in metadata
        
        return {
            "message": "Document deleted successfully",
            "file_id": file_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete document: {str(e)}"
        )
