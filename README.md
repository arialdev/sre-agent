# sre-agent

Proof of Concept for a RAG-based (Retrieval-Augmented Generation) SRE agent, developed as a Master's Thesis in Artificial Intelligence (Alfonso X el Sabio University).

The system ingests SRE runbooks in Markdown format, splits them into semantically coherent chunks, generates embeddings with OpenAI, and stores them in a vector database (ChromaDB). Given an error or log input, it retrieves the most relevant runbook context to assist in incident diagnosis and resolution.

## Prerequisites

- [Mamba](https://mamba.readthedocs.io/) (or Conda)
- An **OpenAI** API key with access to the `text-embedding-3-small` model

## Installation

```bash
# 1. Clone the repository
git clone git@github.com:arialdev/sre-agent.git
cd sre-agent

# 2. Create the environment
mamba env create -f environment.yml

# 3. Activate the environment
mamba activate sre-agent
```

## Configuration

Create a `.env` file in the project root with your OpenAI API key:

```env
OPENAI_API_KEY=sk-...
```

> **Note:** The `.env` file is already included in `.gitignore` and will never be pushed to the repository.

## Usage

### 1. Ingest the runbooks

Loads runbooks from `data/`, splits them into chunks, generates embeddings, and persists them to `vectorstore/`:

```bash
python -m src.ingest
```

Expected output:

```bash
Loaded 3 documents, split into N chunks.
Vectorstore persisted to /path/to/project/vectorstore
```

### 2. Query the vectorstore

Pass an error or log line as an argument and the system returns the most relevant runbook excerpts:

```bash
python -m src.query "ECONNREFUSED error on port 5432 in production logs"
python -m src.query "The latency surpasses the SLO threholds"
```

If no argument is provided, a default example query is used.

## Project Structure

```bash
sre-agent/
├── environment.yml         # Mamba environment (Python 3.11 + dependencies)
├── .env                    # OpenAI API key (not versioned)
├── data/                   # SRE runbooks in Markdown
│   ├── db_connection_refused.md
│   ├── high_cpu_microservice.md
│   └── redis_cache_eviction.md
├── src/
│   ├── __init__.py
│   ├── ingest.py           # Ingestion pipeline: load → split → embed → persist
│   └── query.py            # Query pipeline: load vectorstore → similarity search
└── vectorstore/            # Local ChromaDB store (generated, not versioned)
```

## Required API Keys

| Service | Environment Variable | Purpose                                                       |
|---------|----------------------|-------------------------------------------------------------- |
| OpenAI  | `OPENAI_API_KEY`     | Embedding generation using the `text-embedding-3-small` model |

## Main Dependencies

| Package               | Purpose                                                         |
| --------------------- | --------------------------------------------------------------- |
| `langchain`           | Orchestration framework for RAG pipelines                       |
| `langchain-openai`    | OpenAI integration (embeddings)                                 |
| `langchain-community` | Loaders (DirectoryLoader, TextLoader) and vectorstores (Chroma) |
| `chromadb`            | Local vector database with on-disk persistence                  |
| `python-dotenv`       | Load environment variables from `.env`                          |
