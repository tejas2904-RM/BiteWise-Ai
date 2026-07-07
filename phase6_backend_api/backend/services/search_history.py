from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
from threading import Lock

from contract.models import RecommendationRequest

from backend.models.schemas import SearchHistoryItem, SearchHistoryResponse


class SearchHistoryStore:
    """In-memory recent search history (optional Phase 6 endpoint)."""

    def __init__(self, max_items: int = 20) -> None:
        self._max_items = max_items
        self._items: deque[SearchHistoryItem] = deque()
        self._lock = Lock()

    def add(self, request: RecommendationRequest) -> None:
        item = SearchHistoryItem(
            location=request.location,
            cuisine=request.cuisine,
            budget=request.budget.value,
            min_rating=request.min_rating,
            additional_notes=request.additional_notes,
            searched_at=datetime.now(timezone.utc).isoformat(),
        )
        with self._lock:
            self._items.appendleft(item)
            while len(self._items) > self._max_items:
                self._items.pop()

    def list(self, limit: int = 10) -> SearchHistoryResponse:
        with self._lock:
            items = list(self._items)[:limit]
        return SearchHistoryResponse(items=items)


search_history_store = SearchHistoryStore()
