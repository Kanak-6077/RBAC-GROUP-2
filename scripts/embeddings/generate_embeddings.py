import os
import json
import pandas as pd
from sentence_transformers import SentenceTransformer

<<<<<<< Updated upstream
INPUT_CSV = "output/metadata.csv"
=======

METADATA_CSV = "output/metadata.csv"
>>>>>>> Stashed changes
OUTPUT_DIR = "output/embeddings"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "embeddings.json")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
<<<<<<< Updated upstream


def ensure_directories():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_chunks():
    if not os.path.exists(INPUT_CSV):
        raise FileNotFoundError(f"Input file not found: {INPUT_CSV}")
    return pd.read_csv(INPUT_CSV)
=======
BATCH_SIZE = 32



def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_metadata():
    if not os.path.exists(METADATA_CSV):
        raise FileNotFoundError("metadata.csv not found")

    df = pd.read_csv(METADATA_CSV)

    required_cols = ["chunk_id", "filename", "role", "allowed_roles", "text"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    print(f"[INFO] Loaded {len(df)} chunks from metadata.csv")
    return df
>>>>>>> Stashed changes

def load_model():
    print("[INFO] Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)
    print("[INFO] Model loaded successfully.")
    return model

<<<<<<< Updated upstream
def generate_embeddings(model, texts):
    print(f"[INFO] Generating embeddings for {len(texts)} chunks...")
    return model.encode(texts, show_progress_bar=True)

def save_embeddings(data):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[INFO] Embeddings saved to: {OUTPUT_FILE}")


def main():
    print("[START] Task 2: Embedding Generation")

    ensure_directories()

    df = load_chunks()
    print(f"[INFO] Loaded {len(df)} chunks from CSV")

    model = load_model()

    texts = df["text"].astype(str).tolist()
    embeddings = generate_embeddings(model, texts)

    output_data = []
    for i, row in df.iterrows():
        output_data.append({
            "chunk_id": row["chunk_id"],
            "doc_id": row.get("doc_id", ""),
            "filename": row["filename"],
            "title": row["title"],
            "role": row["role"],
            "chunk_index": int(row["chunk_index"]),
            "chunk_count": int(row["chunk_count"]),
            "embedding": embeddings[i].tolist()
        })

    save_embeddings(output_data)

    print("[SUCCESS] Task 2 completed successfully!")
=======

def main():
    print("[START] Task 2 – Bulk Embedding Generation")

    ensure_output_dir()
    df = load_metadata()
    model = load_model()

    texts = df["text"].astype(str).tolist()
    embeddings = []

    print("[INFO] Generating embeddings in batches...")

    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        batch_embeddings = model.encode(batch, show_progress_bar=False)
        embeddings.extend(batch_embeddings)

        print(f"[INFO] Processed {i + len(batch)} / {len(texts)} chunks")

    output_data = []

    for i, row in df.iterrows():
        roles = [r.strip() for r in row["allowed_roles"].split(",")]

        output_data.append({
            "chunk_id": row["chunk_id"],
            "embedding": embeddings[i].tolist(),
            "chunk_text": row["text"],
            "document_name": row["filename"],
            "department": row["role"],
            "allowed_roles": roles
        })

    final_json = {"embeddings": output_data}

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=2)

    print(f"[SUCCESS] Embeddings saved to: {OUTPUT_FILE}")
    print(f"[INFO] Total embeddings generated: {len(output_data)}")

>>>>>>> Stashed changes

if __name__ == "__main__":
    main()
