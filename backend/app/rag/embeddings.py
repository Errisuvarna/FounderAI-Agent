"""
Embedding generation using Google's Gemini embedding model.
Used both at ingestion time (documents -> vectors) and query time
(user/agent query -> vector) for the RAG pipeline.
"""
import google.generativeai as genai

from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)


def embed_text(text: str, task_type: str = "retrieval_document") -> list[float]:
    """
    Generate an embedding vector for a single piece of text.
    task_type should be 'retrieval_document' when embedding content to store,
    or 'retrieval_query' when embedding a search query.
    """
    response = genai.embed_content(
        model=settings.GEMINI_EMBEDDING_MODEL,
        content=text,
        task_type=task_type,
    )
    return response["embedding"]


def embed_texts(texts: list[str], task_type: str = "retrieval_document") -> list[list[float]]:
    """Batch-embed multiple texts. Falls back to sequential calls for portability."""
    return [embed_text(t, task_type=task_type) for t in texts]
