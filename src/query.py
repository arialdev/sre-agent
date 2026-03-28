"""
Query pipeline for SRE runbook retrieval.

Loads the persisted ChromaDB vectorstore and exposes a retrieval function
that accepts a natural-language query (typically an error log line) and
returns the most relevant runbook excerpts.

The retrieve_context function is designed to be wrapped as a LangChain Tool
so a future Agent can call it autonomously:

    from langchain.tools import tool

    @tool
    def search_runbooks(query: str) -> str:
        \"\"\"Search SRE runbooks for relevant troubleshooting steps.\"\"\"
        return retrieve_context(query)
"""

import os
import sys
from pathlib import Path

os.environ["ANONYMIZED_TELEMETRY"] = "False"

from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
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
    results = vectorstore.similarity_search(query, k=k)

    if not results:
        return "No relevant runbook context found."

    formatted = []
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "unknown")
        formatted.append(
            f"--- Result {i} (source: {source}) ---\n{doc.page_content}"
        )
    return "\n\n".join(formatted)


if __name__ == "__main__":
    query = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "database connection refused error in production"
    )
    print(f"Query: {query}\n")
    print(retrieve_context(query))
