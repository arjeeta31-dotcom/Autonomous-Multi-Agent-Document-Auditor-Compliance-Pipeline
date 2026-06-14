from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from src.agents import AuditAgentTeam
from src.config import settings


st.set_page_config(page_title="Agentic RAG Compliance Auditor", layout="wide")

st.title("Agentic RAG PDF Compliance Auditor")
st.caption("Phidata-style agents + Llama-3-70B via Groq + hierarchical ChromaDB retrieval")


with st.sidebar:
    st.header("Configuration")
    domain = st.selectbox("Audit domain", ["insurance", "medical", "rental", "general"])
    st.write("Model:", settings.groq_model)
    st.write("Vector DB:", settings.chroma_dir)
    st.info("Add GROQ_API_KEY in .env locally or as a Hugging Face Space secret.")


uploaded_file = st.file_uploader(
    "Upload an unstructured document",
    type=["pdf", "txt", "md", "png", "jpg", "jpeg"],
)

run = st.button("Run Compliance Audit", type="primary", disabled=uploaded_file is None)

if run and uploaded_file:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / uploaded_file.name
        path.write_bytes(uploaded_file.getbuffer())

        team = AuditAgentTeam()
        with st.spinner("Extracting, chunking, indexing, retrieving evidence, and running agents..."):
            report = team.run(path, domain)

    st.subheader("Executive Audit Summary")
    st.markdown(report["executive_summary"])

    st.subheader("Flagged Anomaly Alerts")
    alerts = report["alerts"]
    if alerts:
        st.dataframe(pd.DataFrame(alerts), use_container_width=True, hide_index=True)
    else:
        st.success("No major alerts detected. Human review is still recommended.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Deterministic Tool Results")
        st.json(report["tool_results"])
    with col2:
        st.subheader("Retrieval Stats")
        st.json(report["retrieval_stats"])

    st.subheader("Rule-by-Rule Evidence")
    for result in report["rule_results"]:
        with st.expander(result["rule_name"]):
            st.write("Question:", result["question"])
            st.write("Answer:", result["answer"])
            st.write("Severity:", result["severity"])
            st.write("Evidence:")
            for context in result["contexts"]:
                st.code(context[:1200])

    st.subheader("Raw JSON Report")
    st.download_button(
        "Download audit_report.json",
        data=json.dumps(report, indent=2),
        file_name="audit_report.json",
        mime="application/json",
    )
    st.code(json.dumps(report, indent=2), language="json")

