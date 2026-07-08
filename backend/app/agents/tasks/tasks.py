"""
CrewAI task definitions for FounderAI.
Tasks are chained via the `context` parameter so later agents receive the
outputs of earlier agents, forming a sequential collaborative pipeline.
"""
from crewai import Agent, Task


def build_tasks(agents: dict[str, Agent], idea_title: str, idea_description: str, industry: str, target_market: str) -> dict[str, Task]:
    market_research_task = Task(
        description=(
            f"Research the market opportunity for this startup idea:\n\n"
            f"Title: {idea_title}\n"
            f"Description: {idea_description}\n"
            f"Industry: {industry}\n"
            f"Target market: {target_market}\n\n"
            "Use the web_search tool to find at least 3 real competitors and current market size "
            "data. Use rag_knowledge_search to ground your TAM/SAM/SOM methodology. "
            "Produce: (1) TAM/SAM/SOM estimate with reasoning, (2) a competitor table (name, "
            "positioning, weakness), (3) 3 key market trends relevant to this idea."
        ),
        expected_output=(
            "A structured market research report in Markdown with sections: "
            "'Market Sizing (TAM/SAM/SOM)', 'Competitive Landscape', and 'Key Trends'."
        ),
        agent=agents["market_research"],
    )

    finance_task = Task(
        description=(
            f"Using the market context provided, build a financial plan for '{idea_title}'. "
            "Choose reasonable assumptions for average price per unit, starting monthly "
            "customers, monthly growth rate, CAC, gross margin, fixed monthly costs, and average "
            "customer lifetime in months given the industry and target market. "
            "Call the financial_calculator tool with these assumptions as a JSON string to get "
            "LTV, LTV:CAC ratio, 3-year revenue projection, and break-even month. "
            "Clearly state your input assumptions before presenting the calculated results."
        ),
        expected_output=(
            "A financial plan in Markdown with sections: 'Assumptions', 'Unit Economics "
            "(LTV, CAC, LTV:CAC)', and '3-Year Revenue Projection & Break-Even'."
        ),
        agent=agents["finance"],
        context=[market_research_task],
    )

    tech_architect_task = Task(
        description=(
            f"Using the market context provided, recommend an MVP tech stack and system "
            f"architecture for '{idea_title}' ({idea_description}). "
            "Specify frontend, backend, database, hosting/deployment, and any third-party APIs "
            "needed. Include a 3-phase build roadmap (MVP, V1, Scale)."
        ),
        expected_output=(
            "A technical architecture plan in Markdown with sections: 'Recommended Stack', "
            "'System Architecture Overview', and 'Build Roadmap (MVP / V1 / Scale)'."
        ),
        agent=agents["tech_architect"],
        context=[market_research_task],
    )

    strategy_task = Task(
        description=(
            f"Using the market research and financial plan provided, define a go-to-market "
            f"strategy for '{idea_title}'. Specify target segment, primary acquisition channel, "
            "positioning statement, top 3 risks with mitigations, and a 6-month execution roadmap."
        ),
        expected_output=(
            "A growth strategy in Markdown with sections: 'Positioning', 'Go-To-Market Channel', "
            "'Key Risks & Mitigations', and '6-Month Roadmap'."
        ),
        agent=agents["strategy"],
        context=[market_research_task, finance_task],
    )

    pitch_writer_task = Task(
        description=(
            f"Using ALL prior outputs (market research, financial plan, tech architecture, "
            f"growth strategy), write a compelling executive summary (max 200 words) for "
            f"'{idea_title}' and a 10-slide pitch deck outline (one line per slide: Problem, "
            "Solution, Market Size, Product, Business Model, Traction/Roadmap, Go-To-Market, "
            "Competition, Team, The Ask)."
        ),
        expected_output=(
            "A Markdown document with two sections: 'Executive Summary' (a tight paragraph) "
            "and 'Pitch Deck Outline' (a numbered list of 10 slides, one line each)."
        ),
        agent=agents["pitch_writer"],
        context=[market_research_task, finance_task, tech_architect_task, strategy_task],
    )

    return {
        "market_research": market_research_task,
        "finance": finance_task,
        "tech_architect": tech_architect_task,
        "strategy": strategy_task,
        "pitch_writer": pitch_writer_task,
    }
