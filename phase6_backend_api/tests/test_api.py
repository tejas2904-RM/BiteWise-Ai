import backend.config  # noqa: F401

import pytest
from fastapi.testclient import TestClient

from backend.api.app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["restaurants_loaded"] > 0


def test_recommendations_validation_error():
    response = client.post(
        "/api/recommendations",
        json={
            "location": "",
            "budget": "medium",
            "cuisine": "Chinese",
            "min_rating": 4.0,
        },
    )
    assert response.status_code == 422
    body = response.json()
    assert body["code"] == "validation_error"


def test_recommendations_fallback_only():
    response = client.post(
        "/api/recommendations?fallback_only=true&top_n=3",
        json={
            "location": "Bangalore",
            "budget": "medium",
            "cuisine": "Chinese",
            "min_rating": 4.0,
            "additional_notes": "family-friendly",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "fallback"
    assert len(body["recommendations"]) == 3
    assert body["total_matches"] > 0
    assert body["preferences"]["location"] == "Bangalore"


def test_restaurant_detail_found():
    rec = client.post(
        "/api/recommendations?fallback_only=true&top_n=1",
        json={
            "location": "Bangalore",
            "budget": "medium",
            "cuisine": "Chinese",
            "min_rating": 4.0,
        },
    )
    assert rec.status_code == 200
    restaurant_id = rec.json()["recommendations"][0]["restaurant_id"]

    detail = client.get(f"/api/restaurants/{restaurant_id}")
    assert detail.status_code == 200
    assert detail.json()["id"] == restaurant_id


def test_restaurant_detail_not_found():
    response = client.get("/api/restaurants/nonexistent-id-12345")
    assert response.status_code == 404
    assert response.json()["code"] == "no_matches"


def test_search_history_after_recommendation():
    client.post(
        "/api/recommendations?fallback_only=true&top_n=1",
        json={
            "location": "Bangalore",
            "budget": "low",
            "cuisine": "Italian",
            "min_rating": 3.5,
        },
    )
    history = client.get("/api/search/history?limit=5")
    assert history.status_code == 200
    items = history.json()["items"]
    assert len(items) >= 1
    assert items[0]["cuisine"] == "Italian"


def test_no_matches_returns_404():
    response = client.post(
        "/api/recommendations?fallback_only=true",
        json={
            "location": "NonexistentCityXYZ",
            "budget": "high",
            "cuisine": "Martian",
            "min_rating": 4.9,
        },
    )
    assert response.status_code == 404
    assert response.json()["code"] == "no_matches"
