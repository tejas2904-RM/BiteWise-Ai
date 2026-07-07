from __future__ import annotations

from . import phase_imports as _phase_imports  # noqa: F401
from .models import Recommendation, RecommendationResponse
from .phase_imports import CandidateRestaurant, IntegrationResult

DEFAULT_TOP_N = 5


class FallbackRanker:
    """Rule-based ranking when OpenAI is unavailable or returns invalid output."""

    def __init__(self, top_n: int = DEFAULT_TOP_N) -> None:
        self.top_n = top_n

    def rank(self, integration_result: IntegrationResult) -> RecommendationResponse:
        unique_candidates = _unique_candidates(integration_result.candidates)
        candidates = sorted(
            unique_candidates,
            key=lambda item: (item.rating, item.votes or 0),
            reverse=True,
        )[: self.top_n]

        if not candidates:
            raise ValueError("No candidate restaurants available for fallback ranking.")

        preferences = integration_result.preferences
        location = str(preferences.get("location", "your area"))
        cuisine = str(preferences.get("cuisine", "your preferred cuisine"))
        budget = _format_budget(preferences.get("budget", "your budget"))
        notes = preferences.get("additional_notes")

        recommendations: list[Recommendation] = []
        for index, candidate in enumerate(candidates, start=1):
            cuisine_label = ", ".join(candidate.cuisines[:2])
            explanation = (
                f"{candidate.name} is rated {candidate.rating}/5 in {candidate.location} "
                f"and serves {cuisine_label}. It fits a {budget} budget with an estimated "
                f"cost for two of ₹{int(candidate.cost_for_two)}."
            )
            if notes:
                explanation += f" It may also suit your note: {notes}."

            recommendations.append(
                Recommendation(
                    rank=index,
                    restaurant_id=candidate.id,
                    name=candidate.name,
                    cuisine=cuisine_label,
                    rating=candidate.rating,
                    estimated_cost=candidate.cost_for_two,
                    explanation=explanation,
                )
            )

        summary = (
            f"Top {len(recommendations)} {cuisine} options in {location} "
            f"selected by rating and popularity (fallback ranking)."
        )
        return RecommendationResponse(
            summary=summary,
            recommendations=recommendations,
            source="fallback",
        )

    @staticmethod
    def _primary_cuisine(candidate: CandidateRestaurant, preferred: str) -> str:
        preferred_lower = preferred.lower()
        for cuisine in candidate.cuisines:
            if preferred_lower in cuisine.lower():
                return cuisine
        return candidate.cuisines[0] if candidate.cuisines else preferred


def _format_budget(value: object) -> str:
    if hasattr(value, "value"):
        return str(value.value)
    text = str(value)
    if text.startswith("BudgetTier."):
        return text.split(".", 1)[1].lower()
    return text


def _unique_candidates(candidates: list[CandidateRestaurant]) -> list[CandidateRestaurant]:
    unique: list[CandidateRestaurant] = []
    seen_ids: set[str] = set()
    seen_names: set[str] = set()
    for candidate in candidates:
        name_key = candidate.name.strip().lower()
        if candidate.id in seen_ids or name_key in seen_names:
            continue
        seen_ids.add(candidate.id)
        seen_names.add(name_key)
        unique.append(candidate)
    return unique
