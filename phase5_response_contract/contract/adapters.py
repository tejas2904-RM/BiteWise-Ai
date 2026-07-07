from __future__ import annotations

from typing import Any

from .models import Recommendation, RecommendationResponse, UserPreferences


def to_contract_response(
    payload: dict[str, Any] | RecommendationResponse,
    *,
    preferences: UserPreferences | dict[str, Any] | None = None,
    total_matches: int | None = None,
) -> RecommendationResponse:
    """Validate and normalize any recommendation payload to the Phase 5 contract."""
    if isinstance(payload, RecommendationResponse):
        data = payload.model_dump()
    else:
        data = dict(payload)

    if preferences is not None:
        data["preferences"] = (
            preferences.model_dump()
            if isinstance(preferences, UserPreferences)
            else preferences
        )
    if total_matches is not None:
        data["total_matches"] = total_matches

    return RecommendationResponse.model_validate(data)


def from_phase4_response(
    phase4_response: Any,
    *,
    preferences: UserPreferences | dict[str, Any] | None = None,
    total_matches: int | None = None,
) -> RecommendationResponse:
    """Adapt Phase 4 RecommendationResponse to the Phase 5 contract."""
    if hasattr(phase4_response, "model_dump"):
        payload = phase4_response.model_dump()
    elif isinstance(phase4_response, dict):
        payload = phase4_response
    else:
        raise TypeError("phase4_response must be a Pydantic model or dict.")

    recommendations = [
        Recommendation.model_validate(item) for item in payload.get("recommendations", [])
    ]

    prefs = preferences
    if prefs is None and payload.get("preferences"):
        prefs = UserPreferences.model_validate(payload["preferences"])
    elif isinstance(prefs, dict):
        prefs = UserPreferences.model_validate(prefs)

    return RecommendationResponse(
        summary=payload.get("summary"),
        recommendations=recommendations,
        source=payload.get("source", "openai"),
        preferences=prefs,
        total_matches=total_matches if total_matches is not None else payload.get("total_matches"),
    )
