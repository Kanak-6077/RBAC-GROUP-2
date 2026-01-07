import os
import re
import json
import pandas as pd
from sentence_transformers import SentenceTransformer

# Load tokenizer (used only for token counting + chunking)
model = SentenceTransformer("all-MiniLM-L6-v2")

DATA_DIR = "data"
MAPPING_FILE = os.path.join(DATA_DIR, "role_document_mapping.csv")
OUTPUT_DIR = "output"

def clean_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    return text.strip()

def read_markdown(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_csv(path):
    df = pd.read_csv(path)
    return " ".join(df.astype(str).values.flatten())

def chunk_text(text, chunk_size=400, overlap=50):
    tokens = model.tokenizer.encode(text)
    chunks = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk = model.tokenizer.decode(chunk_tokens)
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

def load_mapping():
    df = pd.read_csv(MAPPING_FILE)
    df["Allowed_Roles"] = df["Allowed_Roles"].apply(
        lambda x: [r.strip() for r in x.split(",")]
    )
    return df

def process_documents():
    mapping_df = load_mapping()
    all_chunks = []

    for _, row in mapping_df.iterrows():
        doc_name = row["Document_Name"]
        department = row["Department"]
        allowed_roles = row["Allowed_Roles"]

        doc_path = os.path.join(DATA_DIR, department, doc_name)

        if not os.path.exists(doc_path):
            print(f"⚠️ Skipping missing file: {doc_path}")
            continue

        if doc_name.endswith(".md"):
            raw_text = read_markdown(doc_path)
        elif doc_name.endswith(".csv"):
            raw_text = read_csv(doc_path)
        else:
            continue

        cleaned_text = clean_text(raw_text)
        chunks = chunk_text(cleaned_text)

        for idx, chunk in enumerate(chunks, start=1):
            all_chunks.append({
                "chunk_id": f"{department}_{doc_name}_{idx:03}",
                "source_file": doc_name,
                "department": department,
                "allowed_roles": allowed_roles,
                "text": chunk
            })

    return all_chunks

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    chunks = process_documents()
    print(f"Total chunks generated: {len(chunks)}")

    with open(os.path.join(OUTPUT_DIR, "sample_chunks.json"), "w", encoding="utf-8") as f:
        json.dump(chunks[:10], f, indent=2)

    print("Sample chunks saved to output/sample_chunks.json")
