"""
LLM configuration shared by all CrewAI agents.
Uses Gemini 2.5 Flash through CrewAI's built-in LiteLLM integration.
"""
from crewai import LLM

from app.core.config import settings


def get_gemini_llm(temperature: float = 0.4) -> LLM:
    """
    Build a CrewAI LLM instance pointed at Gemini 2.5 Flash.
    CrewAI's LLM class delegates to LiteLLM, which understands the
    'gemini/<model-name>' provider prefix and reads GEMINI_API_KEY.
    """
    return LLM(
        model=settings.GEMINI_MODEL,
        api_key=settings.GEMINI_API_KEY,
        temperature=temperature,
    )
