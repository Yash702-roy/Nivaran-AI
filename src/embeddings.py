from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_embedding_model():
    return SentenceTransformer(MODEL_NAME)


def generate_embeddings(chunks, model):
    texts = [chunk["text"] for chunk in chunks]

    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return vectors


if __name__ == "__main__":
    model = load_embedding_model()

    sample_texts = [
        "UDID is a Unique Disability ID.",
        "The scheme supports accessibility in public buildings."
    ]

    vectors = model.encode(
        sample_texts,
        normalize_embeddings=True
    )

    print("Number of texts:", len(sample_texts))
    print("Vector shape:", vectors.shape)
    print("First vector dimensions:", vectors[0][:5])