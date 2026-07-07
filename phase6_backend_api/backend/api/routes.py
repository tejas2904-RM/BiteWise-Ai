from __future__ import annotations

from fastapi import APIRouter, Query

from contract.models import RecommendationRequest, RecommendationResponse
from backend.models.schemas import HealthResponse, RestaurantDetailResponse, SearchHistoryResponse
from backend.services.recommendation_service import recommendation_service
from backend.services.restaurant_service import restaurant_service
from backend.services.search_history import search_history_store

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        restaurants_loaded=restaurant_service.restaurant_count,
    )


@router.post(
    "/api/recommendations",
    response_model=RecommendationResponse,
    tags=["recommendations"],
)
def create_recommendations(
    request: RecommendationRequest,
    top_n: int = Query(default=5, ge=1, le=10),
    fallback_only: bool = Query(default=False, description="Skip OpenAI and use rule-based ranking."),
) -> RecommendationResponse:
    response = recommendation_service.create_recommendations(
        request,
        top_n=top_n,
        use_openai=not fallback_only,
    )
    search_history_store.add(request)
    return response


@router.get(
    "/api/restaurants/{restaurant_id}",
    response_model=RestaurantDetailResponse,
    tags=["restaurants"],
)
def get_restaurant(restaurant_id: str) -> RestaurantDetailResponse:
    return restaurant_service.get_by_id(restaurant_id)


@router.get(
    "/api/search/history",
    response_model=SearchHistoryResponse,
    tags=["search"],
)
def get_search_history(limit: int = Query(default=10, ge=1, le=20)) -> SearchHistoryResponse:
    return search_history_store.list(limit=limit)
