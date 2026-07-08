"""
CrewAI agent definitions for FounderAI.
Five specialized agents collaborate sequentially to turn a raw startup idea
into a complete, investor-ready business blueprint.
"""
from crewai import Agent

from app.agents.llm_config import get_gemini_llm
from app.agents.tools.financial_calc_tool import FinancialCalculatorTool
from app.agents.tools.rag_retriever_tool import RagRetrieverTool
from app.agents.tools.web_search_tool import WebSearchTool


def build_agents(startup_id: str) -> dict[str, Agent]:
    """
    Construct all five agents for a given startup's crew run.
    Each agent gets its own RAG tool instance scoped to this startup_id so
    retrieval stays isolated per user session.
    """
    llm = get_gemini_llm()
    web_search = WebSearchTool()
    rag_search = RagRetrieverTool(startup_id=startup_id)
    financial_calc = FinancialCalculatorTool()

    market_research_agent = Agent(
        role="Senior Market Research Analyst",
        goal=(
            "Analyze the market opportunity for the given startup idea, including TAM/SAM/SOM, "
            "top competitors, and key market trends, using real web data wherever possible."
        ),
        backstory=(
            "You are a former VC analyst who has sized hundreds of markets for seed-stage "
            "startups. You back every claim with evidence from web search or the knowledge base "
            "and are explicit when a number is an estimate rather than a verified fact."
        ),
        tools=[web_search, rag_search],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    finance_agent = Agent(
        role="Startup Financial Analyst",
        goal=(
            "Build a realistic financial plan: revenue model, cost structure, unit economics "
            "(LTV, CAC, break-even), and a 3-year revenue projection, using the financial "
            "calculator tool for all arithmetic."
        ),
        backstory=(
            "You are a fractional CFO who has built financial models for dozens of pre-seed "
            "and seed startups. You never eyeball numbers — you always run them through the "
            "financial calculator tool and explain the assumptions behind every input."
        ),
        tools=[financial_calc, rag_search],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    tech_architect_agent = Agent(
        role="Startup Solutions Architect",
        goal=(
            "Recommend a pragmatic MVP tech stack and system architecture that matches the "
            "startup's scale, budget, and team size, and outline the phased build roadmap."
        ),
        backstory=(
            "You are a CTO-for-hire who has shipped MVPs for over 30 early-stage startups. "
            "You favor boring, proven technology and managed services over premature complexity, "
            "and you always justify stack choices against the startup's actual constraints."
        ),
        tools=[web_search, rag_search],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    strategy_agent = Agent(
        role="Growth & GTM Strategist",
        goal=(
            "Define a go-to-market strategy, positioning, key risks, and a 6-month execution "
            "roadmap that a first-time founder could realistically follow."
        ),
        backstory=(
            "You are a growth advisor who has run GTM playbooks across B2B and B2C startups. "
            "You are direct about risks and trade-offs rather than offering generic optimism."
        ),
        tools=[web_search, rag_search],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    pitch_writer_agent = Agent(
        role="Pitch Deck & Narrative Consultant",
        goal=(
            "Synthesize the market research, financial plan, tech architecture, and growth "
            "strategy into a compelling executive summary and a slide-by-slide pitch deck outline."
        ),
        backstory=(
            "You are a startup storytelling consultant who has helped founders raise seed and "
            "Series A rounds. You turn dense analysis into a crisp, investor-ready narrative "
            "without losing the substance underneath."
        ),
        tools=[],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    return {
        "market_research": market_research_agent,
        "finance": finance_agent,
        "tech_architect": tech_architect_agent,
        "strategy": strategy_agent,
        "pitch_writer": pitch_writer_agent,
    }
