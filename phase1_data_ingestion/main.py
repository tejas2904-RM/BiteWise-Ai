from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.pipeline import run_ingestion_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Phase 1: Load and preprocess the Zomato restaurant dataset.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/processed"),
        help="Directory for processed parquet/csv outputs.",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Skip writing processed files to disk.",
    )
    parser.add_argument(
        "--location",
        type=str,
        help="Optional query filter: city or locality.",
    )
    parser.add_argument(
        "--cuisine",
        type=str,
        help="Optional query filter: cuisine name.",
    )
    parser.add_argument(
        "--budget",
        choices=["low", "medium", "high"],
        help="Optional query filter: budget tier.",
    )
    parser.add_argument(
        "--min-rating",
        type=float,
        help="Optional query filter: minimum rating.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of sample query results to print.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    print("Loading dataset from Hugging Face...")
    store = run_ingestion_pipeline(
        output_dir=args.output_dir,
        save_outputs=not args.no_save,
    )

    summary = store.summary()
    print("\nIngestion complete.")
    print(json.dumps(summary, indent=2))

    if not args.no_save:
        print(f"\nSaved: {args.output_dir / 'restaurants.parquet'}")
        print(f"Saved: {args.output_dir / 'restaurants.csv'}")

    if any([args.location, args.cuisine, args.budget, args.min_rating is not None]):
        results = store.query(
            location=args.location,
            cuisine=args.cuisine,
            budget=args.budget,
            min_rating=args.min_rating,
            limit=args.limit,
        )
        print(f"\nQuery returned {len(results)} result(s). Showing up to {args.limit}:")
        for restaurant in results:
            print(
                f"- {restaurant.name} | {restaurant.location} | "
                f"{', '.join(restaurant.cuisines)} | "
                f"rating={restaurant.rating} | cost={restaurant.cost_for_two} | "
                f"budget={restaurant.budget_tier.value}"
            )


if __name__ == "__main__":
    main()
