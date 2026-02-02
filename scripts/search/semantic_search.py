import chromadb
from sentence_transformers import SentenceTransformer

# CONFIG
CHROMA_PATH = "output/vector_db/chroma"
COLLECTION_NAME = "rbac_chunks"
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def semantic_search(query: str, top_k: int = 5):
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)
    
    # Embed query
    query_embedding = model.encode(query).tolist()

    # THE FIX: include=['metadatas', 'documents']
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["metadatas", "documents", "distances"]
    )

    formatted_results = []
    
    if not results["ids"] or len(results["ids"][0]) == 0:
        return formatted_results

    # Loop through the results
    for i in range(len(results["ids"][0])):
        # If this still says None, the indexer (Step 2) failed
        meta = results["metadatas"][0][i] or {}
        
        formatted_results.append({
            "chunk_text": results["documents"][0][i],
            "document_name": meta.get("document_name", "Unknown Source"),
            "department": meta.get("department", "N/A"),
            "allowed_roles": meta.get("allowed_roles", "Employee"),
            "similarity": round(1 - results["distances"][0][i], 3)
        })

    return formatted_results

if __name__ == "__main__":
    q = input("Search: ")
    res = semantic_search(q)
    for r in res:
        print(f"\nSource: {r['document_name']} | Dept: {r['department']}")
        print(f"Text: {r['chunk_text'][:100]}...")