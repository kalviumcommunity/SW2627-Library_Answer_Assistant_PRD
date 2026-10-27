"""Streamlit frontend for the University Library Research Assistant."""

from __future__ import annotations

import os
from html import escape
from pathlib import Path
from typing import Any

import httpx
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
METADATA_PATH = PROJECT_ROOT / "data" / "document_metadata.csv"
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
NO_EVIDENCE_MESSAGE = "No supporting evidence was found in the library documents."


st.set_page_config(
    page_title="Library Answer Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css() -> None:
    st.markdown(
        """
        <style>
        .block-container { max-width: 1180px; padding-top: 2rem; }
        .hero {
            padding: 1.5rem 1.75rem;
            border-radius: 1rem;
            background: linear-gradient(135deg, #17324d 0%, #285b75 100%);
            color: white;
            margin-bottom: 1.5rem;
        }
        .hero h1 { margin: 0 0 .35rem 0; color: white; }
        .hero p { margin: 0; color: #e6f3f7; font-size: 1.05rem; }
        .answer-card {
            padding: 1.25rem 1.5rem;
            border: 1px solid #d9e3ea;
            border-radius: .85rem;
            background: #f8fbfc;
            margin: .75rem 0 1.25rem 0;
        }
        .source-label {
            color: #536773;
            font-size: .9rem;
            margin-bottom: .5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_metadata() -> pd.DataFrame:
    """Load the catalog used to populate supported search filters."""
    if not METADATA_PATH.is_file():
        return pd.DataFrame()
    return pd.read_csv(METADATA_PATH)


def backend_health() -> bool:
    try:
        response = httpx.get(f"{BACKEND_URL}/health", timeout=3.0)
        return response.is_success and response.json().get("status") == "ok"
    except (httpx.HTTPError, ValueError):
        return False


def ask_backend(question: str, filters: dict[str, Any]) -> dict[str, Any]:
    try:
        response = httpx.post(
            f"{BACKEND_URL}/chat",
            json={"question": question, "filters": filters},
            timeout=90.0,
        )
    except httpx.ConnectError as exc:
        raise RuntimeError(
            "The backend is not running. Start FastAPI with "
            "`python -m uvicorn Backend.main:app --host 127.0.0.1 --port 8000`."
        ) from exc
    except httpx.TimeoutException as exc:
        raise RuntimeError(
            "The backend request timed out. Please try the question again."
        ) from exc
    except httpx.HTTPError as exc:
        raise RuntimeError(f"Could not contact the backend: {exc}") from exc

    if response.is_error:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise RuntimeError(f"Backend error ({response.status_code}): {detail}")

    try:
        payload = response.json()
    except ValueError as exc:
        raise RuntimeError("The backend returned an invalid response.") from exc

    if not isinstance(payload, dict):
        raise RuntimeError("The backend returned an unexpected response shape.")
    return payload


def render_citation(citation: dict[str, Any]) -> None:
    citation_id = citation.get("citation_id", "?")
    title = citation.get("title") or citation.get("document_id") or "Library document"
    details = []
    if citation.get("page") is not None:
        details.append(f"page {citation['page']}")
    if citation.get("section"):
        details.append(str(citation["section"]))
    if citation.get("score") is not None:
        details.append(f"similarity {float(citation['score']):.2f}")

    heading = f"[{citation_id}] {title}"
    if details:
        heading += " · " + " · ".join(details)

    with st.expander(heading):
        if citation.get("author"):
            st.markdown(f"**Author:** {citation['author']}")
        st.markdown(
            '<div class="source-label">Retrieved evidence</div>',
            unsafe_allow_html=True,
        )
        st.write(citation.get("excerpt") or "No excerpt was returned.")
        if citation.get("source_url"):
            st.markdown(f"[Open the original source]({citation['source_url']})")
        if citation.get("chunk_id"):
            st.caption(f"Chunk: {citation['chunk_id']}")


def build_filters(
    document: str,
    document_type: str,
    year: str,
    author: str,
) -> dict[str, Any]:
    filters: dict[str, Any] = {}
    if document != "All documents":
        filters["document_id"] = document
    if document_type != "All types":
        filters["document_type"] = document_type
    if year != "All years":
        filters["year"] = int(year)
    if author != "All authors":
        filters["author"] = author
    return filters


def render_sidebar(metadata: pd.DataFrame) -> dict[str, Any]:
    with st.sidebar:
        st.header("Search filters")
        st.caption("Narrow retrieval to a particular part of the library.")

        if metadata.empty:
            st.warning("Document catalog is unavailable.")
            document_options = ["All documents"]
            type_options = ["All types"]
            year_options = ["All years"]
            author_options = ["All authors"]
        else:
            document_options = ["All documents"] + sorted(
                metadata["document_id"].dropna().astype(str).unique()
            )
            type_options = ["All types"] + sorted(
                metadata["document_type"].dropna().astype(str).unique()
            )
            year_options = ["All years"] + [
                str(year)
                for year in sorted(
                    metadata["year"].dropna().astype(int).unique(), reverse=True
                )
            ]
            author_options = ["All authors"] + sorted(
                metadata["author"].dropna().astype(str).unique()
            )

        document = st.selectbox("Document", document_options)
        document_type = st.selectbox("Document type", type_options)
        year = st.selectbox("Year", year_options)
        author = st.selectbox("Author", author_options)

        st.divider()
        st.subheader("Backend")
        if backend_health():
            st.success("Connected")
        else:
            st.error("Offline")
        st.caption(BACKEND_URL)

        if st.button("Clear conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    return build_filters(document, document_type, year, author)


def render_message(message: dict[str, Any]) -> None:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and message.get("has_evidence"):
            st.markdown(
                f'<div class="answer-card">{escape(message["content"])}</div>',
                unsafe_allow_html=True,
            )
            citations = message.get("citations", [])
            st.markdown(f"**Sources ({len(citations)})**")
            for citation in citations:
                render_citation(citation)
        else:
            st.markdown(message["content"])


def main() -> None:
    load_css()
    metadata = load_metadata()
    filters = render_sidebar(metadata)

    st.markdown(
        """
        <div class="hero">
            <h1>📚 Library Answer Assistant</h1>
            <p>Ask research questions and verify concise answers against academic sources.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        st.info(
            "Try questions such as **What is retrieval augmented generation?** "
            "or **What is self-attention?**"
        )

    for message in st.session_state.messages:
        render_message(message)

    question = st.chat_input("Ask a question about the library documents...")
    if not question:
        return

    st.session_state.messages.append({"role": "user", "content": question})
    render_message(st.session_state.messages[-1])

    with st.chat_message("assistant"):
        with st.spinner("Searching the library and preparing a cited answer..."):
            try:
                result = ask_backend(question.strip(), filters)
            except RuntimeError as exc:
                st.error(str(exc))
                st.session_state.messages.append(
                    {"role": "assistant", "content": str(exc)}
                )
                return

        answer = str(result.get("answer", "")).strip()
        has_evidence = bool(result.get("has_evidence"))
        citations = result.get("citations", [])

        if not has_evidence:
            st.warning(answer or NO_EVIDENCE_MESSAGE)
        else:
            st.markdown(
                f'<div class="answer-card">{escape(answer)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(f"**Sources ({len(citations)})**")
            for citation in citations:
                render_citation(citation)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer or NO_EVIDENCE_MESSAGE,
                "has_evidence": has_evidence,
                "citations": citations,
            }
        )


if __name__ == "__main__":
    main()
