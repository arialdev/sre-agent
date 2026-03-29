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
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

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


def answer_query(
    query: str, k: int = 3, persist_dir: Path = VECTORSTORE_DIR
) -> str:
    """
    Answer the SRE query in natural language using the retrieved runbook context and internal knowledge.

    Args:
        query: A natural-language description or raw error log line.
        k: Number of chunks to retrieve (default 3).
        persist_dir: Path to the ChromaDB persistence directory.

    Returns:
        A natural language response from the LLM based on the context and its own knowledge.
    """
    context = retrieve_context(query, k, persist_dir)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    if context == "No relevant runbook context found.":
        system_prompt = (
            "You are an expert Kubernetes Site Reliability Engineer (SRE). "
            "Your task is to provide a complete analysis to diagnose and resolve the issue. "
            "Format your output entirely in Markdown. "
            "Because no runbook context is available, rely entirely on your general SRE knowledge."
        )
        warning_prefix = "> [!WARNING]\n> **No runbook context found.** The following analysis is based entirely on general model knowledge.\n\n"
    else:
        system_prompt = (
            "You are an expert Kubernetes Site Reliability Engineer (SRE). "
            "Your task is to provide a complete analysis to diagnose and resolve the issue. "
            "You must base your analysis on BOTH the provided runbook context AND your own domain knowledge. "
            "Format your output entirely in Markdown. "
            "Whenever you use or reference information from the runbook context, you MUST explicitly cite the source "
            "(e.g., referencing the file path and the specific heading or section)."
        )
        warning_prefix = ""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Problem: {query}\n\nRunbook Context:\n{context}")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({"query": query, "context": context})
    return warning_prefix + response.content



if __name__ == "__main__":
    query = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "database connection refused error in production"
    )
    print(f"Query: {query}\n")
    print(answer_query(query))
