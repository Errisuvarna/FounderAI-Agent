"""
Real tool calling: live web search via Serper.dev (Google Search API wrapper).
Used by Market Research, Tech Architect, and Strategy agents to ground
their output in current, real-world information instead of hallucinating.
"""
import requests
from crewai_tools import BaseTool
from pydantic import Field

from app.core.config import settings


class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = (
        "Search the live web for current information such as competitors, market size, "
        "industry trends, or pricing. Input should be a concise search query string. "
        "Returns the top organic search results with titles, links, and snippets."
    )
    api_key: str = Field(default_factory=lambda: settings.SERPER_API_KEY)

    def _run(self, query: str) -> str:
        if not self.api_key:
            return (
                "Web search is not configured (missing SERPER_API_KEY). "
                "Proceed using general domain knowledge and clearly flag it as an estimate."
            )

        try:
            response = requests.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": self.api_key, "Content-Type": "application/json"},
                json={"q": query, "num": 8},
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            return f"Web search failed due to a network error: {exc}. Proceed with best estimate."

        results = data.get("organic", [])[:8]
        if not results:
            return f"No web search results found for query: '{query}'."

        formatted = [f"Search results for '{query}':"]
        for idx, item in enumerate(results, start=1):
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            formatted.append(f"{idx}. {title}\n   {snippet}\n   Source: {link}")

        return "\n".join(formatted)
