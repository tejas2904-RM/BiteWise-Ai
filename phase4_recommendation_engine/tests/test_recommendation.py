import json
from unittest.mock import MagicMock, patch

import pytest

from recommendation import phase_imports as _phase_imports  # noqa: F401
from recommendation.fallback_ranker import FallbackRanker
from recommendation.models import RecommendationResponse
from recommendation.openai_client import OpenAIClientError
from recommendation.phase_imports import CandidateRestaurant, IntegrationResult, LLMPrompt
from recommendation.pipeline import generate_recommendations
from recommendation.response_parser import ResponseParser, ResponseParserError


def _integration_result() -> IntegrationResult:
    return IntegrationResult(
        preferences={
            "location": "Bangalore",
            "budget": "medium",
            "cuisine": "Chinese",
            "min_rating": 4.0,
            "additional_notes": "family-friendly",
        },
        total_matches=2,
        candidate_count=2,
        relaxed_filters=[],
        candidates=[
            CandidateRestaurant(
                id="1",
                name="Alpha",
                location="Bangalore, Indiranagar",
                cuisines=["Chinese", "Thai"],
                rating=4.5,
                cost_for_two=800,
                budget_tier="medium",
                votes=500,
            ),
            CandidateRestaurant(
                id="2",
                name="Beta",
                location="Bangalore, Koramangala",
                cuisines=["Chinese"],
                rating=4.2,
                cost_for_two=500,
                budget_tier="medium",
                votes=300,
            ),
        ],
        prompt=LLMPrompt(
            system_prompt="system",
            user_prompt="user",
            estimated_tokens=100,
            output_schema={"type": "object"},
        ),
    )


def test_response_parser_accepts_json_object():
    payload = {
        "summary": "Great picks",
        "recommendations": [
            {
                "rank": 1,
                "restaurant_id": "1",
                "name": "Alpha",
                "cuisine": "Chinese",
                "rating": 4.5,
                "estimated_cost": 800,
                "explanation": "Strong match",
            }
        ],
    }
    result = ResponseParser().parse(json.dumps(payload))
    assert result.summary == "Great picks"
    assert result.recommendations[0].name == "Alpha"


def test_response_parser_accepts_fenced_json():
    content = """Here are picks:
```json
{"summary":"ok","recommendations":[{"rank":1,"restaurant_id":"1","name":"Alpha","cuisine":"Chinese","rating":4.5,"estimated_cost":800,"explanation":"Nice"}]}
```"""
    result = ResponseParser().parse(content)
    assert result.recommendations[0].restaurant_id == "1"


def test_response_parser_raises_on_invalid_json():
    with pytest.raises(ResponseParserError):
        ResponseParser().parse("not json")


def test_fallback_ranker_returns_top_matches():
    result = FallbackRanker(top_n=2).rank(_integration_result())
    assert result.source == "fallback"
    assert len(result.recommendations) == 2
    assert result.recommendations[0].name == "Alpha"
    assert result.recommendations[0].rank == 1


@patch("recommendation.pipeline.OpenAIRecommendationClient")
def test_generate_recommendations_uses_openai(mock_client_cls):
    mock_client = MagicMock()
    mock_client.recommend.return_value = RecommendationResponse(
        summary="AI summary",
        recommendations=[
            {
                "rank": 1,
                "restaurant_id": "1",
                "name": "Alpha",
                "cuisine": "Chinese",
                "rating": 4.5,
                "estimated_cost": 800,
                "explanation": "Best fit",
            }
        ],
        source="openai",
    )
    mock_client_cls.return_value = mock_client

    response = generate_recommendations(_integration_result(), use_openai=True, api_key="test-key")
    assert response.source == "openai"
    assert response.recommendations[0].name == "Alpha"
    mock_client.recommend.assert_called_once()


@patch("recommendation.pipeline.OpenAIRecommendationClient")
def test_generate_recommendations_falls_back_when_openai_unavailable(mock_client_cls):
    mock_client_cls.side_effect = OpenAIClientError("OpenAI unavailable")
    response = generate_recommendations(
        _integration_result(),
        use_openai=True,
        api_key="test-key",
    )
    assert response.source == "fallback"
    assert len(response.recommendations) == 2
