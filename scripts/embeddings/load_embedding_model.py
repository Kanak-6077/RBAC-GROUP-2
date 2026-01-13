from sentence_transformers import SentenceTransformer
import pandas as pd

def main():
    print("Milestone 2 Task 1: Embedding Model Setup")

    # Load embedding model
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("Embedding model loaded")

    # Path to metadata file (created in Milestone 1)
    metadata_path = "output/metadata.csv"

    # Read metadata
    df = pd.read_csv(metadata_path)

    # Take one real chunk from metadata
    sample_chunk = df.iloc[0]["title"]

    # Generate embedding
    embedding = model.encode(sample_chunk)

    print("Embedding vector length:", len(embedding))

    # Save proof output
    with open("output/test_embedding/sample_embedding_test.txt", "w") as f:
        f.write("Sample chunk:\n")
        f.write(sample_chunk[:300] + "\n\n")
        f.write(f"Embedding vector length: {len(embedding)}\n")

if __name__ == "__main__":
    main()

