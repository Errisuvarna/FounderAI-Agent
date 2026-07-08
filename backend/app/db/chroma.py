"""
ChromaDB client management for the RAG vector store.
Uses a local persistent client so the hackathon deployment needs no external vector DB service.
"""
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings

_chroma_client: chromadb.ClientAPI | None = None


def get_chroma_client() -> chromadb.ClientAPI:
    """Return a singleton persistent ChromaDB client."""
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
    return _chroma_client


def get_or_create_collection(collection_name: str):
    """Get (or lazily create) a named Chroma collection."""
    client = get_chroma_client()
    return client.get_or_create_collection(name=collection_name)
