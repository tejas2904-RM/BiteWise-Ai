import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError as PydanticValidationError

from src.api import app
from src.models import BudgetTier, PreferenceInput
from src.validator import ValidationError, validate_preferences

client = TestClient(app)


def test_valid_preferences():
    result = validate_preferences(
        {
            "location": "  Bangalore ",
            "budget": "medium",
            "cuisine": " Chinese ",
            "min_rating": 4.0,
            "additional_notes": "family-friendly",
        }
    )
    assert result.location == "Bangalore"
    assert result.cuisine == "Chinese"
    assert result.budget == BudgetTier.MEDIUM
    assert result.min_rating == 4.0
    assert result.additional_notes == "family-friendly"
    assert result.to_filter_kwargs()["location"] == "Bangalore"


def test_missing_location_raises_clear_error():
    with pytest.raises(ValidationError) as exc_info:
        validate_preferences(
            {
                "location": "   ",
                "budget": "low",
                "cuisine": "Italian",
                "min_rating": 3.5,
            }
        )
    assert exc_info.value.errors[0]["field"] == "location"


def test_invalid_budget_raises_error():
    with pytest.raises(PydanticValidationError):
        PreferenceInput.model_validate(
            {
                "location": "Delhi",
                "budget": "expensive",
                "cuisine": "Thai",
                "min_rating": 4.0,
            }
        )


def test_invalid_rating_raises_error():
    with pytest.raises(PydanticValidationError):
        PreferenceInput.model_validate(
            {
                "location": "Delhi",
                "budget": "low",
                "cuisine": "Thai",
                "min_rating": 6.0,
            }
        )


def test_api_submit_preferences_json():
    response = client.post(
        "/api/preferences",
        json={
            "location": "Bangalore",
            "budget": "high",
            "cuisine": "Italian",
            "min_rating": 4.2,
            "additional_notes": "quick service",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["location"] == "Bangalore"
    assert body["budget"] == "high"
    assert body["cuisine"] == "Italian"


def test_api_rejects_invalid_payload():
    response = client.post(
        "/api/preferences",
        json={
            "location": "",
            "budget": "medium",
            "cuisine": "Chinese",
            "min_rating": 4.0,
        },
    )
    assert response.status_code == 422


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
