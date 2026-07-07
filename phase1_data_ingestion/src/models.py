from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class BudgetTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Restaurant(BaseModel):
    """Normalized restaurant record used by downstream phases."""

    id: str
    name: str
    location: str
    city: str
    locality: str
    cuisines: list[str] = Field(default_factory=list)
    cost_for_two: float
    budget_tier: BudgetTier
    rating: float
    address: Optional[str] = None
    votes: Optional[int] = None
    rest_type: Optional[str] = None
    online_order: Optional[bool] = None
    book_table: Optional[bool] = None
