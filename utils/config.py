"""Configuration utilities for AI Organization OS"""

from pathlib import Path
import os

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAG_DB_PATH = PROJECT_ROOT / "rag" / "chroma_db"
MEMORY_DB_PATH = PROJECT_ROOT / "memory" / "memory_db"

# Create necessary directories
DATA_DIR.mkdir(exist_ok=True)
RAG_DB_PATH.mkdir(parents=True, exist_ok=True)
MEMORY_DB_PATH.mkdir(parents=True, exist_ok=True)

# System configuration
SYSTEM_CONFIG = {
    "app_name": "AI Organization OS",
    "version": "1.0.0",
    "environment": os.getenv("ENV", "production"),
    "debug": os.getenv("DEBUG", "false").lower() == "true",
}

# RAG configuration
RAG_CONFIG = {
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "db_path": str(RAG_DB_PATH),
    "k_retrieval": 4,
}

# Memory configuration
MEMORY_CONFIG = {
    "db_path": str(MEMORY_DB_PATH),
    "collection_name": "ai_os_memory",
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
}

# LLM configuration
LLM_CONFIG = {
    "provider": "groq",
    "main_model": "llama-3.3-70b-versatile",
    "fast_model": "llama-3.1-8b-instant",
    "temperature": 0.3,
    "max_tokens": 2000,
    "timeout": 60,
}

# Workflow configuration
WORKFLOW_CONFIG = {
    "agents": ["planner", "ceo", "research", "analyst", "critic", "qa"],
    "timeout_per_agent": 120,
    "total_timeout": 600,
}

# Reporting configuration
REPORT_CONFIG = {
    "formats": ["markdown", "html", "pdf", "text"],
    "page_size": "letter",
    "include_metadata": True,
}
