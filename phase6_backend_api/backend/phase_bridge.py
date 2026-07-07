from __future__ import annotations

from integration.phase_imports import ValidationError, validate_preferences
from integration.pipeline import load_data_store, run_integration
from recommendation.pipeline import generate_recommendations

from contract.adapters import from_phase4_response
from contract.errors import ErrorCode, ErrorResponse, build_error_response
from contract.models import (
    RecommendationRequest,
    RecommendationResponse,
    UserPreferences as ContractUserPreferences,
)

from backend.config import DEFAULT_DATA_PATH, get_settings

__all__ = [
    "ContractUserPreferences",
    "DEFAULT_DATA_PATH",
    "ErrorCode",
    "ErrorResponse",
    "RecommendationRequest",
    "RecommendationResponse",
    "ValidationError",
    "build_error_response",
    "from_phase4_response",
    "generate_recommendations",
    "get_settings",
    "load_data_store",
    "run_integration",
    "validate_preferences",
]
