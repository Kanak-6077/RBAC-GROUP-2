from typing import List, Dict
from backend.rag.llm_client import generate_answer

def calculate_confidence(similarities: List[float]) -> float:
    if not similarities:
        return 0.0
    return round(sum(similarities) / len(similarities), 2)

def run_rag_pipeline(user: Dict, query: str, search_results: List[Dict]) -> Dict:
    allowed_chunks = []

    # If search_results is empty, the pipeline cannot generate an answer
    if not search_results:
        return {
            "answer": "No relevant information found in the database.",
            "sources": [],
            "confidence_score": 0.0
        }

    for item in search_results:
        # Get metadata safely
        metadata = item.get("metadata", {})
        
        # C-Level gets EVERYTHING
        if user.get("role") == "C-Level":
            allowed_chunks.append(item)
        
        # Others match department OR see "General" files
        elif metadata.get("department") == user.get("department") or metadata.get("department") == "General":
            allowed_chunks.append(item)

    if not allowed_chunks:
        return {
            "answer": "Access denied. You do not have permission to view the documents related to this query.",
            "sources": [],
            "confidence_score": 0.0
        }

    context_chunks = [c["text"] for c in allowed_chunks]
    # Change this line in pipeline.py:
    sources = list({c.get("document_name", "Unknown Source") for c in allowed_chunks})
    similarities = [c.get("similarity", 0.0) for c in allowed_chunks]

    answer = generate_answer(context_chunks, query)
    confidence = calculate_confidence(similarities)

    return {
        "answer": answer,
        "sources": sources,
        "confidence_score": confidence
    }