from __future__ import annotations

from langchain_groq import ChatGroq

from src.config import require_groq_key, settings


class RetrievalQA:
    def __init__(self, vector_store):
        require_groq_key()
        self.retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        self.llm = ChatGroq(model=settings.groq_model, temperature=0, api_key=settings.groq_api_key)

    def ask(self, question: str) -> dict:
        docs = self.retriever.invoke(question)
        context = "\n\n".join(
            f"[section={doc.metadata.get('parent_section')}, chunk={doc.metadata.get('chunk_index')}]\n{doc.page_content}"
            for doc in docs
        )
        prompt = (
            "You are a compliance audit assistant. Answer only from the provided context. "
            "If evidence is missing, say exactly: NOT_FOUND. Keep the answer concise and cite the evidence.\n\n"
            f"Question: {question}\n\nContext:\n{context}"
        )
        response = self.llm.invoke(prompt).content
        return {
            "question": question,
            "answer": response,
            "contexts": [doc.page_content for doc in docs],
            "metadata": [doc.metadata for doc in docs],
        }

