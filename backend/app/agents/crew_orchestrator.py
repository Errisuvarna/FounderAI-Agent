"""
Crew orchestration service.
Wires together the RAG seeding step, the 5 CrewAI agents, and the chained
tasks, then executes the crew and shapes the raw outputs into the
structured blueprint format persisted to MongoDB.
"""
import logging
from typing import Any

from crewai import Crew, Process

from app.agents.definitions.agents import build_agents
from app.agents.tasks.tasks import build_tasks
from app.rag.ingestion import seed_default_knowledge_base

logger = logging.getLogger(__name__)


def run_startup_crew(
    startup_id: str,
    idea_title: str,
    idea_description: str,
    industry: str,
    target_market: str,
) -> dict[str, Any]:
    """
    Execute the full FounderAI multi-agent pipeline synchronously and return
    a structured blueprint dict ready to persist to the `blueprints` collection.
    """
    # 1. Ground the crew with the curated knowledge base (RAG ingestion)
    try:
        seed_default_knowledge_base(startup_id)
    except Exception:  # pragma: no cover - RAG seeding must never block generation
        logger.exception("RAG seeding failed for startup_id=%s; continuing without it.", startup_id)

    # 2. Build agents + chained tasks
    agents = build_agents(startup_id)
    tasks = build_tasks(agents, idea_title, idea_description, industry, target_market)

    crew = Crew(
        agents=list(agents.values()),
        tasks=list(tasks.values()),
        process=Process.sequential,
        verbose=True,
    )

    # 3. Kick off the crew (blocking call — run in a threadpool from the route layer)
    crew.kickoff()

    # 4. Collect each task's raw output
    market_research_output = str(tasks["market_research"].output)
    finance_output = str(tasks["finance"].output)
    tech_output = str(tasks["tech_architect"].output)
    strategy_output = str(tasks["strategy"].output)
    pitch_output = str(tasks["pitch_writer"].output)

    executive_summary = _extract_section(pitch_output, "Executive Summary")

    agent_outputs = [
        {"agent_name": "market_research", "output": market_research_output, "tools_used": ["web_search", "rag_knowledge_search"]},
        {"agent_name": "finance", "output": finance_output, "tools_used": ["financial_calculator", "rag_knowledge_search"]},
        {"agent_name": "tech_architect", "output": tech_output, "tools_used": ["web_search", "rag_knowledge_search"]},
        {"agent_name": "strategy", "output": strategy_output, "tools_used": ["web_search", "rag_knowledge_search"]},
        {"agent_name": "pitch_writer", "output": pitch_output, "tools_used": []},
    ]

    return {
        "idea_title": idea_title,
        "executive_summary": executive_summary or pitch_output[:600],
        "market_research": {"markdown": market_research_output},
        "financial_plan": {"markdown": finance_output},
        "tech_architecture": {"markdown": tech_output},
        "growth_strategy": {"markdown": strategy_output},
        "pitch_deck_outline": {"markdown": pitch_output},
        "agent_outputs": agent_outputs,
    }


def _extract_section(markdown_text: str, heading: str) -> str:
    """Best-effort extraction of a named Markdown section's body text."""
    lines = markdown_text.splitlines()
    capturing = False
    captured: list[str] = []
    for line in lines:
        stripped = line.strip().lstrip("#").strip()
        if stripped.lower().startswith(heading.lower()):
            capturing = True
            continue
        if capturing and line.strip().startswith("#"):
            break
        if capturing:
            captured.append(line)
    return "\n".join(captured).strip()
