# backend/rag/llm_client.py

import os
import requests
from typing import List
from backend.rag.prompts import build_prompt

# Hugging Face model endpoint
HF_MODEL_URL = (
    "https://api-inference.huggingface.co/models/"
    "mistralai/Mistral-7B-Instruct-v0.2"
)

# Load token from environment variable
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}


def generate_answer(
    context_chunks: List[str],
    user_question: str,
    timeout: int = 30
) -> str:
    """
    Sends context + question to Hugging Face LLM
    and returns generated answer.
    """

    # ❌ Safety check
    if not HF_API_TOKEN:
        return "LLM Error: Hugging Face API token not found."

    # Build final prompt
    prompt = build_prompt(context_chunks, user_question)

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.2,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(
            HF_MODEL_URL,
            headers=HEADERS,
            json=payload,
            timeout=timeout
        )

        # Handle rate limit / server error
        if response.status_code != 200:
            return (
                f"LLM Error: API failed "
                f"(status {response.status_code})"
            )

        result = response.json()

        # Expected HF response format
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"].strip()

        return "LLM Error: Unexpected response format."

    except requests.exceptions.Timeout:
        return "LLM Error: Request timed out."

    except requests.exceptions.RequestException as e:
        return f"LLM Error: {str(e)}"
