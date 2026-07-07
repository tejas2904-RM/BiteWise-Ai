from __future__ import annotations

from enum import Enum
from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class BudgetTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class UserPreferences(BaseModel):
    """Validated user preferences included in API responses."""

    model_config = ConfigDict(str_strip_whitespace=True)

    location: str = Field(..., min_length=1)
    budget: BudgetTier
    cuisine: str = Field(..., min_length=1)
    min_rating: float = Field(..., ge=0.0, le=5.0)
    additional_notes: Optional[str] = Field(default=None, max_length=500)


class RecommendationRequest(BaseModel):
    """POST /api/recommendations request body (Phase 6 input)."""

    model_config = ConfigDict(str_strip_whitespace=True)

    location: str = Field(..., min_length=1, examples=["Bangalore"])
    budget: BudgetTier = Field(..., examples=["medium"])
    cuisine: str = Field(..., min_length=1, examples=["Chinese"])
    min_rating: float = Field(..., ge=0.0, le=5.0, examples=[4.0])
    additional_notes: Optional[str] = Field(
        default=None,
        max_length=500,
        examples=["family-friendly, quick service"],
    )


class Recommendation(BaseModel):
    """Single ranked restaurant recommendation for display."""

    rank: int = Field(..., ge=1)
    restaurant_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    cuisine: str = Field(..., min_length=1)
    rating: float = Field(..., ge=0.0, le=5.0)
    estimated_cost: Union[str, float]
    explanation: str = Field(..., min_length=1)


class RecommendationResponse(BaseModel):
    """Successful recommendation API response (Phase 5 / 6 / 7 contract)."""

    summary: Optional[str] = None
    recommendations: list[Recommendation] = Field(..., min_length=1, max_length=10)
    source: Literal["openai", "fallback"] = "openai"
    preferences: Optional[UserPreferences] = None
    total_matches: Optional[int] = Field(default=None, ge=0)

    def display_preferences_label(self) -> str:
        """Human-readable preference chips, e.g. 'Bangalore · Chinese · medium'."""
        if not self.preferences:
            return ""
        budget = (
            self.preferences.budget.value
            if hasattr(self.preferences.budget, "value")
            else str(self.preferences.budget)
        )
        return f"{self.preferences.location} · {self.preferences.cuisine} · {budget}"
