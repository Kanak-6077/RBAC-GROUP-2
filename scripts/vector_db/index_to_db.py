import os
import json
import chromadb
from chromadb.config import Settings

EMBEDDINGS_FILE = "output/embeddings/embeddings.json"
CHROMA_PATH = "output/vector_db/chroma"
COLLECTION_NAME = "rbac_chunks"


def load_embeddings(file_path: str) -> list:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing embeddings file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)["embeddings"]


def init_chroma_client():
    return chromadb.Client(
        Settings(
            persist_directory=CHROMA_PATH,
            anonymized_telemetry=False
        )
    )


def index_to_vector_db():
    embeddings = load_embeddings(EMBEDDINGS_FILE)
    client = init_chroma_client()

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
                "allowed_roles": ",".join(e["allowed_roles"])  # FIX
            }
            for e in embeddings
        ]
    )

    print(f"Indexed {collection.count()} embeddings into Chroma DB")


if __name__ == "__main__":
    index_to_vector_db()
