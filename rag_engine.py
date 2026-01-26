# backend/rag_engine.py

from typing import List, Dict

def compute_confidence(sources: List[Dict]) -> float:
    """
    Confidence is computed as the average similarity score
    of the retrieved document chunks.
    """
    if not sources:
        return 0.0
    scores = [src["score"] for src in sources if src["score"] is not None]
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 2)


def run_rag_engine(query: str, retrieved_chunks: List):
    """
    This function assumes retrieved_chunks is coming from Task 2
    and already contains role-filtered documents.
    """

    sources = []

    # Build citation metadata from retrieved chunks
    for chunk in retrieved_chunks:
        sources.append({
            "text": chunk.page_content,
            "document": chunk.metadata.get("doc_name", "Unknown Document"),
            "department": chunk.metadata.get("department", "Unknown Department"),
            "score": chunk.metadata.get("similarity_score", 0.0)
        })

    # Prompt augmentation for transparency
    context_text = "\n\n".join([src["text"] for src in sources])

    prompt = f"""
    You are an internal company assistant.
    Answer the question strictly using the context below.
    Do not hallucinate or use external knowledge.

    Context:
    {context_text}

    Question:
    {query}
    """

    # --- LLM call happens here (already implemented in Task 2) ---
    # final_answer = llm.generate(prompt)

    final_answer = "This is a placeholder answer generated from provided documents."

    response = {
        "answer": final_answer,
        "sources": sources,
        "confidence": compute_confidence(sources)
    }

    return response
