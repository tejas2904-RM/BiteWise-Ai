from __future__ import annotations

from pathlib import Path
from typing import Union

from . import phase_imports as _phase_imports  # noqa: F401
from .fallback_ranker import FallbackRanker
from .models import RecommendationResponse
from .normalize import normalize_recommendations
from .openai_client import OpenAIClientError, OpenAIRecommendationClient
from .phase_imports import (
    IntegrationResult,
    RestaurantDataStore,
    UserPreferences,
    load_data_store,
    run_integration,
)

DEFAULT_TOP_N = 5


def generate_recommendations(
    integration_result: IntegrationResult,
    *,
    top_n: int = DEFAULT_TOP_N,
    use_openai: bool = True,
    api_key: str | None = None,
    model: str | None = None,
) -> RecommendationResponse:
    """Generate recommendations from a Phase 3 integration result."""
    fallback = FallbackRanker(top_n=top_n)

    if not integration_result.candidates:
        raise ValueError("Integration result contains no candidate restaurants.")

    if not use_openai:
        return fallback.rank(integration_result)

    try:
        client = OpenAIRecommendationClient(api_key=api_key, model=model)
        response = client.recommend(integration_result.prompt)
        response = normalize_recommendations(
            response,
            integration_result,
            top_n=top_n,
        )
        response.source = "openai"
        return response
    except (OpenAIClientError, ValueError):
        return fallback.rank(integration_result)


def run_recommendation_pipeline(
    preferences: UserPreferences,
    store: RestaurantDataStore,
    *,
    max_candidates: int = 20,
    top_n: int = DEFAULT_TOP_N,
    use_openai: bool = True,
    api_key: str | None = None,
    model: str | None = None,
) -> RecommendationResponse:
    """Run Phase 3 integration, then Phase 4 recommendation generation."""
    integration_result = run_integration(
        preferences,
        store,
        max_candidates=max_candidates,
        top_n=top_n,
    )
    return generate_recommendations(
        integration_result,
        top_n=top_n,
        use_openai=use_openai,
        api_key=api_key,
        model=model,
    )


def load_integration_result(path: Union[str, Path]) -> IntegrationResult:
    return IntegrationResult.model_validate_json(Path(path).read_text(encoding="utf-8"))
