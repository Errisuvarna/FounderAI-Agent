"""
LLM configuration shared by all CrewAI agents.
Uses Gemini Flash through CrewAI's built-in LiteLLM integration.
"""
from crewai import LLM

from app.core.config import settings


def get_gemini_llm(temperature: float = 0.4) -> LLM:
    """
    Build a CrewAI LLM instance pointed at Gemini Flash.
    CrewAI's LLM class delegates to LiteLLM, which understands the
    'gemini/<model-name>' provider prefix and reads GEMINI_API_KEY.
    
    Using gemini-1.5-flash for better rate limits.
    """
    # Use gemini-1.5-flash instead of gemini-2.5-flash for higher rate limits
    model = settings.GEMINI_MODEL.replace("gemini-2.5-flash", "gemini-1.5-flash")
    
    return LLM(
        model=model,
        api_key=settings.GEMINI_API_KEY,
        temperature=temperature,
        max_tokens=8192,
        timeout=120,
    )
