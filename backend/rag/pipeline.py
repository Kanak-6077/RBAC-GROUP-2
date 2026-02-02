import os
from typing import List, Dict

from dotenv import load_dotenv
from backend.rag.llm_client import generate_answer
# --- ADDED: Load environment variables from the project root ---
# This looks two levels up from backend/rag/ to find the .env file
env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path=env_path)

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
        # Get fields directly (not nested under 'metadata')
        department = item.get("department", "")
        
        # C-Level gets EVERYTHING
        if user.get("role") == "C-Level":
            allowed_chunks.append(item)
        
        # Others match department OR see "General" files
        elif department == user.get("department") or department == "General":
            allowed_chunks.append(item)

    if not allowed_chunks:
        return {
            "answer": "Access denied. You do not have permission to view the documents related to this query.",
            "sources": [],
            "confidence_score": 0.0
        }

    context_chunks = [c.get("chunk_text") or c.get("text") for c in allowed_chunks]
    
    # Get unique sources
    sources = list({c.get("document_name", "Unknown Source") for c in allowed_chunks})
    
    similarities = [c.get("similarity", 0.0) for c in allowed_chunks]

    answer = generate_answer(context_chunks, query)
    confidence = calculate_confidence(similarities)

    return {
        "answer": answer,
        "sources": sources,
        "confidence_score": confidence
    }