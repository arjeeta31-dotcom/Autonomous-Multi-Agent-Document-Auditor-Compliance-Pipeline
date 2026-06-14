from __future__ import annotations

import re
from dataclasses import dataclass, asdict


@dataclass
class HierarchicalChunk:
    text: str
    parent_section: str
    section_index: int
    chunk_index: int
    level: str

    def metadata(self) -> dict:
        return asdict(self) | {"text": None}


SECTION_RE = re.compile(
    r"(?im)^(?:\d+\.?\s+)?(definitions|coverage|exclusions|premium|deductible|claim|medical history|diagnosis|treatment|rent|deposit|termination|maintenance|signature|terms|conditions)\b.*$"
)


def hierarchical_chunk(text: str, chunk_size: int = 900, overlap: int = 160) -> list[HierarchicalChunk]:
    sections = _split_sections(text)
    chunks: list[HierarchicalChunk] = []
    for section_index, (title, body) in enumerate(sections):
        child_chunks = _sliding_chunks(body, chunk_size=chunk_size, overlap=overlap)
        for chunk_index, chunk in enumerate(child_chunks):
            chunks.append(
                HierarchicalChunk(
                    text=chunk,
                    parent_section=title,
                    section_index=section_index,
                    chunk_index=chunk_index,
                    level="child",
                )
            )
    return chunks


def _split_sections(text: str) -> list[tuple[str, str]]:
    matches = list(SECTION_RE.finditer(text))
    if not matches:
        return [("full_document", text)]

    sections: list[tuple[str, str]] = []
    if matches[0].start() > 0:
        sections.append(("preamble", text[: matches[0].start()]))

    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        title = match.group(0).strip()[:120] or f"section_{idx}"
        sections.append((title, text[start:end]))
    return sections


def _sliding_chunks(text: str, chunk_size: int, overlap: int) -> list[str]:
    normalized = " ".join(text.split())
    if not normalized:
        return []
    chunks = []
    start = 0
    while start < len(normalized):
        end = min(len(normalized), start + chunk_size)
        chunks.append(normalized[start:end])
        if end == len(normalized):
            break
        start = max(0, end - overlap)
    return chunks

