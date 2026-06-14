from __future__ import annotations

import json
from pathlib import Path


RULE_PATH = Path(__file__).resolve().parents[1] / "data" / "compliance_rules.json"


def load_rules(domain: str) -> list[dict]:
    rules = json.loads(RULE_PATH.read_text(encoding="utf-8"))
    return rules.get(domain, rules["general"])

