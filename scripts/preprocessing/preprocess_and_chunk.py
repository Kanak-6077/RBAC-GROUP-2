import os
import re
import json
import pandas as pd
from sentence_transformers import SentenceTransformer

# Configuration

DATA_DIR = "data"
MAPPING_FILE = "data/role_document_mapping.csv" 
OUTPUT_DIR = "output"

CHUNK_SIZE = 400
CHUNK_OVERLAP = 50

model = SentenceTransformer("all-MiniLM-L6-v2")

# File Reading Utilities

def clean_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    return text.strip()


def read_markdown(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def read_csv(file_path: str) -> str:
    df = pd.read_csv(file_path)
    return " ".join(df.astype(str).values.flatten())

# Chunking Logic

def chunk_text(text: str) -> list:
    tokens = model.tokenizer.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + CHUNK_SIZE
        chunk_tokens = tokens[start:end]
        chunks.append(model.tokenizer.decode(chunk_tokens))
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


# Role Mapping

def load_role_mapping() -> pd.DataFrame:
    df = pd.read_csv(MAPPING_FILE)
    df["Allowed_Roles"] = df["Allowed_Roles"].apply(
        lambda x: [role.strip() for role in x.split(",")]
    )
    return df

# Document Processing

def process_documents() -> list:
    mapping_df = load_role_mapping()
    all_chunks = []

    for _, row in mapping_df.iterrows():
        document_name = row["Document_Name"]
        department = row["Department"].strip()
        department_dir = department.lower()
        allowed_roles = row["Allowed_Roles"]

        document_path = os.path.join(DATA_DIR, department_dir, document_name)

        if not os.path.exists(document_path):
            print(f"Skipping missing file: {document_path}")
            continue

        if document_name.endswith(".md"):
            raw_text = read_markdown(document_path)
        elif document_name.endswith(".csv"):
            raw_text = read_csv(document_path)
        else:
            continue

        cleaned_text = clean_text(raw_text)
        chunks = chunk_text(cleaned_text)

        for idx, chunk in enumerate(chunks, start=1):
            all_chunks.append({
                "chunk_id": f"{department}_{document_name}_{idx:03}",
                "source_file": document_name,
                "department": department,
                "allowed_roles": allowed_roles,
                "text": chunk
            })

    return all_chunks

# Entry Point

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    chunks = process_documents()
    print(f"Total chunks generated: {len(chunks)}")

    output_path = os.path.join(OUTPUT_DIR, "sample_chunks.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks[:10], f, indent=2)

    print("Sample chunks saved to output/sample_chunks.json")
