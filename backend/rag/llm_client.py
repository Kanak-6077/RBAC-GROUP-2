# backend/rag/llm_client.py

import os
import requests
from typing import List
from dotenv import load_dotenv
from backend.rag.prompts import build_prompt

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(ENV_PATH)

HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("Hugging Face API token not found in .env")

# -------------------------------------------------
# Hugging Face Model (FREE + STABLE)
# -------------------------------------------------
HF_MODEL_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# -------------------------------------------------
# LLM Call
# -------------------------------------------------
def generate_answer(
    context_chunks: List[str],
    user_question: str,
    timeout: int = 30
) -> str:
    """
    Sends context + question to Hugging Face LLM
    and returns generated answer.
    """

    # 🔴 IMPORTANT: keep prompt SHORT for free tier
    context = "\n".join(context_chunks[:3])  # LIMIT context
    prompt = build_prompt([context], user_question)

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.2
        }
    }

    try:
        response = requests.post(
            HF_MODEL_URL,
            headers=HEADERS,
            json=payload,
            timeout=timeout
        )

        if response.status_code != 200:
            return f"LLM Error: API failed (status {response.status_code})"

        result = response.json()

        # HF text-generation format
        if isinstance(result, list) and len(result) > 0:
            if "generated_text" in result[0]:
                return result[0]["generated_text"].strip()

        return "LLM Error: Empty or unexpected response."

    except requests.exceptions.Timeout:
        return "LLM Error: Request timed out."

    except requests.exceptions.RequestException as e:
        return f"LLM Error: {str(e)}"
