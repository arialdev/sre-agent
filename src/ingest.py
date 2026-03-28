"""
Ingestion pipeline for SRE runbooks.

Loads Markdown files from the /data directory, splits them into
semantically meaningful chunks, computes embeddings via OpenAI,
and persists the resulting vectors to a local ChromaDB store.

This module exposes reusable functions so a future LangChain Agent
can trigger re-ingestion as a Tool.
"""

import os
from pathlib import Path

os.environ["ANONYMIZED_TELEMETRY"] = "False"

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100


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
    """
    Split documents using RecursiveCharacterTextSplitter.

    chunk_size=800 and chunk_overlap=100 are chosen for SRE runbooks because:

    - SRE runbook sections (Symptoms, Diagnosis, Resolution) typically range from
      200 to 600 characters. A chunk size of 800 keeps most sections intact as a
      single chunk, preserving the procedural coherence of each troubleshooting step.

    - An overlap of 100 characters (~1-2 lines) ensures that numbered step sequences
      are not orphaned at chunk boundaries, so context carries across adjacent chunks.

    - The custom separators list tries markdown headers first (## , ### ), then
      paragraph breaks, then line breaks. This respects the runbook's heading
      hierarchy before falling back to arbitrary splits, producing chunks that
      align with the semantic structure of the document.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(documents)


def get_embeddings() -> OpenAIEmbeddings:
    """Return the OpenAI embeddings model (text-embedding-3-small)."""
    return OpenAIEmbeddings(model="text-embedding-3-small")


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
    load_dotenv()
    docs = load_documents(data_dir)
    chunks = split_documents(docs)
    print(f"Loaded {len(docs)} documents, split into {len(chunks)} chunks.")
    vectorstore = create_vectorstore(chunks, persist_dir)
    print(f"Vectorstore persisted to {persist_dir}")
    return vectorstore


if __name__ == "__main__":
    ingest()
