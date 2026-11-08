import fitz
from pathlib import Path


def load_pdf(pdf_path):
    """Extract text from a PDF file."""

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"File not found: {pdf_path}")

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text()

        if text.strip():
            pages.append({
                "text": text,
                "page": page_number + 1,
                "source": pdf_path.name
            })

    document.close()

    return pages


if __name__ == "__main__":

    # pdf = "C:\\Users\\Yash Kumar Roy\\Desktop\\Nivaran Ai\\data\\raw\\uuid_scheme2026.pdf"
    pdf='C:\\Users\\Yash Kumar Roy\\Desktop\\Nivaran Ai\\data\\raw\\cbfe_scheme.pdf'

    pages = load_pdf(pdf)

    print(f"Total pages loaded: {len(pages)}")
    print(f"Page types: {type(pages)}")

    for page in pages[:2]:
        print("\n--- PAGE", page["page"], "---")
        print(page["text"][:1000])

   