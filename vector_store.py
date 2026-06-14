from __future__ import annotations

import hashlib
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

from src.chunking import HierarchicalChunk
from src.config import settings


def build_persistent_vector_store(chunks: list[HierarchicalChunk], source_name: str) -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    collection_name = _collection_name(source_name, chunks)
    docs = [
        Document(
            page_content=chunk.text,
            metadata={
                "source": source_name,
                "parent_section": chunk.parent_section,
                "section_index": chunk.section_index,
                "chunk_index": chunk.chunk_index,
                "level": chunk.level,
            },
        )
        for chunk in chunks
    ]
    return Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=settings.chroma_dir,
    )


def _collection_name(source_name: str, chunks: list[HierarchicalChunk]) -> str:
    joined = source_name + "".join(chunk.text[:100] for chunk in chunks[:10])
    digest = hashlib.sha1(joined.encode("utf-8", errors="ignore")).hexdigest()[:12]
    safe_stem = Path(source_name).stem.lower().replace(" ", "_")[:24]
    return f"audit_{safe_stem}_{digest}"

