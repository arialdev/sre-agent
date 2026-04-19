"""
Query pipeline for SRE runbook retrieval.

Loads the persisted ChromaDB vectorstore and exposes a retrieval function
that accepts a natural-language query (typically an error log line) and
returns the most relevant runbook excerpts.

This module provides:
- retrieve_context(): raw retrieval with relevance filtering.
- search_runbooks: a LangChain @tool wrapping retrieve_context, used by
  the ReAct agent in `sre_agent.agent`.
"""

import json
import os
import sys
from pathlib import Path
from urllib import error, parse, request

from langchain_chroma import Chroma
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings

from sre_agent.config import (
    DEFAULT_RETRIEVAL_LIMIT,
    NO_CONTEXT_SENTINEL,
    OPENAI_EMBEDDING_MODEL,
    REMOTE_REQUEST_TIMEOUT_SECONDS,
    RETRIEVAL_DISTANCE_THRESHOLD,
    RUNBOOKS_API_BASE_URL_ENV,
    RUNBOOKS_API_QUERY_PATH,
    VECTORSTORE_DIR,
    load_project_env,
)


def load_vectorstore(persist_dir: Path = VECTORSTORE_DIR) -> Chroma:
    """Load the persisted ChromaDB vectorstore from disk."""
    load_project_env()
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)
    return Chroma(
        persist_directory=str(persist_dir),
        embedding_function=embeddings,
    )


def retrieve_context(
    query: str,
    k: int = DEFAULT_RETRIEVAL_LIMIT,
    persist_dir: Path = VECTORSTORE_DIR,
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
    load_project_env()
    remote_base_url = os.getenv(RUNBOOKS_API_BASE_URL_ENV)
    if remote_base_url:
        remote_context = retrieve_remote_context(remote_base_url, query, k)
        if remote_context is not None:
            return remote_context

    vectorstore = load_vectorstore(persist_dir)
    results = vectorstore.similarity_search_with_score(query, k=k)

    filtered_results = [
        doc for doc, score in results if score <= RETRIEVAL_DISTANCE_THRESHOLD
    ]

    if not filtered_results:
        return NO_CONTEXT_SENTINEL

    formatted = []
    for i, doc in enumerate(filtered_results, 1):
        source = doc.metadata.get("source", "unknown")
        formatted.append(
            f"--- Result {i} (source: {source}) ---\n{doc.page_content}"
        )
    return "\n\n".join(formatted)


def retrieve_remote_context(
    base_url: str,
    query: str,
    k: int = DEFAULT_RETRIEVAL_LIMIT,
) -> str | None:
    """
    Query the external runbook knowledge API.

    Returns:
        - A formatted retrieval context string when the request succeeds.
        - The sentinel string when the API returns no results.
        - None when the remote call fails, allowing local fallback.
    """
    normalized_base_url = base_url.rstrip("/")
    endpoint = parse.urljoin(
        f"{normalized_base_url}/", RUNBOOKS_API_QUERY_PATH
    )
    payload = json.dumps({"query": query, "limit": k}).encode("utf-8")
    http_request = request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(
            http_request, timeout=REMOTE_REQUEST_TIMEOUT_SECONDS
        ) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (error.URLError, TimeoutError, json.JSONDecodeError):
        return None

    results = body.get("results", [])
    if not results:
        return NO_CONTEXT_SENTINEL

    formatted = []
    for index, result in enumerate(results, 1):
        title = result.get("title", "unknown")
        source_filename = result.get("sourceFilename", "unknown")
        excerpt = result.get("excerpt", "")
        formatted.append(
            f"--- Result {index} (source: {title} / {source_filename}) ---\n{excerpt}"
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


def main() -> None:
    """Run the CLI query entrypoint."""
    if len(sys.argv) <= 1:
        print(
            'Error: No query provided. Usage: python -m sre_agent.query "your query"'
        )
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(f"Query: {query}\n")
    print(retrieve_context(query))


if __name__ == "__main__":
    main()
