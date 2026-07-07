from __future__ import annotations

import json
from pathlib import Path

from .errors import ErrorResponse
from .models import Recommendation, RecommendationRequest, RecommendationResponse


def export_json_schemas(output_dir: Path) -> dict[str, Path]:
    """Export JSON Schema files for OpenAPI, frontend, and documentation."""
    output_dir.mkdir(parents=True, exist_ok=True)
    models: list[tuple[str, type]] = [
        ("recommendation_request", RecommendationRequest),
        ("recommendation", Recommendation),
        ("recommendation_response", RecommendationResponse),
        ("error_response", ErrorResponse),
    ]

    written: dict[str, Path] = {}
    for name, model in models:
        schema = model.model_json_schema()
        path = output_dir / f"{name}.schema.json"
        path.write_text(json.dumps(schema, indent=2), encoding="utf-8")
        written[name] = path

    bundle = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "BiteWise API Contract",
        "schemas": {name: model.model_json_schema() for name, model in models},
    }
    bundle_path = output_dir / "api_contract.bundle.json"
    bundle_path.write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    written["bundle"] = bundle_path

    return written


def export_typescript_types(output_path: Path) -> Path:
    """Write TypeScript types mirroring the Python contract for Phase 7."""
    content = """// Auto-aligned with phase5_response_contract — do not edit by hand unless syncing Python models.

export type BudgetTier = "low" | "medium" | "high";

export type RecommendationSource = "openai" | "fallback";

export type ErrorCode =
  | "validation_error"
  | "no_matches"
  | "openai_error"
  | "server_error";

export interface UserPreferences {
  location: string;
  budget: BudgetTier;
  cuisine: string;
  min_rating: number;
  additional_notes?: string | null;
}

export interface RecommendationRequest {
  location: string;
  budget: BudgetTier;
  cuisine: string;
  min_rating: number;
  additional_notes?: string | null;
}

export interface Recommendation {
  rank: number;
  restaurant_id: string;
  name: string;
  cuisine: string;
  rating: number;
  estimated_cost: string | number;
  explanation: string;
}

export interface RecommendationResponse {
  summary?: string | null;
  recommendations: Recommendation[];
  source: RecommendationSource;
  preferences?: UserPreferences | null;
  total_matches?: number | null;
}

export interface FieldError {
  field: string;
  message: string;
}

export interface ErrorDetails {
  errors?: FieldError[] | null;
  extra?: Record<string, unknown> | null;
}

export interface ErrorResponse {
  message: string;
  code: ErrorCode;
  details?: ErrorDetails | Record<string, unknown> | null;
}
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return output_path
