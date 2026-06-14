from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class AuditAlert:
    severity: str
    category: str
    title: str
    explanation: str
    evidence: str

    def to_dict(self) -> dict:
        return asdict(self)

