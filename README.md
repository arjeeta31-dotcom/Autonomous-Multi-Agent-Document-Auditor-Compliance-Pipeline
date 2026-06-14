# Agentic RAG PDF Compliance Auditor

An autonomous **Agentic RAG** project that audits messy unstructured PDFs for compliance issues. It uses:

- **Phidata-style agents** for compliance, anomaly, and report generation workflows
- **Llama-3-70B through Groq** for fast LLM reasoning
- **Hierarchical text chunking** for better retrieval
- **Persistent ChromaDB** vector storage
- **Deterministic Python tools** for dates, money, totals, and missing clauses
- **Streamlit dashboard** ready for **Hugging Face Spaces**
- **RAGAS-style evaluation** to benchmark retrieval quality

> Disclaimer: This is an educational portfolio project. It is not legal, medical, insurance, or financial advice.

## Resume Bullet This Project Supports

```text
Built an Agentic RAG pipeline using Phidata and Llama-3-70B to automate unstructured PDF compliance audits.

Implemented hierarchical text chunking with a persistent ChromaDB vector backend to optimize context retrieval.

Equipped the LLM with deterministic Python tools to cross-verify document data and eliminate calculation errors.

Deployed a live interactive web dashboard using Streamlit hosted on Hugging Face Spaces.
```

## Quick Start On Your Computer

Open PowerShell:

```powershell
cd C:\Users\asus\Documents\Codex\2026-06-14\project-title-automated-multimodal-legal-medical\outputs\phidata_llama3_streamlit_auditor
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Open `.env` and add your Groq key:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-70b-8192
```

Run:

```powershell
streamlit run app.py
```

Open the local URL shown in terminal, usually:

```text
http://localhost:8501
```

## Test The Demo

Upload:

```text
samples/sample_insurance_policy.txt
```

Choose:

```text
insurance
```

Click:

```text
Run Compliance Audit
```

You should see:

- severity-ranked alerts
- retrieved evidence
- deterministic anomaly checks
- final AI audit summary

## Hugging Face Spaces Deployment

1. Create a new Space on Hugging Face.
2. Select **Streamlit** as the SDK.
3. Upload all project files except local/private/generated files.
4. In Space settings, add repository secrets:

```text
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-70b-8192
```

5. Hugging Face will run:

```bash
streamlit run app.py
```

## Project Structure

```text
app.py                          Streamlit dashboard
requirements.txt                Python dependencies
packages.txt                    Linux packages for HF Spaces OCR support
.env.example                    Environment variable template
.gitignore                      Files that should not go to GitHub
src/config.py                   Settings
src/ingestion.py                PDF/image/text extraction
src/chunking.py                 Hierarchical chunking
src/vector_store.py             Persistent ChromaDB backend
src/retrieval.py                RAG retrieval and answer generation
src/deterministic_tools.py      Python validation tools
src/agents.py                   Phidata-style agent orchestration
src/schemas.py                  Structured dataclasses
data/compliance_rules.json      Audit checklist rules
samples/sample_insurance_policy.txt
evals/evaluate_rag.py           RAGAS-style evaluation workflow
docs/GITHUB_UPLOAD_GUIDE.md     What to upload and what each file means
docs/IMPLEMENTATION_STEPS.md    Full build explanation
```

## Evaluation

After installing dependencies and adding your API key:

```powershell
python evals/evaluate_rag.py samples/sample_insurance_policy.txt insurance
```

For serious benchmarking, replace the placeholder ground-truth answers with human-written reference answers.

