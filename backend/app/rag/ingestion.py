"""
RAG ingestion pipeline.
Splits source text into overlapping chunks, embeds each chunk with Gemini,
and stores the vectors + metadata in a per-startup ChromaDB collection.

Two sources feed this pipeline:
1. A small built-in knowledge base of startup/finance/market frameworks
   (pre-seeded on first run) that grounds agents even with zero user uploads.
2. Optional user-uploaded documents (competitor reports, market research PDFs, etc).
"""
import hashlib

from app.db.chroma import get_or_create_collection
from app.rag.embeddings import embed_text

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Simple sliding-window character-based chunker with overlap."""
    text = text.strip()
    if len(text) <= chunk_size:
        return [text] if text else []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def ingest_text(
    collection_name: str,
    text: str,
    source_name: str,
) -> int:
    """
    Chunk, embed, and upsert a block of text into the given Chroma collection.
    Returns the number of chunks ingested.
    """
    collection = get_or_create_collection(collection_name)
    chunks = chunk_text(text)
    if not chunks:
        return 0

    ids, embeddings, documents, metadatas = [], [], [], []
    for idx, chunk in enumerate(chunks):
        chunk_id = hashlib.sha256(f"{source_name}-{idx}-{chunk[:50]}".encode()).hexdigest()
        ids.append(chunk_id)
        embeddings.append(embed_text(chunk, task_type="retrieval_document"))
        documents.append(chunk)
        metadatas.append({"source": source_name, "chunk_index": idx})

    collection.upsert(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
    return len(chunks)


# A compact, hand-curated startup knowledge base used to ground agent
# reasoning even before any user document has been uploaded.
DEFAULT_KNOWLEDGE_BASE = {
    "market_sizing_framework": (
        "TAM, SAM, and SOM are the three layers used to size a market. TAM (Total Addressable "
        "Market) is the total revenue opportunity if a product captured 100% of its market. "
        "SAM (Serviceable Addressable Market) is the segment of TAM realistically reachable given "
        "the product's business model and geography. SOM (Serviceable Obtainable Market) is the "
        "portion of SAM a startup can realistically capture in the near term given competition and "
        "go-to-market constraints. Early-stage startups should justify SOM using bottoms-up "
        "assumptions (e.g., sales capacity, conversion rates) rather than top-down percentages."
    ),
    "saas_unit_economics": (
        "Healthy SaaS unit economics generally target an LTV:CAC ratio of at least 3:1 and CAC "
        "payback period under 12-18 months. Gross margin for software businesses typically ranges "
        "from 70-85%. Net revenue retention above 100% indicates expansion revenue is outpacing churn. "
        "Early-stage startups should track monthly burn multiple (net burn / net new ARR) to gauge "
        "capital efficiency; a burn multiple under 2 is considered efficient growth."
    ),
    "gtm_strategy_playbook": (
        "Go-to-market strategy should specify: target customer segment, primary acquisition channel "
        "(PLG, sales-led, or channel partnerships), pricing model, and a wedge feature that drives "
        "initial adoption before expanding to the full platform. Early-stage startups typically pick "
        "one primary channel to master before diversifying, since split focus dilutes CAC efficiency."
    ),
    "mvp_tech_scoping": (
        "An MVP should implement the smallest feature set that lets a startup test its core value "
        "hypothesis with real users. Common early-stage stacks favor managed services (e.g., managed "
        "Postgres, serverless functions, third-party auth) to minimize DevOps overhead, migrating to "
        "custom infrastructure only once usage patterns justify the engineering investment."
    ),
    "fundraising_basics": (
        "Pre-seed and seed rounds typically fund 12-18 months of runway to reach the next milestone "
        "(e.g., product-market fit signals, initial revenue traction). Investors evaluate market size, "
        "founder-market fit, early traction, and defensibility. A pitch deck typically covers: problem, "
        "solution, market size, product, traction, business model, competition, team, and the ask."
    ),
}


def seed_default_knowledge_base(startup_id: str) -> int:
    """Ingest the built-in knowledge base into the startup's Chroma collection."""
    collection_name = f"startup_{startup_id}"
    total_chunks = 0
    for source_name, text in DEFAULT_KNOWLEDGE_BASE.items():
        total_chunks += ingest_text(collection_name, text, source_name)
    return total_chunks
