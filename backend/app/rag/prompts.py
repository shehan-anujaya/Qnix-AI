"""
Prompt Templates for LLM
Optimized for Sri Lankan student tutoring
"""

# System prompt for the AI tutor
SYSTEM_PROMPT = """You are an AI tutor for Sri Lankan students.

Your role is to:
- Explain concepts clearly and step-by-step
- Use simple language that students can understand
- Provide examples to illustrate concepts
- Break down complex topics into manageable parts
- Be encouraging and supportive

IMPORTANT RULES:
- Only answer using the provided document context
- If the answer is not in the documents, clearly say "I don't have information about that in the uploaded documents"
- Do not make up information or use external knowledge
- Always cite which document or section your answer comes from
- If you're unsure, express that uncertainty

Be patient, clear, and helpful. Your goal is to help students learn and understand."""


def create_chat_prompt(question: str, context_chunks: list, conversation_history: list = None) -> str:
    """
    Create a complete prompt for the LLM
    
    Args:
        question: User's question
        context_chunks: Relevant document chunks retrieved from vector store
        conversation_history: Previous messages in the conversation
        
    Returns:
        Formatted prompt string
    """
    # Format context from retrieved chunks
    context_text = "\n\n".join([
        f"[Document: {chunk.get('filename', 'Unknown')}]\n{chunk.get('text', '')}"
        for chunk in context_chunks
    ])
    
    # Build conversation history if provided
    history_text = ""
    if conversation_history:
        history_text = "\n\nPrevious conversation:\n"
        for msg in conversation_history[-3:]:  # Include last 3 exchanges
            role = msg.get("role", "user")
            content = msg.get("content", "")
            history_text += f"{role.capitalize()}: {content}\n"
    
    # Construct full prompt
    prompt = f"""{SYSTEM_PROMPT}

DOCUMENT CONTEXT:
{context_text}
{history_text}

STUDENT QUESTION:
{question}

ANSWER:
"""
    
    return prompt


def create_summarization_prompt(document_chunks: list, filename: str) -> str:
    """
    Create a prompt for document summarization
    
    Args:
        document_chunks: All chunks from a specific document
        filename: Name of the document
        
    Returns:
        Formatted summarization prompt
    """
    full_text = "\n\n".join([chunk.get('text', '') for chunk in document_chunks])
    
    prompt = f"""You are an AI tutor helping Sri Lankan students understand their study materials.

Please create a comprehensive summary of the following document: "{filename}"

DOCUMENT CONTENT:
{full_text}

Create a summary that:
1. Highlights the main topics and key concepts
2. Organizes information in a logical flow
3. Uses clear, simple language
4. Includes important definitions and formulas
5. Is suitable for exam revision

SUMMARY:
"""
    
    return prompt


def create_mcq_prompt(document_chunks: list, num_questions: int = 5) -> str:
    """
    Create a prompt for MCQ generation
    
    Args:
        document_chunks: Relevant document chunks
        num_questions: Number of questions to generate
        
    Returns:
        Formatted MCQ generation prompt
    """
    context_text = "\n\n".join([chunk.get('text', '') for chunk in document_chunks])
    
    prompt = f"""You are an AI tutor creating practice questions for Sri Lankan students.

Based on the following content, generate {num_questions} multiple choice questions (MCQs).

CONTENT:
{context_text}

For each question:
1. Create a clear, specific question
2. Provide 4 options (A, B, C, D)
3. Mark the correct answer
4. Ensure questions test understanding, not just memorization
5. Use appropriate difficulty level for the content

Format each question as:
Q1: [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Correct Answer: [Letter]
Explanation: [Brief explanation]

QUESTIONS:
"""
    
    return prompt

