import json

import pytest

from integration.candidate_selector import CandidateSelector
from integration.context_formatter import ContextFormatter
from integration.filter_service import FilterService
from integration.phase_imports import (
    PROJECT_ROOT,
    BudgetTier,
    Restaurant,
    RestaurantDataStore,
    UserPreferences,
)
from integration.pipeline import load_data_store, run_integration
from integration.prompt_builder import PromptBuilder


def _sample_store() -> RestaurantDataStore:
    restaurants = [
        Restaurant(
            id="1",
            name="Alpha",
            location="Bangalore, Indiranagar",
            city="Bangalore",
            locality="Indiranagar",
            cuisines=["Chinese", "Thai"],
            cost_for_two=800,
            budget_tier=BudgetTier.MEDIUM,
            rating=4.5,
            votes=500,
        ),
        Restaurant(
            id="2",
            name="Beta",
            location="Bangalore, Koramangala",
            city="Bangalore",
            locality="Koramangala",
            cuisines=["Chinese"],
            cost_for_two=400,
            budget_tier=BudgetTier.LOW,
            rating=4.2,
            votes=300,
        ),
        Restaurant(
            id="3",
            name="Gamma",
            location="Delhi, Connaught Place",
            city="Delhi",
            locality="Connaught Place",
            cuisines=["Italian"],
            cost_for_two=1500,
            budget_tier=BudgetTier.HIGH,
            rating=4.8,
            votes=900,
        ),
    ]
    return RestaurantDataStore(restaurants)


def _preferences(**overrides) -> UserPreferences:
    payload = {
        "location": "Bangalore",
        "budget": BudgetTier.MEDIUM,
        "cuisine": "Chinese",
        "min_rating": 4.0,
        "additional_notes": "family-friendly",
    }
    payload.update(overrides)
    return UserPreferences(**payload)


def test_filter_service_returns_location_matches():
    store = _sample_store()
    result = FilterService().filter(store, _preferences())
    names = {restaurant.name for restaurant in result.restaurants}
    assert names == {"Alpha"}
    assert result.relaxed_filters == []


def test_candidate_selector_orders_by_rating():
    store = _sample_store()
    filtered = FilterService().filter(store, _preferences()).restaurants
    selected = CandidateSelector(max_candidates=1).select(filtered)
    assert selected[0].name == "Alpha"


def test_context_formatter_produces_compact_records():
    store = _sample_store()
    restaurant = store.restaurants[0]
    candidate = ContextFormatter().format_restaurant(restaurant)
    assert candidate.id == "1"
    assert candidate.budget_tier == "medium"


def test_prompt_builder_includes_preferences_and_candidates():
    store = _sample_store()
    preferences = _preferences()
    filtered = FilterService().filter(store, preferences).restaurants
    candidates = ContextFormatter().format_many(filtered)
    prompt = PromptBuilder().build(preferences, candidates, [])
    assert "Bangalore" in prompt.user_prompt
    assert "Alpha" in prompt.user_prompt
    assert "recommendations" in prompt.user_prompt
    assert prompt.estimated_tokens > 0


def test_run_integration_end_to_end():
    result = run_integration(_preferences(), _sample_store(), max_candidates=5)
    assert result.total_matches == 1
    assert result.candidate_count == 1
    assert result.prompt.estimated_tokens <= 8000
    assert result.candidates[0].name == "Alpha"


def test_integration_with_phase1_data_if_available():
    data_path = PROJECT_ROOT / "phase1_data_ingestion" / "data" / "processed" / "restaurants.parquet"
    if not data_path.exists():
        pytest.skip("Phase 1 processed data not available")

    store = load_data_store(data_path)
    result = run_integration(
        _preferences(),
        store,
        max_candidates=20,
        max_prompt_tokens=8000,
    )
    assert result.total_matches > 0
    assert result.candidate_count > 0
    assert "summary" in json.dumps(result.prompt.output_schema)
