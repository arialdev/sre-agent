"""
Query pipeline for SRE runbook retrieval.

Loads the persisted ChromaDB vectorstore and exposes a retrieval function
that accepts a natural-language query (typically an error log line) and
returns the most relevant runbook excerpts.

This module provides:
- retrieve_context(): raw retrieval with relevance filtering.
- search_runbooks: a LangChain @tool wrapping retrieve_context, used by
  the ReAct agent in src/agent.py.
"""

import os
import sys
from pathlib import Path

os.environ["ANONYMIZED_TELEMETRY"] = "False"

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"


def load_vectorstore(persist_dir: Path = VECTORSTORE_DIR) -> Chroma:
    """Load the persisted ChromaDB vectorstore from disk."""
    load_dotenv()
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma(
        persist_directory=str(persist_dir),
        embedding_function=embeddings,
    )


def retrieve_context(
    query: str, k: int = 3, persist_dir: Path = VECTORSTORE_DIR
) -> str:
    """
    Retrieve relevant runbook context for a given query.

    Args:
        query: A natural-language description or raw error log line.
        k: Number of chunks to retrieve (default 3).
        persist_dir: Path to the ChromaDB persistence directory.

    Returns:
        A single string with the top-k relevant chunks joined by separator
        lines. This format is ready to be injected into an LLM prompt as
        context. The function returns str (not list[Document]) so it can be
        directly wrapped as a LangChain Tool with zero glue code.
    """
    vectorstore = load_vectorstore(persist_dir)
    # Use similarity_search_with_score to get distances (L2 by default, lower is better)
    results = vectorstore.similarity_search_with_score(query, k=k)

    # Filter out chunks that are practically irrelevant (distance > 1.25 is far in L2 space)
    filtered_results = [doc for doc, score in results if score <= 1.25]

    if not filtered_results:
        return "No relevant runbook context found."

    formatted = []
    for i, doc in enumerate(filtered_results, 1):
        source = doc.metadata.get("source", "unknown")
        formatted.append(
            f"--- Result {i} (source: {source}) ---\n{doc.page_content}"
        )
    return "\n\n".join(formatted)


@tool
def search_runbooks(query: str) -> str:
    """Search the SRE runbooks knowledge base for troubleshooting procedures.

    Use this tool when you need to find documented procedures, diagnosis steps,
    or resolution steps for a specific incident or error. The query should
    describe the problem or symptoms observed.

    Returns relevant runbook excerpts with source file references, or a message
    indicating no relevant context was found.
    """
    return retrieve_context(query)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Error: No query provided. Usage: python -m src.query \"your query\"")
        sys.exit(1)
        
    query = " ".join(sys.argv[1:])
    print(f"Query: {query}\n")
    print(retrieve_context(query))
