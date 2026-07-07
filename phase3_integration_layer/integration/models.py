from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class CandidateRestaurant(BaseModel):
    """Compact restaurant record passed to the LLM."""

    id: str
    name: str
    location: str
    cuisines: list[str]
    rating: float
    cost_for_two: float
    budget_tier: str
    votes: Optional[int] = None
    rest_type: Optional[str] = None


class LLMPrompt(BaseModel):
    """System and user prompts ready for Phase 4."""

    system_prompt: str
    user_prompt: str
    estimated_tokens: int
    output_schema: dict[str, object]


class IntegrationResult(BaseModel):
    """Filtered candidates and LLM-ready prompt package."""

    preferences: dict[str, object]
    total_matches: int
    candidate_count: int
    relaxed_filters: list[str] = Field(default_factory=list)
    candidates: list[CandidateRestaurant]
    prompt: LLMPrompt
