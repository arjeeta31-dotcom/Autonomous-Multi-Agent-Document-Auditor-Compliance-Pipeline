# Implementation Steps

## 1. Build the ingestion layer

File: `src/ingestion.py`

This extracts text from:

- digital PDFs using `pypdf`
- scanned PDFs using PyMuPDF + Tesseract OCR
- images using Tesseract OCR
- plain text and Markdown files

Why it matters:

Real compliance documents are messy. Some are scanned, some are digital, and some have poor formatting.

## 2. Implement hierarchical chunking

File: `src/chunking.py`

The code first detects parent sections such as:

- Coverage
- Exclusions
- Premium
- Deductible
- Claims
- Diagnosis
- Rent
- Deposit

Then it creates child chunks inside each parent section.

Why it matters:

Hierarchical chunks preserve document structure better than blindly splitting every 1,000 characters.

## 3. Store chunks in persistent ChromaDB

File: `src/vector_store.py`

The project stores embeddings in `.chroma/`.

Why it matters:

Persistent vector storage allows repeated retrieval without rebuilding everything from scratch.

## 4. Use Llama-3-70B through Groq

File: `src/retrieval.py`

The RAG answer step uses:

```text
GROQ_MODEL=llama3-70b-8192
```

Why it matters:

Groq gives fast inference for Llama models, which makes the dashboard feel responsive.

## 5. Add deterministic Python tools

File: `src/deterministic_tools.py`

Tools check:

- impossible dates
- very large monetary values
- mismatched totals

Why it matters:

An LLM may miss arithmetic errors. Deterministic tools give reliable verification.

## 6. Create Phidata-style agent orchestration

File: `src/agents.py`

The workflow is divided into:

- compliance agent
- anomaly agent
- report agent

The project includes `phidata` as a dependency and checks whether Phidata imports successfully.

Why it matters:

This gives you an agentic architecture rather than a simple one-shot chatbot.

## 7. Build the Streamlit dashboard

File: `app.py`

The dashboard supports:

- document upload
- domain selection
- audit execution
- alert table
- rule evidence
- JSON report download

## 8. Add evaluation

File: `evals/evaluate_rag.py`

The script prepares RAGAS metrics:

- faithfulness
- answer relevancy
- context precision

Why it matters:

It proves you understand scientific LLM evaluation, not only prompt engineering.

