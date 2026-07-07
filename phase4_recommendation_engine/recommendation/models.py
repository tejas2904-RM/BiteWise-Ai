from __future__ import annotations

from typing import Literal, Optional, Union

from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    rank: int = Field(ge=1)
    restaurant_id: str
    name: str
    cuisine: str
    rating: float = Field(ge=0.0, le=5.0)
    estimated_cost: Union[str, float]
    explanation: str


class RecommendationResponse(BaseModel):
    summary: Optional[str] = None
    recommendations: list[Recommendation] = Field(min_length=1)
    source: Literal["openai", "fallback"] = "openai"
