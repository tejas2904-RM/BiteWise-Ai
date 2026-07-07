from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .models import BudgetTier, UserPreferences
from .validator import ValidationError, validate_preferences


def collect_interactive_input() -> dict[str, Any]:
    print("Enter your restaurant preferences.\n")

    location = input("Location (e.g. Bangalore): ").strip()
    cuisine = input("Cuisine (e.g. Chinese): ").strip()
    budget = input("Budget (low / medium / high): ").strip().lower()
    min_rating_raw = input("Minimum rating (0-5, e.g. 4.0): ").strip()
    additional_notes = input("Additional notes (optional): ").strip()

    try:
        min_rating = float(min_rating_raw)
    except ValueError:
        min_rating = min_rating_raw

    payload: dict[str, Any] = {
        "location": location,
        "cuisine": cuisine,
        "budget": budget,
        "min_rating": min_rating,
    }
    if additional_notes:
        payload["additional_notes"] = additional_notes
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Phase 2: Collect user restaurant preferences.")
    parser.add_argument("--location", type=str, help='City or locality, e.g. "Bangalore"')
    parser.add_argument("--cuisine", type=str, help='Cuisine, e.g. "Chinese"')
    parser.add_argument(
        "--budget",
        type=str,
        choices=[tier.value for tier in BudgetTier],
        help="Budget tier: low, medium, or high",
    )
    parser.add_argument("--min-rating", type=float, help="Minimum rating between 0 and 5")
    parser.add_argument(
        "--notes",
        type=str,
        default=None,
        help='Additional preferences, e.g. "family-friendly, quick service"',
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Prompt for preferences interactively.",
    )
    return parser


def run_cli(argv: list[str] | None = None) -> UserPreferences:
    args = build_parser().parse_args(argv)

    if args.interactive or not all([args.location, args.cuisine, args.budget, args.min_rating is not None]):
        payload = collect_interactive_input()
    else:
        payload = {
            "location": args.location,
            "cuisine": args.cuisine,
            "budget": args.budget,
            "min_rating": args.min_rating,
        }
        if args.notes:
            payload["additional_notes"] = args.notes

    try:
        preferences = validate_preferences(payload)
    except ValidationError as exc:
        print(exc.message, file=sys.stderr)
        for error in exc.errors:
            print(f"  - {error['field']}: {error['message']}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(preferences.model_dump(), indent=2))
    return preferences
