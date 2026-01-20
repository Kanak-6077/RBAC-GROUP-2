# scripts/tests/test_rag_backend.py

from backend.rag.pipeline import run_rag_pipeline


def test_rag_pipeline():
    user = {
        "username": "Ritika",
        "role": "C-Level",
        "department": "Finance"
    }

    search_results = [
        {
            "text": "The company revenue grew by 15% in Q3.",
            "metadata": {
                "document_name": "Finance_Report_Q3.pdf",
                "department": "Finance"
            },
            "similarity": 0.89
        },
        {
            "text": "Marketing expenses increased in Q3.",
            "metadata": {
                "document_name": "Marketing_Report_Q3.pdf",
                "department": "Marketing"
            },
            "similarity": 0.72
        }
    ]

    query = "What was the revenue growth in Q3?"

    response = run_rag_pipeline(user, query, search_results)

    print("\n--- RAG PIPELINE OUTPUT ---")
    print(response)


if __name__ == "__main__":
    test_rag_pipeline()
