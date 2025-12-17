"""
RAG Query Engine
Retrieves relevant chunks and generates answers using LLM
"""

from typing import List, Dict, Optional

from app.utils.ollama_client import generate_embeddings, generate_chat_completion
from app.db.vector_store import get_vector_store
from app.rag.prompts import create_chat_prompt


async def query_documents(
    question: str,
    max_results: int = 3,
    conversation_history: Optional[List[dict]] = None
) -> Dict:
    """
    Query the knowledge base using RAG
    
    Process:
    1. Generate embedding for the question
    2. Retrieve top-k similar chunks from vector store
    3. Construct prompt with context
    4. Generate answer using LLM
    5. Return answer with sources
    
    Args:
        question: User's question
        max_results: Number of relevant chunks to retrieve
        conversation_history: Previous conversation messages
        
    Returns:
        Dictionary containing answer and source references
    """
    try:
        # Step 1: Generate embedding for the question
        print(f"🔍 Processing question: {question[:100]}...")
        question_embedding = await generate_embeddings(question)
        
        # Step 2: Retrieve relevant chunks from vector store
        print(f"📚 Searching vector database...")
        vector_store = get_vector_store()
        
        results = vector_store.query(
            query_embeddings=[question_embedding],
            n_results=max_results
        )
        
        # Extract chunks and metadata
        if not results or not results.get('documents') or len(results['documents'][0]) == 0:
            return {
                "answer": "I don't have any documents uploaded yet. Please upload some study materials first so I can help answer your questions.",
                "sources": [],
                "confidence": "none"
            }
        
        # Format retrieved chunks
        chunks = []
        for i, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i] if results.get('metadatas') else {}
            distance = results['distances'][0][i] if results.get('distances') else 0
            
            chunks.append({
                "text": doc,
                "filename": metadata.get("filename", "Unknown"),
                "chunk_index": metadata.get("chunk_index", i),
                "distance": distance
            })
        
        print(f"   Found {len(chunks)} relevant chunks")
        
        # Step 3: Construct prompt with context
        prompt = create_chat_prompt(
            question=question,
            context_chunks=chunks,
            conversation_history=conversation_history or []
        )
        
        # Step 4: Generate answer using LLM
        print(f"🤖 Generating answer with Ollama...")
        answer = await generate_chat_completion(prompt)
        
        # Step 5: Prepare response with sources
        sources = [
            {
                "filename": chunk["filename"],
                "chunk_index": chunk["chunk_index"],
                "relevance_score": round(1 - chunk["distance"], 2),  # Convert distance to similarity
                "preview": chunk["text"][:200] + "..." if len(chunk["text"]) > 200 else chunk["text"]
            }
            for chunk in chunks
        ]
        
        # Determine confidence based on relevance scores
        avg_relevance = sum(s["relevance_score"] for s in sources) / len(sources) if sources else 0
        confidence = "high" if avg_relevance > 0.7 else "medium" if avg_relevance > 0.4 else "low"
        
        print(f"✅ Answer generated (confidence: {confidence})")
        
        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence
        }
        
    except Exception as e:
        print(f"❌ Error in query pipeline: {str(e)}")
        raise Exception(f"Failed to process query: {str(e)}")


async def search_documents(query: str, max_results: int = 10) -> List[Dict]:
    """
    Search for relevant document chunks without generating an answer
    Useful for document exploration and finding specific information
    
    Args:
        query: Search query
        max_results: Maximum number of results to return
        
    Returns:
        List of relevant document chunks with metadata
    """
    try:
        # Generate embedding for search query
        query_embedding = await generate_embeddings(query)
        
        # Search vector store
        vector_store = get_vector_store()
        results = vector_store.query(
            query_embeddings=[query_embedding],
            n_results=max_results
        )
        
        # Format results
        search_results = []
        if results and results.get('documents'):
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results.get('metadatas') else {}
                distance = results['distances'][0][i] if results.get('distances') else 0
                
                search_results.append({
                    "text": doc,
                    "filename": metadata.get("filename", "Unknown"),
                    "chunk_index": metadata.get("chunk_index", i),
                    "relevance_score": round(1 - distance, 2)
                })
        
        return search_results
        
    except Exception as e:
        print(f"❌ Error in document search: {str(e)}")
        raise Exception(f"Search failed: {str(e)}")
