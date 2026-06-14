from __future__ import annotations

import re
from datetime import datetime
from decimal import Decimal, InvalidOperation

from src.schemas import AuditAlert


MONEY_RE = re.compile(r"(?:INR|Rs\.?|\$)?\s*([0-9][0-9,]*(?:\.[0-9]{1,2})?)", re.IGNORECASE)
DATE_RE = re.compile(r"\b(?:\d{4}-\d{1,2}-\d{1,2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b")


def run_deterministic_checks(text: str) -> dict:
    money_alerts = detect_money_anomalies(text)
    date_alerts = detect_date_anomalies(text)
    calculation_alerts = verify_financial_calculations(text)
    return {
        "money_alerts": [alert.to_dict() for alert in money_alerts],
        "date_alerts": [alert.to_dict() for alert in date_alerts],
        "calculation_alerts": [alert.to_dict() for alert in calculation_alerts],
        "all_alerts": [alert.to_dict() for alert in money_alerts + date_alerts + calculation_alerts],
    }


def detect_money_anomalies(text: str) -> list[AuditAlert]:
    alerts = []
    for value, evidence in _amounts_with_evidence(text):
        if value >= Decimal("1000000"):
            alerts.append(
                AuditAlert(
                    severity="medium",
                    category="financial",
                    title="Large monetary value detected",
                    explanation=f"Detected amount {value}. Verify comma placement, policy limit, premium, or deposit basis.",
                    evidence=evidence,
                )
            )
    return alerts


def detect_date_anomalies(text: str) -> list[AuditAlert]:
    alerts = []
    now = datetime.now()
    for match in DATE_RE.finditer(text):
        parsed = _parse_date(match.group(0))
        if not parsed:
            alerts.append(
                AuditAlert(
                    severity="high",
                    category="date",
                    title="Invalid date format or impossible date",
                    explanation=f"Could not parse date value: {match.group(0)}.",
                    evidence=_window(text, match.start(), match.end()),
                )
            )
            continue
        if parsed.year < 1950 or parsed.year > now.year + 20:
            alerts.append(
                AuditAlert(
                    severity="high",
                    category="date",
                    title="Implausible date detected",
                    explanation=f"Date {parsed.date()} is outside the expected range.",
                    evidence=_window(text, match.start(), match.end()),
                )
            )
    return alerts


def verify_financial_calculations(text: str) -> list[AuditAlert]:
    alerts = []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for idx, line in enumerate(lines):
        lower = line.lower()
        if "total" not in lower:
            continue
        total = _first_amount(line)
        if total is None:
            continue
        nearby = "\n".join(lines[max(0, idx - 5) : idx])
        components = [_first_amount(row) for row in nearby.splitlines()]
        components = [value for value in components if value is not None]
        if len(components) < 2:
            continue
        calculated = sum(components)
        if abs(calculated - total) > Decimal("1.00"):
            alerts.append(
                AuditAlert(
                    severity="high",
                    category="calculation",
                    title="Financial total mismatch",
                    explanation=f"Nearby line items sum to {calculated}, but stated total is {total}.",
                    evidence=nearby + "\n" + line,
                )
            )
    return alerts


def _amounts_with_evidence(text: str) -> list[tuple[Decimal, str]]:
    values = []
    for match in MONEY_RE.finditer(text):
        try:
            amount = Decimal(match.group(1).replace(",", ""))
        except InvalidOperation:
            continue
        if amount >= Decimal("100"):
            values.append((amount, _window(text, match.start(), match.end())))
    return values


def _first_amount(text: str) -> Decimal | None:
    match = MONEY_RE.search(text)
    if not match:
        return None
    try:
        return Decimal(match.group(1).replace(",", ""))
    except InvalidOperation:
        return None


def _parse_date(raw: str) -> datetime | None:
    for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%m-%d-%Y", "%d/%m/%y", "%m/%d/%y"]:
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            pass
    return None


def _window(text: str, start: int, end: int, radius: int = 120) -> str:
    return " ".join(text[max(0, start - radius) : min(len(text), end + radius)].split())

