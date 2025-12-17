"""
ChromaDB Vector Store
Manages document embeddings and similarity search
"""

import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Optional


# ChromaDB configuration
CHROMA_DB_DIR = "data/chroma_db"
COLLECTION_NAME = "qnix_documents"

# Ensure directory exists
os.makedirs(CHROMA_DB_DIR, exist_ok=True)

# Global vector store instance
_vector_store = None


def get_vector_store():
    """
    Get or create ChromaDB vector store instance (Singleton pattern)
    
    Returns:
        ChromaDB collection instance
    """
    global _vector_store
    
    if _vector_store is None:
        print(f"🔧 Initializing ChromaDB at {CHROMA_DB_DIR}")
        
        # Initialize ChromaDB client with persistent storage
        client = chromadb.PersistentClient(
            path=CHROMA_DB_DIR,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        try:
            _vector_store = client.get_collection(name=COLLECTION_NAME)
            print(f"   Loaded existing collection: {COLLECTION_NAME}")
        except:
            _vector_store = client.create_collection(
                name=COLLECTION_NAME,
                metadata={"description": "Qnix AI document embeddings"}
            )
            print(f"   Created new collection: {COLLECTION_NAME}")
    
    return _vector_store


def reset_vector_store():
    """
    Reset the vector store (delete all data)
    WARNING: This will delete all indexed documents
    """
    global _vector_store
    
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print(f"🗑️  Deleted collection: {COLLECTION_NAME}")
    except:
        pass
    
    _vector_store = None
    print("✅ Vector store reset complete")


def get_collection_stats() -> Dict:
    """
    Get statistics about the vector store
    
    Returns:
        Dictionary with collection statistics
    """
    vector_store = get_vector_store()
    
    try:
        count = vector_store.count()
        
        return {
            "collection_name": COLLECTION_NAME,
            "total_chunks": count,
            "storage_path": CHROMA_DB_DIR
        }
    except Exception as e:
        return {
            "error": str(e)
        }


def delete_document_chunks(file_id: str) -> int:
    """
    Delete all chunks belonging to a specific document
    
    Args:
        file_id: Unique identifier of the document
        
    Returns:
        Number of chunks deleted
    """
    vector_store = get_vector_store()
    
    try:
        # Query all chunks with this file_id
        results = vector_store.get(
            where={"file_id": file_id}
        )
        
        if results and results.get('ids'):
            # Delete all matching chunks
            vector_store.delete(ids=results['ids'])
            deleted_count = len(results['ids'])
            print(f"🗑️  Deleted {deleted_count} chunks for file_id: {file_id}")
            return deleted_count
        
        return 0
        
    except Exception as e:
        print(f"❌ Error deleting chunks: {str(e)}")
        raise
