"""
Chat Endpoint
Handles question-answering using RAG pipeline
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.rag.query import query_documents
from app.rag.prompts import create_chat_prompt

router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    question: str
    conversation_history: Optional[List[dict]] = []
    max_sources: Optional[int] = 3


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str
    sources: List[dict]
    confidence: Optional[str] = None


@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    """
    Answer a question using RAG pipeline
    
    Process:
    1. Retrieve relevant document chunks from vector store
    2. Construct prompt with context
    3. Generate answer using Ollama LLM
    4. Return answer with source references
    """
    if not request.question or len(request.question.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )
    
    try:
        # Query the RAG system
        result = await query_documents(
            question=request.question,
            max_results=request.max_sources,
            conversation_history=request.conversation_history
        )
        
        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate answer"
            )
        
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            confidence=result.get("confidence", "medium")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


@router.post("/summarize")
async def summarize_document(file_id: str):
    """
    Generate a summary of a specific document
    Uses the same RAG pipeline with a summarization prompt
    """
    try:
        # This is a placeholder for document summarization
        # In production, retrieve all chunks for the specific document
        # and generate a comprehensive summary
        
        return {
            "message": "Summarization feature coming soon",
            "file_id": file_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to summarize document: {str(e)}"
        )


@router.post("/generate-mcq")
async def generate_mcq(file_id: str, num_questions: int = 5):
    """
    Generate multiple choice questions from a document
    Future feature for student assessment
    """
    try:
        return {
            "message": "MCQ generation feature coming soon",
            "file_id": file_id,
            "requested_questions": num_questions
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate MCQs: {str(e)}"
        )
