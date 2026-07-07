from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class RestaurantDetailResponse(BaseModel):
    """Restaurant detail payload for the Phase 7 detail panel."""

    id: str
    name: str
    location: str
    city: str
    locality: str
    cuisines: list[str]
    cost_for_two: float
    budget_tier: str
    rating: float
    address: Optional[str] = None
    votes: Optional[int] = None
    rest_type: Optional[str] = None
    online_order: Optional[bool] = None
    book_table: Optional[bool] = None


class HealthResponse(BaseModel):
    status: str = "ok"
    restaurants_loaded: int = 0


class SearchHistoryItem(BaseModel):
    location: str
    cuisine: str
    budget: str
    min_rating: float
    additional_notes: Optional[str] = None
    searched_at: str


class SearchHistoryResponse(BaseModel):
    items: list[SearchHistoryItem] = Field(default_factory=list)
