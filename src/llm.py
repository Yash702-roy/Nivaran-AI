
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# Load environment variables from the project root
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = os.getenv("OPENROUTER_MODEL")

if not API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY is missing from your .env file."
    )

if not MODEL_NAME:
    raise ValueError(
        "OPENROUTER_MODEL is missing from your .env file."
    )


def load_llm():
    return ChatOpenAI(
        model=MODEL_NAME,
        api_key=API_KEY,
        base_url="https://openrouter.ai/api/v1",
        temperature=0
    )


def generate_answer(question, context):
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are Nivaran AI, an accessible assistant that explains
government schemes in simple language.

Use only the information provided in the context.

Rules:
1. Treat the retrieved context as the primary source of truth.
2. Do not invent facts, eligibility rules, benefits, deadlines,
   application procedures, or financial amounts.
3. If the context does not answer the question, say:
   "I could not find this information in the retrieved
   government documents."
4. Do not introduce general knowledge as if it came from
   the supplied documents.
5. If general background is explicitly requested, label it
   clearly as general information, not verified document content.
6. Distinguish support for institutions from benefits for
   individual citizens.
7. Keep answers clear, concise, respectful, and accessible.
8. Mention the relevant source and page when available.

Retrieved context:
{context}
"""
        ),
        (
            "human",
            "User question: {question}"
        )
    ])

    llm = load_llm()
    chain = prompt | llm

    response = chain.invoke({
        "question": question,
        "context": context
    })

    return response.content


if __name__ == "__main__":
    sample_context = """
The UDID project relates to disability certification
and the issuance of Unique Disability ID cards.
"""

    sample_question = "What is the purpose of the UDID project?"

    answer = generate_answer(
        sample_question,
        sample_context
    )

    print("\nNivaran AI Answer:\n")
    print(answer)
