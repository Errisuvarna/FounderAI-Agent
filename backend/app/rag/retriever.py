"""
RAG retrieval: given a query, embed it and run similarity search against
the startup's ChromaDB collection, returning the most relevant chunks.
"""
from app.db.chroma import get_or_create_collection
from app.rag.embeddings import embed_text


def retrieve_relevant_chunks(startup_id: str, query: str, top_k: int = 5) -> list[str]:
    """Return the top_k most semantically relevant text chunks for a query."""
    collection_name = f"startup_{startup_id}"
    collection = get_or_create_collection(collection_name)

    if collection.count() == 0:
        return []

    query_embedding = embed_text(query, task_type="retrieval_query")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
    )
    documents = results.get("documents", [[]])
    return documents[0] if documents else []


def format_context(chunks: list[str]) -> str:
    """Format retrieved chunks into a single context block for prompt injection."""
    if not chunks:
        return "No additional grounding context was found."
    return "\n---\n".join(f"[Context {i + 1}] {chunk}" for i, chunk in enumerate(chunks))
