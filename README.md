# Nivaran AI — Voice-Enabled Government Scheme Assistant

Nivaran AI is a voice-enabled AI assistant designed to make information about Indian government schemes easier to access and understand. Users can ask questions in Hindi or English, receive answers grounded in the available government documents, view source references, and listen to generated responses.

## Key Features

- **Document-grounded Q&A:** Uses Retrieval-Augmented Generation (RAG) to retrieve relevant passages before generating an answer.
- **Semantic search:** Uses Sentence Transformers embeddings and FAISS for similarity-based retrieval.
- **LLM-powered responses:** Uses LangChain and the OpenRouter API to generate clear answers from retrieved context.
- **Voice input:** Uses Faster-Whisper for speech-to-text.
- **Voice output:** Uses Edge TTS to read answers aloud in Hindi or English.
- **Source references:** Displays the source document and page information associated with retrieved passages.
- **Interactive interface:** Built with Streamlit.

## Technology Stack

| Area | Technology |
|---|---|
| Language | Python |
| Frontend | Streamlit |
| PDF extraction | PyMuPDF |
| Text chunking | LangChain Text Splitters |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Vector search | FAISS |
| LLM integration | LangChain, OpenRouter API |
| Speech-to-text | Faster-Whisper |
| Text-to-speech | Edge TTS |

## How It Works

```text
User asks a question (text or voice)
              |
              v
       Speech-to-text
       (voice input)
              |
              v
       Query embedding
              |
              v
      FAISS similarity search
              |
              v
   Retrieve relevant PDF passages
              |
              v
  LangChain + OpenRouter LLM
              |
              v
   Context-grounded answer
              |
       +------+------+
       |             |
       v             v
 Source references  Text-to-speech
                    (spoken answer)
```

## Project Structure

```text
Nivaran-AI/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── config/
├── data/
│   └── raw/
│       ├── cbfe_scheme.pdf
│       └── uuid_scheme2026.pdf
├── src/
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── rag_pipeline.py
│   ├── retriever.py
│   ├── speech_to_text.py
│   ├── text_splitter.py
│   ├── text_to_speech.py
│   └── vector_store.py
└── vectorstore/
    ├── nivaran.index
    └── chunks.pkl
```

## Setup and Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Nivaran-AI.git
cd Nivaran-AI
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=your_openrouter_model_name
```

Get an API key from [OpenRouter](https://openrouter.ai/). Do not commit your `.env` file or publish your API key.

### 5. Prepare the vector store (if it is not already included)

From the project root, run:

```bash
python -m src.vector_store
```

This processes the PDFs, creates text chunks and embeddings, and saves the FAISS index and chunk metadata in `vectorstore/`.

### 6. Launch the application

```bash
streamlit run app.py
```

Streamlit will provide a local URL in the terminal, usually `http://localhost:8501`.

## How to Use

1. Start the Streamlit application.
2. Enter a question about the government scheme documents, or use the voice-input option.
3. Review the generated answer and its source references.
4. Use the audio option to listen to the answer when available.

## Reliability and Scope

Nivaran AI is designed to answer using the documents available in its knowledge base. If relevant information is not retrieved, the LLM prompt instructs the assistant to say that the information could not be found rather than inventing scheme details.

The current knowledge base contains the UDID and CBFE PDFs included with this project. Answers are limited by the coverage, accuracy, and freshness of those documents. Always verify important eligibility, application, and benefit details with the relevant official government source.

## Future Improvements

- Add more verified government scheme documents.
- Improve multilingual retrieval and speech support.
- Add document upload and knowledge-base refresh workflows.
- Expand testing for retrieval quality, answer grounding, and accessibility.
- Deploy the application so it can be accessed online.

## Author

**Yash Roy**

- GitHub: [Yash702-roy](https://github.com/Yash702-roy)
- LinkedIn: [Yash Roy](https://www.linkedin.com/in/yash-roy-88620229a)

---

*Built to make public information more accessible through AI and voice technology.*
