# Autonomous Multi-Agent Document Auditor & Compliance Pipeline

An enterprise-grade **Agentic RAG (Retrieval-Augmented Generation)** application designed to ingest, process, and audit complex, unstructured files for compliance anomalies. Powered by **Phidata/Agno** multi-agent orchestration and **Llama-3-70B via Groq**, this system eliminates natural language calculation blind spots by equipping autonomous agents with deterministic code execution tools.

## Key Features

- **Agentic Orchestration:** Specialized Phidata compliance, anomaly detection, and reporting agents working asynchronously as a cohesive team.
- **Hierarchical Text Processing:** Optimizes contextual density through chunking strategies engineered to preserve structural semantics within lengthy files.
- **Hybrid Vector Data Management:** Local, persistent **ChromaDB** architecture coupled with a local **SentenceTransformer** embedding layer (`all-mpnet-base-v2`) for free, secure vector calculations.
- **Deterministic Evaluation Tools:** Plugs custom Python runtimes directly into the LLM context loop, forcing the model to calculate mathematical matrices via absolute logic instead of textual guessing.
- **Production MLOps & Evaluation Framework:** Natively supports automated validation workflows using an internal **RAGAS-style evaluation suite** to benchmark retrieval exactness.

---

## System Architecture

```text
    ┌──────────────────────────────┐
    │  Unstructured Document Input │ (PDF, TXT, MD, Images via Tesseract OCR)
    └──────────────┬───────────────┘
                   │
                   ▼
    ┌──────────────────────────────┐
    │     Ingestion & Parsing      │ (PyMuPDF / PyPDF Stream Controllers)
    └──────────────┬───────────────┘
                   │
                   ▼
    ┌──────────────────────────────┐
    │  Hierarchical Chunking Layer │ (Text Splitter + Token Context Windows)
    └──────────────┬───────────────┘
                   │
                   ▼
    ┌──────────────────────────────┐
    │      ChromaDB Vector DB      │ (Local Persistent Embedding Database)
    └──────────────┬───────────────┘
                   │
                   ▼
    ┌──────────────────────────────┐
    │   CHIEF AUDITOR TEAM (LLM)   │ ◄─── Managed via Groq / Llama-3-70B
    └──────┬──────────────┬────────┘
           │              │
           ▼              ▼
    ┌─────────────┐┌─────────────┐
    │ Python Math ││ DuckDuckGo  │ ◄─── Deterministic Agent Tools
    │ Calculator  ││ Web Search  │
    └──────┬──────┘└──────┬──────┘
           │              │
           └──────┬───────┘
                  ▼
    ┌──────────────────────────────┐
    │  Streamlit Cloud Dashboard   │ (Live Interactive Flagging Interface)
    └──────────────────────────────┘


## Project Repository Anatomy

├── app.py                     # Streamlit frontend application dashboard
├── requirements.txt           # Explicit Python system dependencies
├── packages.txt               # Linux system binaries for OCR and PDF rendering on HF Cloud
├── .env.example               # Environment variables configuration template
├── .gitignore                 # Prevents local credentials and heavy caches from tracking
├── src/                       # Production application source code modules
│   ├── config.py              # Environment and global operational parameters
│   ├── ingestion.py           # Multi-format raw data text extraction engines
│   ├── chunking.py            # Structural text chunk splitting algorithms
│   ├── vector_store.py        # Persistent Vector database mapping interfaces
│   ├── retrieval.py           # Intelligent context window compilation logic
│   ├── deterministic_tools.py # Deterministic execution tools given to the agents
│   ├── agents.py              # Multi-agent teams layout and prompt engineering blocks
│   └── schemas.py             # Structured Pydantic validator classes for JSON data 
├── data/                      # Local system runtime assets
│   └── compliance_rules.json  # Base evaluation metrics for domain audits
├── samples/                   # Pre-compiled multi-domain test datasets
│   └── sample_insurance_policy.txt
└── evals/                     # Pipeline assessment frameworks
    └── evaluate_rag.py        # Automated validation framework for benchmarking

