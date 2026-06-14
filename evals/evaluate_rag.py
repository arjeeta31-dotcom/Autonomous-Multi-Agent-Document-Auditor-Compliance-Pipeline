from __future__ import annotations

import sys
from pathlib import Path

from datasets import Dataset

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.chunking import hierarchical_chunk
from src.ingestion import extract_document_text
from src.retrieval import RetrievalQA
from src.vector_store import build_persistent_vector_store


QUESTIONS = [
    "Who is the policyholder or primary party?",
    "What is the policy or document number?",
    "What are the effective dates?",
    "What monetary amounts are listed?",
    "What exclusions or limitations are disclosed?",
]


def main(document_path: str, domain: str):
    path = Path(document_path)
    text = extract_document_text(path)
    chunks = hierarchical_chunk(text)
    vector_store = build_persistent_vector_store(chunks, path.name)
    qa = RetrievalQA(vector_store)

    rows = []
    for question in QUESTIONS:
        result = qa.ask(question)
        rows.append(
            {
                "question": question,
                "answer": result["answer"],
                "contexts": result["contexts"],
                "ground_truth": "Replace this with a human-written reference answer for serious evaluation.",
            }
        )

    dataset = Dataset.from_list(rows)
    try:
        from ragas import evaluate
        from ragas.metrics import answer_relevancy, context_precision, faithfulness

        scores = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision])
        print(scores)
    except Exception as exc:
        print("RAGAS could not run. Raw evaluation dataset follows.")
        print(f"Reason: {exc}")
        print(dataset)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python evals/evaluate_rag.py path/to/document.pdf insurance")
        raise SystemExit(1)
    main(sys.argv[1], sys.argv[2])

