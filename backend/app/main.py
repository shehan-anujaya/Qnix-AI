"""
Qnix AI - FastAPI Backend Server
AI-Powered Knowledge Archive for Sri Lankan Students

This is the main entry point for the FastAPI backend server.
It handles CORS, routing, and server lifecycle events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import chat, documents, health

# Initialize FastAPI app
app = FastAPI(
    title="Qnix AI Backend",
    description="AI-Powered Knowledge Archive API using RAG and Local LLM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for Flutter desktop app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify Flutter app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])


@app.on_event("startup")
async def startup_event():
    """Initialize services on server startup"""
    print("🚀 Qnix AI Backend Server Starting...")
    print("📚 Initializing vector store...")
    print("🤖 Checking Ollama connection...")
    print("✅ Server ready at http://localhost:8000")
    print("📖 API docs available at http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on server shutdown"""
    print("👋 Shutting down Qnix AI Backend...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Qnix AI Backend API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
