from langchain_text_splitters import RecursiveCharacterTextSplitter
from document_loader import load_pdf


def create_chunks(pages):
    """Split extracted PDF pages into smaller chunks."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = []

    for page in pages:

        page_chunks = splitter.split_text(page["text"])

        for chunk in page_chunks:

            chunks.append({
                "text": chunk,
                "page": page["page"],
                "source": page["source"]
            })

    return chunks


if __name__ == "__main__":

    pdf = "C:\\Users\\Yash Kumar Roy\\Desktop\\Nivaran Ai\\data\\raw\\cbfe_scheme.pdf"

    pages = load_pdf(pdf)


    chunks = create_chunks(pages)

    print(f"Pages: {len(pages)}")
    print(f"Chunks: {len(chunks)}")

    print("\n--- FIRST CHUNK ---")
    print(chunks[0]["text"])

    print("\n--- METADATA ---")
    print("Source:", chunks[0]["source"])
    print("Page:", chunks[0]["page"])

  