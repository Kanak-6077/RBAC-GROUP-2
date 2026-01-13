import os
import json
import pandas as pd
from sentence_transformers import SentenceTransformer

INPUT_CSV = "output/metadata.csv"
OUTPUT_DIR = "output/embeddings"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "embeddings.json")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def ensure_directories():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_chunks():
    if not os.path.exists(INPUT_CSV):
        raise FileNotFoundError(f"Input file not found: {INPUT_CSV}")
    return pd.read_csv(INPUT_CSV)

def load_model():
    print("[INFO] Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)
    print("[INFO] Model loaded successfully.")
    return model

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

if __name__ == "__main__":
    main()
