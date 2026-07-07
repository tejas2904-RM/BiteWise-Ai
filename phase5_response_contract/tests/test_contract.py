import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from contract.adapters import from_phase4_response, to_contract_response
from contract.errors import ErrorCode, build_error_response
from contract.models import (
    BudgetTier,
    Recommendation,
    RecommendationRequest,
    RecommendationResponse,
    UserPreferences,
)
from contract.schema_export import export_json_schemas, export_typescript_types

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_recommendation_request_validates():
    req = RecommendationRequest(
        location="Bangalore",
        budget=BudgetTier.MEDIUM,
        cuisine="Chinese",
        min_rating=4.0,
        additional_notes="family-friendly",
    )
    assert req.budget == BudgetTier.MEDIUM


def test_recommendation_request_rejects_invalid_rating():
    with pytest.raises(ValidationError):
        RecommendationRequest(
            location="Bangalore",
            budget="medium",
            cuisine="Chinese",
            min_rating=6.0,
        )


def test_recommendation_response_requires_at_least_one_item():
    with pytest.raises(ValidationError):
        RecommendationResponse(recommendations=[], source="openai")


def test_display_preferences_label():
    response = RecommendationResponse(
        summary="Top picks",
        recommendations=[
            Recommendation(
                rank=1,
                restaurant_id="abc",
                name="ECHOES",
                cuisine="Chinese",
                rating=4.7,
                estimated_cost=750,
                explanation="Great fit",
            )
        ],
        source="openai",
        preferences=UserPreferences(
            location="Bangalore",
            budget=BudgetTier.MEDIUM,
            cuisine="Chinese",
            min_rating=4.0,
        ),
        total_matches=100,
    )
    assert "Bangalore" in response.display_preferences_label()
    assert "Chinese" in response.display_preferences_label()


def test_error_response_codes():
    err = build_error_response(
        "Invalid input",
        ErrorCode.VALIDATION_ERROR,
        field_errors=[{"field": "location", "message": "Required"}],
    )
    assert err.code == ErrorCode.VALIDATION_ERROR
    assert err.details is not None
    assert err.details.errors[0].field == "location"


def test_from_phase4_response_adapter():
    phase4_payload = {
        "summary": "AI summary",
        "recommendations": [
            {
                "rank": 1,
                "restaurant_id": "1",
                "name": "ECHOES Koramangala",
                "cuisine": "Chinese",
                "rating": 4.7,
                "estimated_cost": 750,
                "explanation": "Strong match",
            }
        ],
        "source": "openai",
    }
    contract = from_phase4_response(
        phase4_payload,
        preferences={
            "location": "Bangalore",
            "budget": "medium",
            "cuisine": "Chinese",
            "min_rating": 4.0,
        },
        total_matches=1311,
    )
    assert contract.total_matches == 1311
    assert contract.preferences.location == "Bangalore"
    assert contract.recommendations[0].name == "ECHOES Koramangala"


def test_export_json_schemas(tmp_path):
    paths = export_json_schemas(tmp_path)
    assert (tmp_path / "recommendation_response.schema.json").exists()
    assert (tmp_path / "api_contract.bundle.json").exists()
    bundle = json.loads((tmp_path / "api_contract.bundle.json").read_text(encoding="utf-8"))
    assert "recommendation_response" in bundle["schemas"]


def test_export_typescript_types(tmp_path):
    path = export_typescript_types(tmp_path / "types.ts")
    text = path.read_text(encoding="utf-8")
    assert "export interface RecommendationResponse" in text


def test_validate_phase4_output_file_if_present():
    sample = PROJECT_ROOT / "phase4_recommendation_engine" / "output" / "openai_test.json"
    if not sample.exists():
        pytest.skip("Phase 4 sample output not available")
    payload = json.loads(sample.read_text(encoding="utf-8"))
    contract = from_phase4_response(payload)
    assert len(contract.recommendations) >= 1


def test_to_contract_response_round_trip():
    original = RecommendationResponse(
        summary="ok",
        recommendations=[
            Recommendation(
                rank=1,
                restaurant_id="x",
                name="Test",
                cuisine="Italian",
                rating=4.0,
                estimated_cost="500",
                explanation="Nice",
            )
        ],
        source="fallback",
    )
    restored = to_contract_response(original.model_dump())
    assert restored.source == "fallback"
