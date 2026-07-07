from __future__ import annotations

from integration.phase_imports import Restaurant

from .models import CandidateRestaurant


class ContextFormatter:
    """Serialize restaurants into a compact structure for LLM context."""

    def format_restaurant(self, restaurant: Restaurant) -> CandidateRestaurant:
        return CandidateRestaurant(
            id=restaurant.id,
            name=restaurant.name,
            location=restaurant.location,
            cuisines=restaurant.cuisines,
            rating=restaurant.rating,
            cost_for_two=restaurant.cost_for_two,
            budget_tier=restaurant.budget_tier.value,
            votes=restaurant.votes,
            rest_type=restaurant.rest_type,
        )

    def format_many(self, restaurants: list[Restaurant]) -> list[CandidateRestaurant]:
        return [self.format_restaurant(restaurant) for restaurant in restaurants]
