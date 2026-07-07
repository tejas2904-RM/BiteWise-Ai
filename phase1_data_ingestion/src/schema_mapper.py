from __future__ import annotations

from typing import Any

from .models import Restaurant
from .preprocessor import (
    assign_budget_tier,
    build_restaurant_id,
    extract_city,
    normalize_text,
    parse_cost_for_two,
    parse_cuisines,
    parse_rating,
    parse_votes,
    parse_yes_no,
)


def map_raw_record(raw: dict[str, Any], index: int) -> Restaurant:
    """Map a Hugging Face dataset row to the internal Restaurant schema."""
    name = normalize_text(raw.get("name"), default=f"Restaurant {index + 1}")
    address = normalize_text(raw.get("address"))
    locality = normalize_text(raw.get("location")) or normalize_text(raw.get("listed_in(city)"))
    listed_city = normalize_text(raw.get("listed_in(city)"))
    city = extract_city(address, fallback=listed_city)

    cost_for_two = parse_cost_for_two(raw.get("approx_cost(for two people)"))
    rating = parse_rating(raw.get("rate"))

    location = f"{city}, {locality}" if locality and locality.lower() != city.lower() else city

    return Restaurant(
        id=build_restaurant_id(
            normalize_text(raw.get("url")),
            name,
            address,
        ),
        name=name,
        location=location,
        city=city,
        locality=locality or city,
        cuisines=parse_cuisines(raw.get("cuisines")),
        cost_for_two=cost_for_two,
        budget_tier=assign_budget_tier(cost_for_two),
        rating=rating,
        address=address or None,
        votes=parse_votes(raw.get("votes")),
        rest_type=normalize_text(raw.get("rest_type")) or None,
        online_order=parse_yes_no(raw.get("online_order")),
        book_table=parse_yes_no(raw.get("book_table")),
    )


def map_raw_records(raw_records: list[dict[str, Any]]) -> list[Restaurant]:
    return [map_raw_record(record, index) for index, record in enumerate(raw_records)]
