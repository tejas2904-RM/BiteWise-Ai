from __future__ import annotations

import os
import sys
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PHASE6_ROOT = Path(__file__).resolve().parent.parent

for folder in (
    "phase3_integration_layer",
    "phase4_recommendation_engine",
    "phase5_response_contract",
    "phase1_data_ingestion",
):
    path = PROJECT_ROOT / folder
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

load_dotenv(PHASE6_ROOT / ".env")
load_dotenv(PROJECT_ROOT / "phase4_recommendation_engine" / ".env")

DEFAULT_DATA_PATH = (
    PROJECT_ROOT / "phase1_data_ingestion" / "data" / "processed" / "restaurants.parquet"
)


def resolve_data_path(raw: str | Path | None = None) -> Path:
    """Resolve DATA_PATH for local dev and Render (relative paths from phase6 or repo root)."""
    if raw is None:
        raw = os.getenv("DATA_PATH")
    if not raw:
        return DEFAULT_DATA_PATH

    path = Path(raw)
    if path.is_absolute():
        return path

    candidates = (
        PHASE6_ROOT / path,
        PROJECT_ROOT / path,
        PROJECT_ROOT / Path(str(path).lstrip("./")),
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return candidates[0]


VERCEL_PREVIEW_ORIGIN_REGEX = r"https://.*\.vercel\.app"


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


@lru_cache
def get_settings() -> dict[str, object]:
    cors_raw = os.getenv("CORS_ORIGINS", "http://localhost:3000")
    cors_origins = [origin.strip() for origin in cors_raw.split(",") if origin.strip()]

    cors_origin_regex = os.getenv("CORS_ORIGIN_REGEX", "").strip() or None
    if _truthy(os.getenv("CORS_ALLOW_VERCEL_PREVIEWS")):
        cors_origin_regex = cors_origin_regex or VERCEL_PREVIEW_ORIGIN_REGEX

    return {
        "data_path": resolve_data_path(),
        "cors_origins": cors_origins,
        "cors_origin_regex": cors_origin_regex,
        "api_host": os.getenv("API_HOST", "0.0.0.0"),
        "api_port": int(os.getenv("PORT", os.getenv("API_PORT", "8000"))),
    }
