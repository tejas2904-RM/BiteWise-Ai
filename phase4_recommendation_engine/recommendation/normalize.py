from __future__ import annotations

from .fallback_ranker import _format_budget
from .models import Recommendation, RecommendationResponse
from .phase_imports import CandidateRestaurant, IntegrationResult


def normalize_recommendations(
    response: RecommendationResponse,
    integration_result: IntegrationResult,
    *,
    top_n: int,
) -> RecommendationResponse:
    """Deduplicate AI picks, align them to candidates, backfill, and cap at top_n."""
    candidates = integration_result.candidates
    candidate_by_id = {candidate.id: candidate for candidate in candidates}
    preferences = integration_result.preferences

    deduped: list[Recommendation] = []
    seen_ids: set[str] = set()
    seen_names: set[str] = set()

    for item in response.recommendations:
        if len(deduped) >= top_n:
            break

        aligned = _align_to_candidate(item, candidates, candidate_by_id)
        if aligned is None:
            continue

        name_key = aligned.name.strip().lower()
        if aligned.restaurant_id in seen_ids or name_key in seen_names:
            continue

        seen_ids.add(aligned.restaurant_id)
        seen_names.add(name_key)
        deduped.append(aligned)

    if len(deduped) < top_n:
        deduped.extend(
            _backfill_from_candidates(
                candidates=candidates,
                seen_ids=seen_ids,
                seen_names=seen_names,
                preferences=preferences,
                needed=top_n - len(deduped),
            )
        )

    reranked = [
        item.model_copy(update={"rank": index})
        for index, item in enumerate(deduped[:top_n], start=1)
    ]

    return response.model_copy(update={"recommendations": reranked})


def _align_to_candidate(
    item: Recommendation,
    candidates: list[CandidateRestaurant],
    candidate_by_id: dict[str, CandidateRestaurant],
) -> Recommendation | None:
    candidate = candidate_by_id.get(item.restaurant_id)
    if candidate is None:
        candidate = _match_candidate_by_name(item.name, candidates)
    if candidate is None:
        return None

    cuisine_label = item.cuisine or ", ".join(candidate.cuisines[:2])
    return item.model_copy(
        update={
            "restaurant_id": candidate.id,
            "name": candidate.name,
            "cuisine": cuisine_label,
            "rating": candidate.rating,
            "estimated_cost": candidate.cost_for_two,
        }
    )


def _match_candidate_by_name(
    name: str,
    candidates: list[CandidateRestaurant],
) -> CandidateRestaurant | None:
    target = name.strip().lower()
    if not target:
        return None

    for candidate in candidates:
        if candidate.name.strip().lower() == target:
            return candidate
    return None


def _backfill_from_candidates(
    *,
    candidates: list[CandidateRestaurant],
    seen_ids: set[str],
    seen_names: set[str],
    preferences: dict[str, object],
    needed: int,
) -> list[Recommendation]:
    if needed <= 0:
        return []

    location = str(preferences.get("location", "your area"))
    cuisine = str(preferences.get("cuisine", "your preferred cuisine"))
    budget = _format_budget(preferences.get("budget", "your budget"))
    notes = preferences.get("additional_notes")

    ranked = sorted(
        candidates,
        key=lambda item: (item.rating, item.votes or 0),
        reverse=True,
    )

    backfilled: list[Recommendation] = []
    for candidate in ranked:
        if len(backfilled) >= needed:
            break

        name_key = candidate.name.strip().lower()
        if candidate.id in seen_ids or name_key in seen_names:
            continue

        seen_ids.add(candidate.id)
        seen_names.add(name_key)
        cuisine_label = ", ".join(candidate.cuisines[:2])
        explanation = (
            f"{candidate.name} is rated {candidate.rating}/5 in {candidate.location} "
            f"and serves {cuisine_label}. It fits a {budget} budget with an estimated "
            f"cost for two of ₹{int(candidate.cost_for_two)}."
        )
        if notes:
            explanation += f" It may also suit your note: {notes}."

        backfilled.append(
            Recommendation(
                rank=1,
                restaurant_id=candidate.id,
                name=candidate.name,
                cuisine=cuisine_label,
                rating=candidate.rating,
                estimated_cost=candidate.cost_for_two,
                explanation=explanation,
            )
        )

    return backfilled
