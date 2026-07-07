from __future__ import annotations

from integration.phase_imports import Restaurant


class CandidateSelector:
    """Select top-N candidates by rating and popularity."""

    def __init__(self, max_candidates: int = 20) -> None:
        self.max_candidates = max_candidates

    def select(self, restaurants: list[Restaurant]) -> list[Restaurant]:
        ranked = sorted(
            restaurants,
            key=lambda restaurant: (restaurant.rating, restaurant.votes or 0),
            reverse=True,
        )
        return ranked[: self.max_candidates]
