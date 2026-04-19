"""Central configuration for the SRE agent project."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
DATA_DIR = PROJECT_ROOT / "data"
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_CHAT_MODEL = "gpt-4o-mini"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
CHUNK_SEPARATORS = ("\n## ", "\n### ", "\n\n", "\n", " ", "")

RUNBOOKS_API_BASE_URL_ENV = "RUNBOOKS_API_BASE_URL"
RUNBOOKS_API_QUERY_PATH = "api/knowledge/query"
RETRIEVAL_DISTANCE_THRESHOLD = 1.25
REMOTE_REQUEST_TIMEOUT_SECONDS = 10
DEFAULT_RETRIEVAL_LIMIT = 3

NO_CONTEXT_SENTINEL = "No relevant runbook context found."


def load_project_env() -> None:
    """Load project-local environment variables from the repository root."""
    load_dotenv(ENV_FILE)
