"""Phase 5: Shared API response contract for backend and frontend."""

from .adapters import from_phase4_response, to_contract_response
from .errors import ErrorCode, ErrorResponse, build_error_response
from .models import (
    BudgetTier,
    Recommendation,
    RecommendationRequest,
    RecommendationResponse,
    UserPreferences,
)

__all__ = [
    "BudgetTier",
    "ErrorCode",
    "ErrorResponse",
    "Recommendation",
    "RecommendationRequest",
    "RecommendationResponse",
    "UserPreferences",
    "build_error_response",
    "from_phase4_response",
    "to_contract_response",
]
