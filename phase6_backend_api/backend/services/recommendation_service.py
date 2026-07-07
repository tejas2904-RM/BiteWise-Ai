from __future__ import annotations

from contract.models import RecommendationRequest, RecommendationResponse, UserPreferences as ContractUserPreferences

from backend.phase_bridge import (
    from_phase4_response,
    generate_recommendations,
    run_integration,
    validate_preferences,
)
from backend.services.restaurant_service import RestaurantService, restaurant_service


class NoMatchesError(Exception):
    """Raised when filters return no candidate restaurants."""

    def __init__(self, message: str = "No restaurants match the given preferences.") -> None:
        super().__init__(message)


class RecommendationService:
    """Orchestrate Phases 2–4 and return Phase 5 contract responses."""

    def __init__(self, restaurants: RestaurantService | None = None) -> None:
        self._restaurants = restaurants or restaurant_service

    def create_recommendations(
        self,
        request: RecommendationRequest,
        *,
        top_n: int = 5,
        use_openai: bool = True,
    ) -> RecommendationResponse:
        preferences = validate_preferences(request.model_dump())
        store = self._restaurants._get_store()

        integration = run_integration(preferences, store, top_n=top_n)
        if integration.total_matches == 0 or not integration.candidates:
            raise NoMatchesError()

        phase4_response = generate_recommendations(
            integration,
            top_n=top_n,
            use_openai=use_openai,
        )

        contract_prefs = ContractUserPreferences.model_validate(preferences.model_dump())
        return from_phase4_response(
            phase4_response,
            preferences=contract_prefs,
            total_matches=integration.total_matches,
        )


recommendation_service = RecommendationService()
