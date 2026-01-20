# backend/rag/pipeline.py

from typing import List, Dict
from backend.rag.llm_client import generate_answer


def calculate_confidence(similarities: List[float]) -> float:
    """
    Confidence = average similarity score (rounded to 2 decimals)
    """
    if not similarities:
        return 0.0
    return round(sum(similarities) / len(similarities), 2)


def run_rag_pipeline(
    user: Dict,
    query: str,
    search_results: List[Dict]
) -> Dict:
    """
    Full RAG Flow:
    Authenticate → RBAC-filter → Prompt → LLM → Source Attribution
    """

    # -------------------------------
    # 1. RBAC FILTERING
    # -------------------------------
    allowed_chunks = []

    for item in search_results:
        metadata = item["metadata"]

        # C-Level: access everything
        if user["role"] == "C-Level":
            allowed_chunks.append(item)

        # Others: only own department
        elif metadata["department"] == user["department"]:
            allowed_chunks.append(item)

    if not allowed_chunks:
        return {
            "answer": "Access denied for requested information.",
            "sources": [],
            "confidence_score": 0.0
        }

    # -------------------------------
    # 2. CONTEXT + SOURCES
    # -------------------------------
    context_chunks = [c["text"] for c in allowed_chunks]
    sources = list({
        c["metadata"]["document_name"]
        for c in allowed_chunks
    })

    similarities = [c["similarity"] for c in allowed_chunks]

    # -------------------------------
    # 3. LLM GENERATION
    # -------------------------------
    answer = generate_answer(context_chunks, query)

    # -------------------------------
    # 4. CONFIDENCE SCORE
    # -------------------------------
    confidence = calculate_confidence(similarities)

    return {
        "answer": answer,
        "sources": sources,
        "confidence_score": confidence
    }
