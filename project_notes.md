# Nivaran AI — Project Learning Notes

## 1. Project Overview

**Project Name:** Nivaran AI

**Main Objective:** Build a voice-first AI assistant that helps visually impaired people understand Indian government schemes through simple, accessible explanations.

A user should be able to ask a question such as:

- "What is a UDID card?"
- "Explain the government scheme for disability certification."
- "Who is eligible for this scheme?"

Nivaran AI should retrieve relevant information from trusted government documents, generate an understandable answer, and eventually speak the answer aloud.

## 2. Why Are We Building This Project?

Government scheme information is often published in long PDFs and documents. Finding the relevant information and understanding official terminology can be difficult, particularly for people who cannot easily access text-based information.

Nivaran AI aims to make this information easier to access through conversational AI and voice interaction.

**Important principle:** The assistant should answer from reliable sources, distinguish eligibility requirements from benefits, and avoid inventing information that is missing from the documents.

## 3. What Is Our Current Technology Stack?

| Component | Technology | Purpose |
|---|---|---|
| Programming language | Python | Main development language |
| PDF extraction | PyMuPDF (`fitz`) | Extract text from PDF documents |
| Text chunking | LangChain Text Splitters | Divide long text into smaller pieces |
| Embedding model | Sentence Transformers | Convert text into numerical vectors |
| Embedding model name | `sentence-transformers/all-MiniLM-L6-v2` | Generate 384-dimensional embeddings |
| Vector database/index | FAISS | Search for relevant text efficiently |
| Metadata storage | Pickle | Save text chunks and their metadata |
| LLM integration | OpenRouter (planned for the RAG pipeline) | Generate answers using retrieved information |
| Speech input/output | To be implemented | Enable voice-based interaction |

## 4. Our Source Documents

We collected two government documents:

### Document 1: UDID Scheme

The document discusses the Unique Disability ID (UDID) project and disability certification.

It provides information related to the purpose of UDID, disability certification, and the implementation of the project.

### Document 2: CBFE Scheme

CBFE stands for the Scheme for Creation of Barrier-Free Environment.

The document discusses accessibility improvements, including measures such as accessible information systems, tactile pathways, Braille signage, and other accessibility facilities.

**Important distinction:** These documents describe different kinds of government support. Accessibility grants for eligible institutions should not be presented as direct cash benefits for individual citizens.

## 5. What Have We Implemented So Far?

### Step 1: PDF Loading

File: `src/document_loader.py`

We use PyMuPDF to extract text from PDF pages.

The loader produces records containing:

- `text`: Extracted page text.
- `page`: Page number.
- `source`: Source PDF filename.

Why is this necessary?

The AI cannot reliably search the original PDFs as structured text until we extract their contents.

### Step 2: Text Chunking

File: `src/text_splitter.py`

We use `RecursiveCharacterTextSplitter` to divide long page text into smaller chunks.

Current settings:

- Chunk size: 1,000 characters.
- Chunk overlap: 200 characters.

Why do we need chunking?

A government PDF may contain many pages. Instead of searching the entire document as one large block, we search smaller passages that are more likely to contain the answer to a particular question.

The overlap helps preserve context between neighboring chunks.

### Step 3: Embedding Generation

File: `src/embeddings.py`

We use the model:

`sentence-transformers/all-MiniLM-L6-v2`

An embedding is a numerical representation of text. Text with related meanings can have similar vector representations.

For example:

- "What is a UDID card?"
- "Explain the Unique Disability ID."

Although the wording differs, these questions have similar meanings.

Our embedding model converts text into vectors with **384 dimensions**. We have tested the model successfully.

### Step 4: Building the FAISS Vector Database

File: `src/vector_store.py`

This script combines the previous steps:

1. Loads both PDF documents.
2. Extracts their text.
3. Splits the text into chunks.
4. Generates embeddings for the chunks.
5. Creates a FAISS index.
6. Saves the index and its corresponding text metadata.

Our successful output was:

- Total chunks: 85
- Vector dimensions: 384
- Status: Vector database created successfully.

Files generated:

- `vectorstore/nivaran.index`
- `vectorstore/chunks.pkl`

The FAISS index stores the searchable vectors. The pickle file stores the text chunks and metadata so we can recover the text associated with a matching vector.

We use `IndexFlatIP`, which performs inner-product search. Since our embeddings are normalized, the inner product corresponds to cosine similarity.

## 6. How Does Our Current Pipeline Work?

The current indexing pipeline is:

PDF documents → Text extraction → Text chunking → Embeddings → FAISS index + metadata.

This part has been implemented successfully.

## 7. What Is RAG?

RAG stands for Retrieval-Augmented Generation.

It combines two operations:

**Retrieval:** Find relevant information from our own document collection.

**Generation:** Give that information to a language model so it can produce a clear, natural-language answer.

For Nivaran AI, the intended flow is:

1. The user asks a question.
2. The question is converted into an embedding.
3. FAISS searches for similar document chunks.
4. The most relevant chunks are retrieved.
5. The retrieved context is passed to an LLM.
6. The LLM generates an answer grounded in that context.
7. The answer is eventually converted to speech.

We have built the document-indexing portion. The complete retrieval, generation, and voice pipeline is not yet finished.

## 8. What Is the Next Step?

Create `src/retriever.py`.

Its responsibilities will be:

1. Load `nivaran.index`.
2. Load the associated chunks from `chunks.pkl`.
3. Load the same embedding model.
4. Convert the user's question into a vector.
5. Search FAISS for the top three matching chunks.
6. Return the text, source filename, page number, and similarity score.

After that, we will connect the retriever to an LLM and build the complete RAG pipeline.

## 9. Current Project Status

- [x] Collect two government PDFs.
- [x] Implement PDF text extraction.
- [x] Implement text chunking.
- [x] Generate 384-dimensional embeddings.
- [x] Create and save the FAISS index.
- [ ] Test semantic retrieval with different questions.
- [ ] Connect retrieved context to an LLM.
- [ ] Generate answers grounded in the source documents.
- [ ] Add speech-to-text.
- [ ] Add text-to-speech.
- [ ] Test accessibility and answer reliability.

## 10. Key Concepts to Understand

**PDF extraction:** Converting document pages into machine-readable text.

**Chunking:** Splitting long text into manageable passages.

**Embedding:** Representing text numerically so semantic similarity can be measured.

**Vector index:** A structure used to search stored embeddings.

**Semantic search:** Searching by meaning rather than only matching exact keywords.

**Metadata:** Information such as a source filename and page number that identifies where a passage came from.

**RAG:** Retrieving relevant source information before asking an LLM to generate an answer.

**Grounded response:** An answer supported by retrieved evidence rather than an unsupported guess.

---

**Current milestone:** The two PDFs have been converted into 85 searchable text chunks represented by 384-dimensional vectors. The next milestone is to retrieve the correct passages for a user's question.