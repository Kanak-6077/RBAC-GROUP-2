# backend/rag/llm_client.py

import requests
from typing import List
from backend.rag.prompts import build_prompt

# -------------------------------------------------
# Ollama Configuration
# -------------------------------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"   # you already pulled this

# -------------------------------------------------
# LLM Call (Ollama)
# -------------------------------------------------
def generate_answer(
    context_chunks: List[str],
    user_question: str,
    timeout: int = 120
) -> str:
    """
    Sends context + question to Ollama LLM
    and returns generated answer.
    """
    
    # Check if Ollama is enabled
    if not USE_OLLAMA:
        return "LLM Error: Ollama is disabled. Set USE_OLLAMA=true in .env"
    
    # Prepare the context (Limit to 1 chunk, max 500 chars)
    if not context_chunks:
        return "No context provided to generate an answer."
    
    # Use up to 6 chunks with 1500 chars each for better diversity
    context_text = "\n\n".join([chunk[:1500] for chunk in context_chunks[:6]])
    
    # Simple Prompt
    prompt = f"""You are a helpful assistant. Answer the question based ONLY on the context below.

Context:
{context_text}

Question:
{user_question}

    # Keep context short (good practice)
    context = "\n".join(context_chunks[:3])
    prompt = build_prompt([context], user_question)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=timeout
        )

        if response.status_code != 200:
            return f"LLM Error: API failed (status {response.status_code})"

        result = response.json()

        return result.get("response", "").strip() or "LLM Error: Empty response."

    except requests.exceptions.Timeout:
        return "LLM Error: Request timed out."

    except requests.exceptions.RequestException as e:
        return f"LLM Error: {str(e)}"
