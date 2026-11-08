
from pathlib import Path
import pickle
import faiss

from src.embeddings import load_embedding_model

VECTOR_DIR = Path("vectorstore")


def load_vector_store():
    index_path = VECTOR_DIR / "nivaran.index"
    chunks_path = VECTOR_DIR / "chunks.pkl"

    if not index_path.exists() or not chunks_path.exists():
        raise FileNotFoundError(
            "Vector database files not found. "
            "Run python src/vector_store.py first."
        )

    index = faiss.read_index(str(index_path))

    with open(chunks_path, "rb") as file:
        chunks = pickle.load(file)

    model = load_embedding_model()

    return index, chunks, model


def retrieve(query, index, chunks, model, top_k=5):
    query_vector = model.encode(
        [query],
        normalize_embeddings=True
    ).astype("float32")

    scores, indices = index.search(query_vector, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue

        chunk = chunks[int(idx)]

        results.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "page": chunk["page"],
            "similarity_score": float(score)
        })

    return results


if __name__ == "__main__":
    index, chunks, model = load_vector_store()

    query = input("Ask Nivaran AI a question: ")
    results = retrieve(query, index, chunks, model)

    print("\nRelevant information:\n")

    for i, result in enumerate(results, start=1):
        print(f"--- Result {i} ---")
        print("Source:", result["source"])
        print("Page:", result["page"])
        print("Similarity:", round(result["similarity_score"], 4))
        print(result["text"])
        print()
