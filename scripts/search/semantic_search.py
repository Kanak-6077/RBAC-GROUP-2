import chromadb
from sentence_transformers import SentenceTransformer

# -----------------------------
# CONFIG
# -----------------------------
CHROMA_PATH = "output/vector_db/chroma"
COLLECTION_NAME = "rbac_chunks"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# -----------------------------
# LOAD EMBEDDING MODEL
# -----------------------------

model = SentenceTransformer(EMBEDDING_MODEL)

# -----------------------------
# LOAD CHROMA COLLECTION
# -----------------------------
def load_collection():
    
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    collection = client.get_collection(name=COLLECTION_NAME)

    print(f" Total vectors in collection: {collection.count()}")
    return collection

# -----------------------------
# SEMANTIC SEARCH
# -----------------------------
def semantic_search(query: str, top_k: int = 5):
    """
    Performs semantic search and formats results for RBAC.
    """
    collection = load_collection()
    
    # Generate embedding for the user's query
    query_embedding = model.encode(query).tolist()

    # Query the database
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    formatted_results = []

    # Check if we actually got results back
    if not results or not results["documents"] or len(results["documents"][0]) == 0:
        return formatted_results

    # Loop through findings
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        formatted_results.append({
            "text": doc,  # Use 'text' to match common RAG patterns
            "department": meta.get("department"),
            "document_name": meta.get("document_name", "Unknown"),
            "similarity": 0.9 # Default if distance not used
        })

    return formatted_results

# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":
    user_query = input("Enter search query: ")

    try:
        results = semantic_search(user_query)

        if not results:
            print("❌ No results found in the database.")
        else:
            print(f"\n✅ Found {len(results)} Results:\n")
            for i, res in enumerate(results, start=1):
                print(f"--- Result {i} ---")
                print(f"Department: {res['department']}")
                print(f"Roles: {res['allowed_roles']}")
                print(f"Text: {res['chunk_text'][:200]}...") # Show first 200 chars
                print("-" * 30)
    except Exception as e:
        print(f" An error occurred: {e}")