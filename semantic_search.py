import os
import json
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# -----------------------------
# CONFIG
# -----------------------------
EMBEDDINGS_FILE = r"C:\Users\siing\Downloads\embeddings.json"
CHROMA_PATH = "output/vector_db/chroma"
COLLECTION_NAME = "rbac_chunks"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# -----------------------------
# LOAD MODEL
# -----------------------------
model = SentenceTransformer(EMBEDDING_MODEL)

# -----------------------------
# CHROMA CLIENT
# -----------------------------
def get_chroma_client():
    return chromadb.Client(
        Settings(
            persist_directory=CHROMA_PATH,
            anonymized_telemetry=False
        )
    )

# -----------------------------
# LOAD EMBEDDINGS (TASK 3)
# -----------------------------
def load_embeddings(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing embeddings file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)["embeddings"]

# -----------------------------
# INDEX INTO CHROMA (TASK 3)
# -----------------------------
def index_to_chroma():
    embeddings = load_embeddings(EMBEDDINGS_FILE)
    client = get_chroma_client()

    collection = client.get_or_create_collection(COLLECTION_NAME)

    collection.add(
        ids=[e["chunk_id"] for e in embeddings],
        embeddings=[e["embedding"] for e in embeddings],
        documents=[e["chunk_text"] for e in embeddings],
        metadatas=[
            {
                "chunk_id": e["chunk_id"],
                "document_name": e["document_name"],
                "department": e["department"],
                "allowed_roles": ",".join(e["allowed_roles"])  # stored as string
            }
            for e in embeddings
        ]
    )

    print(f"Indexed {collection.count()} chunks into ChromaDB")

# -----------------------------
# LOAD COLLECTION (TASK 4)
# -----------------------------
def load_collection():
    client = get_chroma_client()
    return client.get_collection(COLLECTION_NAME)

# -----------------------------
# SEMANTIC SEARCH (TASK 4)
# -----------------------------
def semantic_search(query: str, top_k: int = 5):
    collection = load_collection()

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    formatted_results = []

    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        formatted_results.append({
            "chunk_text": doc,
            "department": meta.get("department"),
            "allowed_roles": meta.get("allowed_roles", "").split(",")
        })

    return formatted_results

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    # Step 1: Index data (run once)
    index_to_chroma()

    # Step 2: Semantic search
    query = input("\nEnter search query: ")
    results = semantic_search(query)

    for i, res in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("Text:", res["chunk_text"])
        print("Department:", res["department"])
        print("Allowed Roles:", res["allowed_roles"])