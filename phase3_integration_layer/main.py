from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from integration.phase_imports import (
    PROJECT_ROOT,
    BudgetTier,
    ValidationError,
    validate_preferences,
)
from integration.pipeline import load_data_store, run_integration

DEFAULT_DATA_PATH = (
    PROJECT_ROOT / "phase1_data_ingestion" / "data" / "processed" / "restaurants.parquet"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Phase 3: Filter restaurants and build an LLM-ready prompt.",
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to Phase 1 processed restaurant data (parquet or csv).",
    )
    parser.add_argument("--location", required=True, help='City or locality, e.g. "Bangalore"')
    parser.add_argument("--cuisine", required=True, help='Cuisine, e.g. "Chinese"')
    parser.add_argument(
        "--budget",
        required=True,
        choices=[tier.value for tier in BudgetTier],
        help="Budget tier: low, medium, or high",
    )
    parser.add_argument("--min-rating", type=float, required=True, help="Minimum rating (0-5)")
    parser.add_argument("--notes", type=str, default=None, help="Additional preference notes")
    parser.add_argument(
        "--max-candidates",
        type=int,
        default=20,
        help="Maximum candidate restaurants in the LLM context.",
    )
    parser.add_argument(
        "--max-prompt-tokens",
        type=int,
        default=8000,
        help="Trim candidates until the prompt is under this token estimate.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to write the integration result JSON.",
    )
    parser.add_argument(
        "--show-prompt",
        action="store_true",
        help="Print the generated system and user prompts.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if not args.data.exists():
        print(f"Data file not found: {args.data}", file=sys.stderr)
        print("Run Phase 1 ingestion first or pass --data.", file=sys.stderr)
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
    result = run_integration(
        preferences,
        store,
        max_candidates=args.max_candidates,
        max_prompt_tokens=args.max_prompt_tokens,
    )

    summary = {
        "total_matches": result.total_matches,
        "candidate_count": result.candidate_count,
        "relaxed_filters": result.relaxed_filters,
        "estimated_tokens": result.prompt.estimated_tokens,
        "preferences": result.preferences,
    }
    print(json.dumps(summary, indent=2))

    if args.show_prompt:
        print("\n--- SYSTEM PROMPT ---\n")
        print(result.prompt.system_prompt)
        print("\n--- USER PROMPT ---\n")
        print(result.prompt.user_prompt)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result.model_dump_json(indent=2), encoding="utf-8")
        print(f"\nWrote integration result to: {args.output}")


if __name__ == "__main__":
    main()
