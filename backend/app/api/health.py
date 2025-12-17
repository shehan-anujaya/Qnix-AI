"""
Health Check Endpoint
Verifies backend and Ollama connectivity
"""

from fastapi import APIRouter, HTTPException
import httpx
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify:
    - Backend server is running
    - Ollama service is accessible
    - Vector store is initialized
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {}
    }
    
    # Check Ollama connectivity
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                health_status["services"]["ollama"] = {
                    "status": "connected",
                    "models": response.json().get("models", [])
                }
            else:
                health_status["services"]["ollama"] = {
                    "status": "error",
                    "message": f"HTTP {response.status_code}"
                }
                health_status["status"] = "degraded"
    except Exception as e:
        health_status["services"]["ollama"] = {
            "status": "disconnected",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Check vector store (ChromaDB)
    try:
        from app.db.vector_store import get_vector_store
        vector_store = get_vector_store()
        health_status["services"]["vector_store"] = {
            "status": "initialized",
            "type": "ChromaDB"
        }
    except Exception as e:
        health_status["services"]["vector_store"] = {
            "status": "error",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    return health_status


@router.get("/health/ollama")
async def check_ollama():
    """
    Detailed Ollama service check
    Returns available models and version info
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                return {
                    "status": "connected",
                    "data": response.json()
                }
            else:
                raise HTTPException(
                    status_code=503,
                    detail=f"Ollama returned status {response.status_code}"
                )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Ensure Ollama is running at http://localhost:11434"
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Ollama health check failed: {str(e)}"
        )
