from recommendation.models import Recommendation, RecommendationResponse
from recommendation.normalize import normalize_recommendations
from recommendation.phase_imports import CandidateRestaurant, IntegrationResult, LLMPrompt


def _candidate(restaurant_id: str, name: str, rating: float = 4.5) -> CandidateRestaurant:
    return CandidateRestaurant(
        id=restaurant_id,
        name=name,
        location="Bangalore, Indiranagar",
        cuisines=["Chinese"],
        rating=rating,
        cost_for_two=800,
        budget_tier="medium",
        votes=500,
    )


def _integration_result(candidates: list[CandidateRestaurant]) -> IntegrationResult:
    return IntegrationResult(
        preferences={
            "location": "Bangalore",
            "budget": "medium",
            "cuisine": "Chinese",
            "min_rating": 4.0,
        },
        total_matches=len(candidates),
        candidate_count=len(candidates),
        relaxed_filters=[],
        candidates=candidates,
        prompt=LLMPrompt(
            system_prompt="system",
            user_prompt="user",
            estimated_tokens=100,
            output_schema={"type": "object"},
        ),
    )


def test_normalize_removes_duplicate_restaurants():
    candidates = [
        _candidate("1", "Alpha", 4.8),
        _candidate("2", "Beta", 4.6),
        _candidate("3", "Gamma", 4.4),
    ]
    response = RecommendationResponse(
        summary="Picks",
        recommendations=[
            Recommendation(
                rank=1,
                restaurant_id="1",
                name="Alpha",
                cuisine="Chinese",
                rating=4.8,
                estimated_cost=800,
                explanation="First",
            ),
            Recommendation(
                rank=2,
                restaurant_id="1",
                name="Alpha",
                cuisine="Chinese",
                rating=4.8,
                estimated_cost=800,
                explanation="Duplicate",
            ),
            Recommendation(
                rank=3,
                restaurant_id="2",
                name="Beta",
                cuisine="Chinese",
                rating=4.6,
                estimated_cost=700,
                explanation="Second",
            ),
        ],
    )

    normalized = normalize_recommendations(
        response,
        _integration_result(candidates),
        top_n=5,
    )

    assert len(normalized.recommendations) == 3
    assert [item.restaurant_id for item in normalized.recommendations] == ["1", "2", "3"]
    assert [item.rank for item in normalized.recommendations] == [1, 2, 3]


def test_normalize_backfills_to_top_n():
    candidates = [
        _candidate("1", "Alpha", 4.8),
        _candidate("2", "Beta", 4.6),
        _candidate("3", "Gamma", 4.4),
        _candidate("4", "Delta", 4.2),
        _candidate("5", "Epsilon", 4.0),
    ]
    response = RecommendationResponse(
        summary="Short list",
        recommendations=[
            Recommendation(
                rank=1,
                restaurant_id="1",
                name="Alpha",
                cuisine="Chinese",
                rating=4.8,
                estimated_cost=800,
                explanation="Top pick",
            ),
            Recommendation(
                rank=2,
                restaurant_id="2",
                name="Beta",
                cuisine="Chinese",
                rating=4.6,
                estimated_cost=700,
                explanation="Runner up",
            ),
        ],
    )

    normalized = normalize_recommendations(
        response,
        _integration_result(candidates),
        top_n=5,
    )

    assert len(normalized.recommendations) == 5
    ids = [item.restaurant_id for item in normalized.recommendations]
    assert len(set(ids)) == 5
