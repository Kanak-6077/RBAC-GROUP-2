import os
import json
import chromadb

# CONFIG
EMBEDDINGS_FILE = "output/embeddings/embeddings.json"
CHROMA_PATH = "output/vector_db/chroma"
COLLECTION_NAME = "rbac_chunks"

def index_to_vector_db():
    if not os.path.exists(EMBEDDINGS_FILE):
        print(f"❌ Error: {EMBEDDINGS_FILE} not found!")
        return

    # 1. Load the pre-calculated embeddings
    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)["embeddings"]

    # 2. Connect to ChromaDB
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    # 3. Create fresh collection
    collection = client.get_or_create_collection(COLLECTION_NAME)

    # 4. Prepare data
    ids = [str(e["chunk_id"]) for e in data]
    embeddings = [e["embedding"] for e in data]
    documents = [e["chunk_text"] for e in data]
    
    # CRITICAL: We map exactly what we need for Milestone 4
    metadatas = [
        {
            "document_name": e.get("document_name", "Unknown"),
            "department": e.get("department", "General"),
            "allowed_roles": ",".join(e.get("allowed_roles", ["Employee"]))
        }
        for e in data
    ]

    # 5. Add to DB
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
    
    print(f"SUCCESS: Indexed {collection.count()} chunks with metadata.")

if __name__ == "__main__":
    index_to_vector_db()