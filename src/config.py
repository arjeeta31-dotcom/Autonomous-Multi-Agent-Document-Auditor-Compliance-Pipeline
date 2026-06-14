from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    groq_api_key: str | None = os.getenv("GROQ_API_KEY")
    groq_model: str = os.getenv("GROQ_MODEL", "llama3-70b-8192")
    chroma_dir: str = os.getenv("CHROMA_DIR", ".chroma")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


settings = Settings()


def require_groq_key() -> None:
    if not settings.groq_api_key:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to .env or Hugging Face Space secrets.")

