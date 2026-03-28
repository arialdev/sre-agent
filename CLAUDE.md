# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`sre-agent` is a RAG-based SRE (Site Reliability Engineering) agent, developed as a thesis project for the Master's in AI at AUAX university.

## Stack

Python 3.11, LangChain, ChromaDB, OpenAI Embeddings (text-embedding-3-small).
Environment managed with **mamba** via `environment.yml`.

## Setup

```bash
mamba env create -f environment.yml
mamba activate sre-agent
# Create .env with OPENAI_API_KEY=sk-...
```

## Common Commands

```bash
python -m src.ingest                          # Ingest runbooks into ChromaDB
python -m src.query "your error log here"     # Query the vectorstore
```

## Architecture

RAG pipeline with two modules:

- **`src/ingest.py`** — Loads Markdown runbooks from `data/`, splits with `RecursiveCharacterTextSplitter` (chunk_size=800, overlap=100, markdown-aware separators), embeds via OpenAI, persists to `vectorstore/` (ChromaDB).
- **`src/query.py`** — Loads persisted vectorstore, exposes `retrieve_context(query) -> str` for similarity search. Returns formatted string ready for LLM context injection.

Both modules expose functions designed to be wrapped as LangChain Tools for future Agent integration (`@tool` decorator).

## Data

`data/` contains SRE runbooks in Markdown with consistent structure: Severity, Symptoms, Diagnosis Steps, Resolution Steps, Prevention/Monitoring. This structure is intentional — the text splitter uses heading boundaries to produce semantically coherent chunks.
