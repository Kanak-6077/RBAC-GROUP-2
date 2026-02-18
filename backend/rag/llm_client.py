import os
import requests
from typing import List
from dotenv import load_dotenv

# Load Environment Variables
ENV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(ENV_PATH)

# Ollama settings (loaded from .env with defaults)
USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() == "true"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

# -------------------------------------------------
# LLM Generation Function - Ollama Only
# -------------------------------------------------
def generate_answer(
    context_chunks: List[str],
    user_question: str,
    timeout: int = 300
) -> str:
    """
    Sends context + question to Ollama local model.
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

Answer:"""

    return generate_ollama(prompt, timeout)


def generate_ollama(prompt: str, timeout: int = 180) -> str:
    """Generate answer using Ollama local model."""
    
    ollama_payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 2048,  # Increased from 200 to prevent response truncation
            "temperature": 0.1
        }
    }
    
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=ollama_payload,
            timeout=timeout
        )
        
        print(f"DEBUG: Ollama Response Status: {response.status_code}")
        print(f"DEBUG: Ollama Response Text: {response.text[:200]}...")
        
        if response.status_code == 200:
            result = response.json()
            generated_text = result.get("response", "").strip()
            print(f"DEBUG: Ollama generated: {generated_text[:100]}...")
            return generated_text
        else:
            error_msg = f"Ollama API failed with status {response.status_code}"
            print(f"DEBUG: {error_msg}: {response.text[:200]}")
            return error_msg
            
    except requests.exceptions.ConnectionError as e:
        error_msg = f"Ollama connection failed. Make sure Ollama is running: ollama run {OLLAMA_MODEL}"
        print(f"DEBUG: {error_msg}: {e}")
        return error_msg
    except Exception as e:
        error_msg = f"Ollama error: {str(e)}"
        print(f"DEBUG: {error_msg}")
        return error_msg
