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
```

## Project Repository Anatomy

```text
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

```

## Quick Start Local Configuration
- **Initialize Virtual Environment & System Requirements**
Execute the following steps inside your terminal to safely provision the background environment variables:

# Clone or move into the project directory
cd project-directory-path

# Create and trigger the virtual python sandbox
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install exact lock dependencies
pip install -r requirements.txt

- **Manage API Passwords**
# Duplicate the sample environment blueprint file and append your private keys safely:

copy .env.example .env

# Open your newly populated .env file and verify your tokens are cleanly registered:

GROQ_API_KEY=gsk_your_actual_private_groq_key_here
GROQ_MODEL=llama3-70b-8192

- **Initialize The Application UI**
# Launch the native web interface server locally on your browser:

streamlit run app.py

Your console will output your local instance routing connection, typically loaded at: http://localhost:8501

- **Pipeline Diagnostics & Quality Testing**
# To execute an automated quality check run on the underlying retriever mechanisms against standard target checklists, execute the evaluation script directly:

python evals/evaluate_rag.py samples/sample_insurance_policy.txt insurance

The system will parse your target documentation asset, run real-time multi-agent queries, cross-verify compliance criteria arrays dynamically, and dump an immutable structured JSON log mapping correctness data metrics.

- **Cloud Infrastructure Deployment (Hugging Face Spaces)**

This project is configured out-of-the-box to run directly on secure container infrastructure tiers:

Initialize a new Space on the Hugging Face hub selecting Streamlit as the baseline application SDK.

Commit your source directories (src/, data/, evals/, samples/) alongside root control configurations (app.py, requirements.txt, packages.txt).

Move to the Spaces Settings UI, expand the Variables and secrets component, and append your production variables:

GROQ_API_KEY = gsk_...

GROQ_MODEL = llama3-70b-8192

The system builder reads packages.txt to safely provision OCR (tesseract-ocr) and file stream binaries (poppler-utils) automatically.

Disclaimer: This repository is developed entirely as a technical portfolio engineering project. The calculations and insights rendered do not constitute binding financial, legal, medical, or corporate compliance advice.
