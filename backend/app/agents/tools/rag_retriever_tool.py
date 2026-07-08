"""
Real tool calling: RAG retrieval tool.
Lets agents pull grounded context (startup knowledge base + any uploaded
documents) from ChromaDB via semantic similarity search, rather than
relying purely on the LLM's parametric memory.
"""
from crewai_tools import BaseTool
from pydantic import Field

from app.rag.retriever import format_context, retrieve_relevant_chunks


class RagRetrieverTool(BaseTool):
    name: str = "rag_knowledge_search"
    description: str = (
        "Search the startup's private knowledge base (uploaded documents plus curated "
        "startup/finance/market frameworks) for context relevant to a query. "
        "Input should be a natural-language question, e.g. 'unit economics benchmarks for SaaS'. "
        "Use this before making claims about frameworks, benchmarks, or best practices."
    )
    startup_id: str = Field(...)

    def _run(self, query: str) -> str:
        chunks = retrieve_relevant_chunks(self.startup_id, query, top_k=5)
        return format_context(chunks)
