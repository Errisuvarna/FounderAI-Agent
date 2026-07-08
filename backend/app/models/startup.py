"""
Pydantic schemas for startup idea submission and generated blueprint output.
"""
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class GenerateBlueprintRequest(BaseModel):
    idea_title: str = Field(min_length=3, max_length=150)
    idea_description: str = Field(min_length=20, max_length=3000)
    industry: str = Field(min_length=2, max_length=100)
    target_market: str = Field(min_length=2, max_length=200)


class AgentOutput(BaseModel):
    agent_name: str
    output: str
    tools_used: list[str] = []


class BlueprintResponse(BaseModel):
    id: str
    startup_id: str
    idea_title: str
    executive_summary: str
    market_research: dict[str, Any]
    financial_plan: dict[str, Any]
    tech_architecture: dict[str, Any]
    growth_strategy: dict[str, Any]
    pitch_deck_outline: dict[str, Any]
    agent_outputs: list[AgentOutput]
    created_at: datetime


class StartupPublic(BaseModel):
    id: str
    user_id: str
    idea_title: str
    idea_description: str
    industry: str
    target_market: str
    status: str
    created_at: datetime
