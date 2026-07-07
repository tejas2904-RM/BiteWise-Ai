from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BudgetTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class PreferenceInput(BaseModel):
    """Raw user preference payload accepted by the API, CLI, or form."""

    model_config = ConfigDict(str_strip_whitespace=True)

    location: str = Field(..., min_length=1, description='City or locality, e.g. "Bangalore"')
    budget: BudgetTier = Field(..., description="Budget tier: low, medium, or high")
    cuisine: str = Field(..., min_length=1, description='Cuisine type, e.g. "Chinese"')
    min_rating: float = Field(..., ge=0.0, le=5.0, description="Minimum restaurant rating (0-5)")
    additional_notes: Optional[str] = Field(
        default=None,
        max_length=500,
        description='Optional notes, e.g. "family-friendly, quick service"',
    )


class UserPreferences(BaseModel):
    """Validated, normalized preferences for Phase 3 integration."""

    model_config = ConfigDict(str_strip_whitespace=True)

    location: str
    budget: BudgetTier
    cuisine: str
    min_rating: float = Field(ge=0.0, le=5.0)
    additional_notes: Optional[str] = None

    def to_filter_kwargs(self) -> dict[str, object]:
        """Map preferences to Phase 1 data store query parameters."""
        return {
            "location": self.location,
            "cuisine": self.cuisine,
            "budget": self.budget,
            "min_rating": self.min_rating,
        }
