"""
Ollama REST API Client
Handles communication with local Ollama server for embeddings and chat
"""

import httpx
from typing import List, Optional, Dict
import json


# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
CHAT_MODEL = "qwen3:8b"  # Using qwen2.5:3b as it's more commonly available


async def generate_embeddings(text: str, model: str = EMBEDDING_MODEL) -> List[float]:
    """
    Generate embeddings for text using Ollama
    
    Args:
        text: Text to embed
        model: Embedding model to use
        
    Returns:
        List of embedding values (vector)
        
    Raises:
        Exception: If Ollama request fails
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/embeddings",
                json={
                    "model": model,
                    "prompt": text
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["embedding"]
            else:
                raise Exception(f"Ollama embeddings API returned status {response.status_code}")
                
    except httpx.ConnectError:
        raise Exception(
            "Cannot connect to Ollama. Please ensure Ollama is running at http://localhost:11434"
        )
    except Exception as e:
        raise Exception(f"Failed to generate embeddings: {str(e)}")


async def generate_chat_completion(
    prompt: str,
    model: str = CHAT_MODEL,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> str:
    """
    Generate chat completion using Ollama
    
    Args:
        prompt: Full prompt including system message and context
        model: LLM model to use
        temperature: Sampling temperature (0.0 to 1.0)
        max_tokens: Maximum tokens to generate
        
    Returns:
        Generated text response
        
    Raises:
        Exception: If Ollama request fails
    """
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            # Prepare request payload
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                }
            }
            
            if max_tokens:
                payload["options"]["num_predict"] = max_tokens
            
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["response"]
            else:
                raise Exception(f"Ollama chat API returned status {response.status_code}")
                
    except httpx.ConnectError:
        raise Exception(
            "Cannot connect to Ollama. Please ensure Ollama is running at http://localhost:11434"
        )
    except httpx.ReadTimeout:
        raise Exception(
            "Ollama request timed out. The model might be too large or the prompt too complex."
        )
    except Exception as e:
        raise Exception(f"Failed to generate chat completion: {str(e)}")


async def check_model_availability(model: str) -> bool:
    """
    Check if a specific model is available in Ollama
    
    Args:
        model: Model name to check
        
    Returns:
        True if model is available, False otherwise
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            
            if response.status_code == 200:
                data = response.json()
                models = data.get("models", [])
                
                # Check if model exists in the list
                for m in models:
                    if m.get("name") == model or m.get("name").startswith(model):
                        return True
                
                return False
            else:
                return False
                
    except:
        return False


async def pull_model(model: str) -> Dict:
    """
    Pull a model from Ollama registry
    
    Args:
        model: Model name to pull
        
    Returns:
        Dictionary with pull status
    """
    try:
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/pull",
                json={"name": model},
                timeout=600.0
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": f"Model {model} pulled successfully"
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to pull model: HTTP {response.status_code}"
                }
                
    except Exception as e:
        return {
            "success": False,
            "message": f"Error pulling model: {str(e)}"
        }
