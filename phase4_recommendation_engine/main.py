from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import recommendation.phase_imports as _phase_imports  # noqa: F401
from recommendation.phase_imports import (
    DEFAULT_DATA_PATH,
    ValidationError,
    validate_preferences,
)
from recommendation.pipeline import (
    generate_recommendations,
    load_integration_result,
    load_data_store,
    run_recommendation_pipeline,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Phase 4: Generate restaurant recommendations with OpenAI.",
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to Phase 1 processed restaurant data.",
    )
    parser.add_argument(
        "--integration-file",
        type=Path,
        default=None,
        help="Optional Phase 3 integration JSON (skips re-running integration).",
    )
    parser.add_argument("--location", type=str, help='City or locality, e.g. "Bangalore"')
    parser.add_argument("--cuisine", type=str, help='Cuisine, e.g. "Chinese"')
    parser.add_argument("--budget", choices=["low", "medium", "high"], help="Budget tier")
    parser.add_argument("--min-rating", type=float, help="Minimum rating (0-5)")
    parser.add_argument("--notes", type=str, default=None, help="Additional preference notes")
    parser.add_argument("--top-n", type=int, default=5, help="Number of recommendations to return.")
    parser.add_argument(
        "--fallback-only",
        action="store_true",
        help="Skip OpenAI and use rule-based fallback ranking.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to write RecommendationResponse JSON.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.integration_file:
        if not args.integration_file.exists():
            print(f"Integration file not found: {args.integration_file}", file=sys.stderr)
            raise SystemExit(1)
        integration_result = load_integration_result(args.integration_file)
        response = generate_recommendations(
            integration_result,
            top_n=args.top_n,
            use_openai=not args.fallback_only,
        )
    else:
        required = [args.location, args.cuisine, args.budget, args.min_rating is not None]
        if not all(required):
            print(
                "Provide --location, --cuisine, --budget, and --min-rating "
                "or pass --integration-file.",
                file=sys.stderr,
            )
            raise SystemExit(1)

        if not args.data.exists():
            print(f"Data file not found: {args.data}", file=sys.stderr)
            raise SystemExit(1)

        try:
            preferences = validate_preferences(
                {
                    "location": args.location,
                    "cuisine": args.cuisine,
                    "budget": args.budget,
                    "min_rating": args.min_rating,
                    "additional_notes": args.notes,
                }
            )
        except ValidationError as exc:
            print(exc.message, file=sys.stderr)
            raise SystemExit(1) from exc

        store = load_data_store(args.data)
        response = run_recommendation_pipeline(
            preferences,
            store,
            top_n=args.top_n,
            use_openai=not args.fallback_only,
        )

    print(json.dumps(response.model_dump(), indent=2))

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(response.model_dump_json(indent=2), encoding="utf-8")
        print(f"\nWrote recommendations to: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
