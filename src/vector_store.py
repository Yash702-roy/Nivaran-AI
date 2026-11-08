
from pathlib import Path
import pickle
import faiss

from src.document_loader import load_pdf
from src.text_splitter import create_chunks
from src.embeddings import load_embedding_model, generate_embeddings


DATA_DIR = Path("data/raw")
VECTOR_DIR = Path("vectorstore")

PDF_FILES = [
    DATA_DIR / "cbfe_scheme.pdf",
    DATA_DIR / "uuid_scheme2026.pdf"
]


def load_all_chunks():
    all_chunks = [] 

    for pdf_path in PDF_FILES:
        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF not found: {pdf_path}"
            )

        pages = load_pdf(pdf_path)
        chunks = create_chunks(pages)
        all_chunks.extend(chunks)

        print(
            f"{pdf_path.name}: "
            f"{len(pages)} pages, {len(chunks)} chunks"
        )

    return all_chunks


def build_vector_store():
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load and chunk both PDFs
    chunks = load_all_chunks()

    for i, chunk in enumerate(chunks):
        if (
            "uuid_scheme2026.pdf" in chunk["source"]
            and any(
                word in chunk["text"].lower()
                for word in ["unique identification", "udid", "disabilities"]
            )
        ):
            print(f"\nChunk index: {i}")
            print(f"Page: {chunk['page']}")
            print(chunk["text"][:700])

    for i, chunk in enumerate(chunks):
        if (chunk["source"] == "cbfe_scheme.pdf"and "OBJECTIVES" in chunk["text"].upper()):
                print("\nFound objectives chunk:")
                print("Chunk index:", i)
                print("Page:", chunk["page"])
                print(chunk["text"][:1000])

    if not chunks:
        raise ValueError("No text chunks found.")

    # 2. Generate embeddings
    model = load_embedding_model()
    vectors = generate_embeddings(chunks, model)

    # FAISS expects float32 vectors
    vectors = vectors.astype("float32")

    # 3. Create a FAISS index
    dimension = vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)

    # 4. Save the index and corresponding metadata
    faiss.write_index(
        index,
        str(VECTOR_DIR / "nivaran.index")
    )

    with open(VECTOR_DIR / "chunks.pkl", "wb") as file:
        pickle.dump(chunks, file)

    print("\nVector database created successfully!")
    print("Total chunks:", len(chunks))
    print("Vector dimensions:", dimension)
    print("Saved to:", VECTOR_DIR.resolve())


if __name__ == "__main__":
    build_vector_store()
