"""
PDF Ingestion Pipeline
Extracts text, chunks, generates embeddings, and stores in vector DB
"""

import os
from typing import List, Dict
import hashlib

from app.utils.pdf_utils import extract_text_from_pdf
from app.utils.ollama_client import generate_embeddings
from app.db.vector_store import get_vector_store


# Chunking configuration
CHUNK_SIZE = 1000  # Characters per chunk
CHUNK_OVERLAP = 200  # Overlap between chunks for context continuity


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Split text into overlapping chunks
    
    Args:
        text: Full text to chunk
        chunk_size: Maximum characters per chunk
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        # Get chunk with specified size
        end = start + chunk_size
        chunk = text[start:end]
        
        # Try to break at sentence boundary if possible
        if end < text_length:
            # Look for sentence endings in the last 100 characters
            last_period = chunk.rfind('. ')
            last_newline = chunk.rfind('\n')
            break_point = max(last_period, last_newline)
            
            if break_point > chunk_size - 200:  # Only break if it's not too far back
                chunk = chunk[:break_point + 1]
                end = start + break_point + 1
        
        chunks.append(chunk.strip())
        
        # Move start position with overlap
        start = end - overlap
        
        # Prevent infinite loop
        if start >= text_length:
            break
    
    return [c for c in chunks if len(c) > 50]  # Filter out very small chunks


async def ingest_pdf(file_path: str, filename: str, file_hash: str) -> Dict:
    """
    Complete PDF ingestion pipeline
    
    Steps:
    1. Extract text from PDF
    2. Chunk text with overlap
    3. Generate embeddings for each chunk
    4. Store in vector database with metadata
    
    Args:
        file_path: Path to PDF file
        filename: Original filename
        file_hash: Unique identifier for the file
        
    Returns:
        Dictionary with ingestion results
    """
    try:
        # Step 1: Extract text from PDF
        print(f"📄 Extracting text from {filename}...")
        text = extract_text_from_pdf(file_path)
        
        if not text or len(text.strip()) < 100:
            raise ValueError("PDF appears to be empty or contains insufficient text")
        
        # Step 2: Chunk the text
        print(f"✂️  Chunking text (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
        chunks = chunk_text(text)
        print(f"   Created {len(chunks)} chunks")
        
        # Step 3: Generate embeddings for each chunk
        print(f"🧮 Generating embeddings...")
        embeddings = []
        for i, chunk in enumerate(chunks):
            embedding = await generate_embeddings(chunk)
            embeddings.append(embedding)
            
            if (i + 1) % 10 == 0:
                print(f"   Processed {i + 1}/{len(chunks)} chunks")
        
        # Step 4: Store in vector database
        print(f"💾 Storing in vector database...")
        vector_store = get_vector_store()
        
        # Prepare metadata for each chunk
        metadatas = [
            {
                "filename": filename,
                "file_id": file_hash,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "source": file_path
            }
            for i in range(len(chunks))
        ]
        
        # Generate unique IDs for each chunk
        ids = [f"{file_hash}_chunk_{i}" for i in range(len(chunks))]
        
        # Add to vector store
        vector_store.add(
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✅ Successfully ingested {filename}")
        
        return {
            "success": True,
            "filename": filename,
            "file_id": file_hash,
            "chunks_count": len(chunks),
            "total_characters": len(text)
        }
        
    except Exception as e:
        print(f"❌ Error ingesting PDF: {str(e)}")
        raise Exception(f"PDF ingestion failed: {str(e)}")


async def reindex_document(file_id: str) -> Dict:
    """
    Re-index an existing document
    Useful if chunking strategy or embeddings model changes
    
    Args:
        file_id: Unique identifier of the document
        
    Returns:
        Dictionary with re-indexing results
    """
    # This is a placeholder for future implementation
    # Would need to:
    # 1. Find the original PDF file
    # 2. Delete existing chunks from vector store
    # 3. Re-run ingestion pipeline
    
    return {
        "success": False,
        "message": "Re-indexing feature not yet implemented"
    }
