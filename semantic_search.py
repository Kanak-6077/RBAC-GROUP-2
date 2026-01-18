import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# -----------------------------
# CONFIG (must match Task 3)
# -----------------------------
CHROMA_PATH = "output/vector_db/chroma"
COLLECTION_NAME = "rbac_chunks"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# -----------------------------
# LOAD EMBEDDING MODEL (Task 1)
# -----------------------------
model = SentenceTransformer(EMBEDDING_MODEL)

# -----------------------------
# LOAD CHROMA COLLECTION (Task 4)
# -----------------------------
def load_collection():
    client = chromadb.Client(
        Settings(
            persist_directory=CHROMA_PATH,
            anonymized_telemetry=False
        )
    )
    return client.get_collection(COLLECTION_NAME)

# -----------------------------
# SEMANTIC SEARCH (Task 4)
# -----------------------------
def semantic_search(query: str, top_k: int = 5):
    """
    Performs semantic search on already indexed Chroma DB.
    Returns structured results for RBAC filtering (Task 5).
    """

    collection = load_collection()
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    formatted_results = []

    if not results["documents"]:
        return formatted_results

    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        formatted_results.append({
            "chunk_text": doc,
            "department": meta.get("department"),
            # allowed_roles stored as comma-separated string in Task 3
            "allowed_roles": meta.get("allowed_roles", "").split(",")
        })

    return formatted_results

# -----------------------------
# TEST RUN
# -----------------------------
if __name__ == "__main__":
    query = input("Enter search query: ")
    results = semantic_search(query)

    for i, res in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("Text:", res["chunk_text"])
        print("Department:", res["department"])
        print("Allowed Roles:", res["allowed_roles"])