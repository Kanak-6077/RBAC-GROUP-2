from sentence_transformers import SentenceTransformer

def main():
    print("Milestone 2 - Task 1: Embedding Model Setup")

    print("Loading embedding model...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("Model loaded successfully.")

    sample_text = "This is a sample sentence to test embedding generation."

    print("Generating embedding...")
    embedding = model.encode(sample_text)

    print("Embedding generated successfully.")
    print("Embedding vector length:", len(embedding))

if __name__ == "__main__":
    main()
