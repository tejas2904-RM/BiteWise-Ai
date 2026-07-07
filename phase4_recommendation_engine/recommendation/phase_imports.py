from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PHASE3_ROOT = PROJECT_ROOT / "phase3_integration_layer"

if str(PHASE3_ROOT) not in sys.path:
    sys.path.insert(0, str(PHASE3_ROOT))

load_dotenv(PROJECT_ROOT / "phase4_recommendation_engine" / ".env")

from integration.models import CandidateRestaurant, IntegrationResult, LLMPrompt  # noqa: E402
from integration.phase_imports import (  # noqa: E402
    BudgetTier,
    Restaurant,
    RestaurantDataStore,
    UserPreferences,
    ValidationError,
    validate_preferences,
)
from integration.pipeline import load_data_store, run_integration  # noqa: E402

DEFAULT_DATA_PATH = (
    PROJECT_ROOT / "phase1_data_ingestion" / "data" / "processed" / "restaurants.parquet"
)


def get_openai_api_key() -> str | None:
    return os.getenv("OPENAI_API_KEY")


def get_openai_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")


__all__ = [
    "BudgetTier",
    "CandidateRestaurant",
    "DEFAULT_DATA_PATH",
    "IntegrationResult",
    "LLMPrompt",
    "Restaurant",
    "RestaurantDataStore",
    "UserPreferences",
    "ValidationError",
    "get_openai_api_key",
    "get_openai_model",
    "load_data_store",
    "run_integration",
    "validate_preferences",
]
