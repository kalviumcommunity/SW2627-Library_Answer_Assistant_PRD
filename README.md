
# University Library Research Assistant

An academic library research assistant prototype that helps university students find **concise, citation-backed answers** from a small collection of research papers using traceable document ingestion and retrieval.

## Problem

University libraries contain large collections of academic documents, but students often have to search through dozens of unrelated papers and materials to find one specific answer.

## Solution

The current system retrieves relevant academic content with local MiniLM embeddings
and a persistent ChromaDB index, then displays supporting sources and citations
alongside a grounded backend-generated response.

### How It Works

```text
Student Question
      ↓
Backend API
      ↓
RAG Retrieval
      ↓
Relevant Academic Sources
      ↓
    Grounded Answer + Citations
```

## Key Features

* 🔎 Search across six processed academic documents
* 🧭 Traceable page-level evidence
* 📚 Research papers, theses, and course materials
* 📌 Citation-backed responses
* 🎯 Metadata-based filtering
* 🚫 No-evidence/refusal handling
* 📄 Source and document viewing
* 🔐 Environment-based secret management

## Tech Stack

**Backend**

* Python
* REST API

**AI / RAG (current implementation)**

* PyMuPDF extraction
* Cleaning and metadata
* Configurable chunking
* Local MiniLM embeddings and ChromaDB semantic retrieval

**Data & Testing**

* Academic document corpus
* Python testing framework
* RAG evaluation metrics

**Development**

* Git
* GitHub
* Feature branches
* Pull Requests

## Project Structure

```text
University-Library-RAG/
├── backend/       # API and AI integration
├── rag/           # Ingestion, retrieval, generation & evaluation
├── data/          # Raw, processed and sample documents
├── tests/         # Backend, RAG & integration tests
├── docs/          # PRD, architecture, API & evaluation docs
├── scripts/       # Ingestion and evaluation scripts
├── .env.example
├── requirements.txt
└── README.md
```

## Team Responsibilities

| Role                   | Responsibility                                                                |
| ---------------------- | ----------------------------------------------------------------------------- |
| AI/RAG Engineer        | Ingestion, chunking, embeddings, retrieval, grounding, citations & evaluation |
| Backend/AI Integration | API, RAG integration, LLM orchestration, streaming, errors & infrastructure   |

## Development Workflow

```text
Issue
  ↓
Feature Branch
  ↓
Implement + Test
  ↓
Pull Request
  ↓
Code Review
  ↓
Merge to main
```

`main` is protected. All development happens through feature branches and reviewed PRs.

## Documentation

Detailed project documentation is available in:

* `docs/PRD.md` — Product requirements
* `docs/ARCHITECTURE.md` — System architecture
* `docs/RAG_DESIGN.md` — RAG design
* `API_CONTRACT.md` — Backend/API contract
* `docs/EVALUATION.md` — Planned RAG evaluation strategy
* `docs/CONTRIBUTING.md` — Development workflow

## Project Goal

> **Ask → Retrieve → Explain → Cite**

The goal is to make academic research faster, clearer, and more reliable while ensuring that answers remain grounded in the university's available sources.

## Run locally

From the repository root, install dependencies and process the PDFs:

```powershell
python -m pip install -r requirements.txt
python -m scripts.process_documents
python -m scripts.build_index
```

Start the backend in one terminal:

```powershell
python -m uvicorn Backend.main:app --host 127.0.0.1 --port 8000
```

Run the tests with `python -m pytest -q`.

## Run the Streamlit UI

The Streamlit frontend calls the FastAPI backend and displays grounded answers
with expandable citations. Install the frontend dependency:

```powershell
python -m pip install -r requirements.txt
```

Build the local document index if it has not been built yet:

```powershell
python -m scripts.process_documents
python -m scripts.build_index
```

Create a local `.env` file. The default example tries Grok first and falls back
to Gemini when the first provider is unavailable:

```env
LLM_PROVIDER=grok
LLM_FALLBACK_PROVIDER=gemini
GROK_API_KEY=your_xai_api_key_here
GROK_MODEL=grok-3-mini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

`GROK_API_KEY` is sent to xAI's OpenAI-compatible API endpoint, while
`GEMINI_API_KEY` is sent to Google's Gemini API. If Grok fails because of an
invalid key, timeout, provider error, or invalid response, the service tries
Gemini. If you only want one provider, leave `LLM_FALLBACK_PROVIDER` empty.

Start the backend in one terminal:

```powershell
python -m uvicorn Backend.main:app --host 127.0.0.1 --port 8000
```

Start Streamlit from the repository root in a second terminal:

```powershell
streamlit run app.py
```

Open the address shown by Streamlit, normally
`http://localhost:8501`. The backend URL can be changed with the
`BACKEND_URL` environment variable.

## Current limitations

The embedding model is downloaded by Chroma on first index creation and the local
vector index is ignored by Git; run
`python -m scripts.build_index` after cloning. Formal evaluation is available
through `python -m scripts.evaluate_retrieval`.

The checked-in metadata catalog currently covers six research papers and the
local processing pipeline produced 528 indexed chunks from them.

Chroma uses cosine distance for its collection. Retrieval converts that value
to a higher-is-better cosine similarity score with `score = 1 - distance`.
General retrieval currently requires a calibrated minimum score of `0.40`;
document-scoped investigation uses `0.25` because its candidate set is already
restricted to one selected source.
