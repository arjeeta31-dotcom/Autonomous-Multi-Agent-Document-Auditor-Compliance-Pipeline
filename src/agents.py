from __future__ import annotations

from pathlib import Path

from src.chunking import hierarchical_chunk
from src.config import settings
from src.deterministic_tools import run_deterministic_checks
from src.ingestion import extract_document_text
from src.retrieval import RetrievalQA
from src.rules import load_rules
from src.vector_store import build_persistent_vector_store


SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


class AuditAgentTeam:
    """Agentic workflow inspired by Phidata teams.

    The project imports Phidata when available so your dependency and architecture
    match the resume. The core workflow remains explicit and reliable for a demo.
    """

    def __init__(self):
        self.phidata_available = self._check_phidata()

    def run(self, document_path: Path, domain: str) -> dict:
        text = extract_document_text(document_path)
        chunks = hierarchical_chunk(text)
        vector_store = build_persistent_vector_store(chunks, document_path.name)
        qa = RetrievalQA(vector_store)

        rule_results = self._run_compliance_agent(qa, domain)
        tool_results = self._run_anomaly_agent(text)
        alerts = self._merge_alerts(rule_results, tool_results)
        executive_summary = self._run_report_agent(document_path.name, domain, alerts, rule_results)

        return {
            "document": document_path.name,
            "domain": domain,
            "model": settings.groq_model,
            "phidata_available": self.phidata_available,
            "executive_summary": executive_summary,
            "alerts": alerts,
            "rule_results": rule_results,
            "tool_results": tool_results,
            "retrieval_stats": {
                "hierarchical_chunks": len(chunks),
                "persist_directory": settings.chroma_dir,
                "embedding_model": settings.embedding_model,
            },
        }

    def _run_compliance_agent(self, qa: RetrievalQA, domain: str) -> list[dict]:
        results = []
        for rule in load_rules(domain):
            answer = qa.ask(rule["question"])
            results.append(
                {
                    "rule_name": rule["name"],
                    "question": rule["question"],
                    "severity": rule["severity"],
                    "fail_message": rule["fail_message"],
                    "answer": answer["answer"],
                    "contexts": answer["contexts"],
                    "metadata": answer["metadata"],
                }
            )
        return results

    def _run_anomaly_agent(self, text: str) -> dict:
        return run_deterministic_checks(text)

    def _run_report_agent(self, document: str, domain: str, alerts: list[dict], rule_results: list[dict]) -> str:
        phidata_summary = self._try_phidata_report_agent(document, domain, alerts, rule_results)
        if phidata_summary:
            return phidata_summary

        high = [alert for alert in alerts if alert["severity"] in {"critical", "high"}]
        lines = [
            f"### Audit report for `{document}`",
            f"Domain: **{domain}**",
            f"Model: **{settings.groq_model}**",
            f"Total alerts: **{len(alerts)}**",
            f"Critical/high alerts: **{len(high)}**",
            "",
        ]
        if alerts:
            lines.append("Top findings:")
            for alert in alerts[:5]:
                lines.append(f"- **{alert['severity'].upper()}**: {alert['title']}")
        else:
            lines.append("No major issues were detected by the automated workflow.")
        lines.append("")
        lines.append(f"Compliance rules checked: **{len(rule_results)}**")
        lines.append("Human expert review is required before real-world use.")
        return "\n".join(lines)

    def _try_phidata_report_agent(
        self,
        document: str,
        domain: str,
        alerts: list[dict],
        rule_results: list[dict],
    ) -> str | None:
        try:
            from phi.agent import Agent
            from phi.model.groq import Groq

            agent = Agent(
                name="Compliance Report Agent",
                model=Groq(id=settings.groq_model),
                instructions=[
                    "You are a compliance audit report agent.",
                    "Summarize audit findings in clear Markdown.",
                    "Do not provide legal, medical, or financial advice.",
                    "Always recommend human expert review.",
                ],
                markdown=True,
            )
            prompt = (
                f"Document: {document}\n"
                f"Domain: {domain}\n"
                f"Alerts: {alerts[:8]}\n"
                f"Rules checked: {len(rule_results)}\n"
                "Create an executive summary with total risk level and top findings."
            )
            response = agent.run(prompt)
            return getattr(response, "content", str(response))
        except Exception:
            return None

    def _merge_alerts(self, rule_results: list[dict], tool_results: dict) -> list[dict]:
        alerts = []
        missing_markers = ["not_found", "not found", "missing", "unclear", "does not specify", "no evidence"]
        for result in rule_results:
            answer = result["answer"].lower()
            if any(marker in answer for marker in missing_markers):
                alerts.append(
                    {
                        "severity": result["severity"],
                        "category": "compliance",
                        "title": result["rule_name"],
                        "explanation": result["fail_message"],
                        "evidence": result["answer"],
                    }
                )
        alerts.extend(tool_results["all_alerts"])
        return sorted(alerts, key=lambda item: SEVERITY_ORDER.get(item["severity"], 9))

    def _check_phidata(self) -> bool:
        try:
            from phi.agent import Agent  # noqa: F401
            from phi.model.groq import Groq  # noqa: F401

            return True
        except Exception:
            return False
