from sentence_transformers import SentenceTransformer
import pandas as pd

def main():
    print("Milestone 2 Task 1: Embedding generation using metadata chunk_text")

    # Load model
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("Embedding model loaded")

    # Read metadata (now has chunk_text)
    metadata_df = pd.read_csv("output/metadata.csv")

    # Pick one random chunk_text
    sample_chunk = metadata_df.iloc[0]["text"]

    # Generate embedding
    embedding = model.encode(sample_chunk)

    print("Embedding vector length:", len(embedding))

    # Save test output
    with open("output/test_embedding/sample_embedding_test.txt", "w") as f:
        f.write("Sample chunk (first 300 chars):\n")
        f.write(sample_chunk[:300] + "\n\n")
        f.write(f"Embedding vector length: {len(embedding)}\n")

if __name__ == "__main__":
    main()


