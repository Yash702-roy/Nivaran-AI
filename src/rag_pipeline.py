
# from retriever import load_vector_store, retrieve
# from llm import generate_answer
from src.retriever import load_vector_store, retrieve
from src.llm import generate_answer


def build_context(results):
    """Combine retrieved chunks into context for the LLM."""
    context_parts = []

    for i, result in enumerate(results, start=1):
        source = result["source"]
        page = result["page"]
        text = result["text"]

        context_parts.append(
            f"[Source {i}: {source}, Page {page}]\n{text}"
        )

    return "\n\n".join(context_parts)


def answer_question(query, index, chunks, model):
    """Retrieve relevant information and generate an answer."""

    # Step 1: Retrieve relevant chunks
    results = retrieve(
        query=query,
        index=index,
        chunks=chunks,
        model=model,
        top_k=3
    )

    # Step 2: Handle empty retrieval results
    if not results:
        return {
            "answer": (
                "I couldn't find relevant information in "
                "the available government documents."
            ),
            "sources": []
        }

    # Step 3: Build context from retrieved chunks
    context = build_context(results)

    # Step 4: Generate an answer using the LLM
    answer = generate_answer(
        question=query,
        context=context
    )

    # Step 5: Collect source references
    sources = []

    for result in results:
        source_info = {
            "source": result["source"],
            "page": result["page"]
        }

        if source_info not in sources:
            sources.append(source_info)

    return {
        "answer": answer,
        "sources": sources
    }


if __name__ == "__main__":
    print("Loading Nivaran AI...")

    # Load the vector index, text chunks, and embedding model
    index, chunks, model = load_vector_store()

    print("Nivaran AI is ready!")

    while True:
        query = input(
            "\nAsk a question (or type 'exit' to stop): "
        ).strip()

        if query.lower() in {"exit", "quit"}:
            print("Thank you for using Nivaran AI!")
            break

        if not query:
            print("Please enter a question.")
            continue

        try:
            result = answer_question(
                query=query,
                index=index,
                chunks=chunks,
                model=model
            )

            print("\nNivaran AI:")
            print(result["answer"])

            print("\nSources:")
            if result["sources"]:
                for source in result["sources"]:
                    print(
                        f"- {source['source']}, "
                        f"page {source['page']}"
                    )
            else:
                print("- No sources retrieved.")

        except Exception as error:
            print(f"\nAn error occurred: {error}")
