from sentence_transformers import SentenceTransformer

def main():
    print("Milestone 2 - Task 1: Embedding Model Setup")

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    sample_chunk = "This is a sample chunk used to test embedding generation."

    embedding = model.encode(sample_chunk)

    print("Embedding vector length:", len(embedding))

    with open("output/tests-embedding/sample_embedding_test.txt", "w") as f:
        f.write("Sample chunk:\n")
        f.write(sample_chunk + "\n\n")
        f.write(f"Embedding vector length: {len(embedding)}\n")

if __name__ == "__main__":
    main()
