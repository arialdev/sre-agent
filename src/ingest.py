"""
Ingestion pipeline for SRE runbooks.

Loads Markdown files from the /data directory, splits them into
semantically meaningful chunks, computes embeddings via OpenAI,
and persists the resulting vectors to a local ChromaDB store.

This module exposes reusable functions so a future LangChain Agent
can trigger re-ingestion as a Tool.
"""

from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import (
    CHUNK_OVERLAP,
    CHUNK_SEPARATORS,
    CHUNK_SIZE,
    DATA_DIR,
    OPENAI_EMBEDDING_MODEL,
    VECTORSTORE_DIR,
    load_project_env,
)


def load_documents(data_dir: Path = DATA_DIR) -> list:
    """Load all Markdown files from the data directory."""
    loader = DirectoryLoader(
        str(data_dir),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    return loader.load()


def split_documents(documents: list) -> list:
    """Split documents using the shared Markdown-aware text splitter."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=list(CHUNK_SEPARATORS),
    )
    return splitter.split_documents(documents)


def get_embeddings() -> OpenAIEmbeddings:
    """Return the OpenAI embeddings model used by the ingestion pipeline."""
    return OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)


def create_vectorstore(chunks: list, persist_dir: Path = VECTORSTORE_DIR) -> Chroma:
    """
    Embed document chunks and persist them to a local ChromaDB store.

    Returns the Chroma vectorstore instance so callers can immediately
    use it for queries without re-loading from disk.
    """
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(persist_dir),
    )
    return vectorstore


def ingest(data_dir: Path = DATA_DIR, persist_dir: Path = VECTORSTORE_DIR) -> Chroma:
    """
    Full ingestion pipeline: load -> split -> embed -> persist.

    This is the primary entry point. It is designed to be wrapped as a
    LangChain Tool in a future Agent so the agent can trigger re-ingestion
    when new runbooks are added.
    """
    load_project_env()
    docs = load_documents(data_dir)
    chunks = split_documents(docs)
    print(f"Loaded {len(docs)} documents, split into {len(chunks)} chunks.")
    vectorstore = create_vectorstore(chunks, persist_dir)
    print(f"Vectorstore persisted to {persist_dir}")
    return vectorstore


if __name__ == "__main__":
    ingest()
