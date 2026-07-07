from __future__ import annotations

import hashlib
import re
from typing import Any, Optional

from .models import BudgetTier

_CITY_ALIASES = {
    "bengaluru": "Bangalore",
    "bangalore": "Bangalore",
    "banglore": "Bangalore",
    "bengalore": "Bangalore",
    "btm bangalore": "Bangalore",
    "delhi": "Delhi",
    "new delhi": "Delhi",
    "ncr": "Delhi",
    "gurgaon": "Gurgaon",
    "gurugram": "Gurgaon",
    "mumbai": "Mumbai",
    "bombay": "Mumbai",
    "hyderabad": "Hyderabad",
    "chennai": "Chennai",
    "kolkata": "Kolkata",
    "calcutta": "Kolkata",
    "pune": "Pune",
}

_COST_RANGE_PATTERN = re.compile(r"^\s*(\d+)\s*-\s*(\d+)\s*$")
_RATING_PATTERN = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*/\s*5\s*$")


def normalize_text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return re.sub(r"\s+", " ", text) if text else default


def parse_cuisines(value: Any) -> list[str]:
    text = normalize_text(value)
    if not text:
        return ["Unknown"]
    cuisines = [part.strip() for part in text.split(",") if part.strip()]
    return cuisines or ["Unknown"]


def parse_cost_for_two(value: Any, default: float = 500.0) -> float:
    text = normalize_text(value)
    if not text:
        return default

    range_match = _COST_RANGE_PATTERN.match(text)
    if range_match:
        low = float(range_match.group(1))
        high = float(range_match.group(2))
        return (low + high) / 2

    digits = re.sub(r"[^\d.]", "", text)
    if not digits:
        return default

    try:
        return float(digits)
    except ValueError:
        return default


def parse_rating(value: Any, default: float = 0.0) -> float:
    text = normalize_text(value)
    if not text or text.upper() in {"NEW", "-", "NA", "N/A"}:
        return default

    match = _RATING_PATTERN.match(text)
    if match:
        return float(match.group(1))

    try:
        rating = float(text)
        return rating if 0 <= rating <= 5 else default
    except ValueError:
        return default


def parse_votes(value: Any) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_yes_no(value: Any) -> Optional[bool]:
    text = normalize_text(value).lower()
    if text == "yes":
        return True
    if text == "no":
        return False
    return None


def extract_city(address: Any, fallback: str = "") -> str:
    text = normalize_text(address)
    if not text:
        return normalize_city(fallback)

    parts = [part.strip() for part in text.split(",") if part.strip()]
    for part in reversed(parts):
        city = normalize_city(part)
        if city:
            return city

    return normalize_city(fallback) or "Unknown"


def normalize_city(value: Any) -> str:
    text = normalize_text(value)
    if not text:
        return ""

    key = text.lower()
    if key in _CITY_ALIASES:
        return _CITY_ALIASES[key]

    if key.endswith(" bangalore") or "bangalore" in key:
        return "Bangalore"

    return text.title()


def assign_budget_tier(cost_for_two: float) -> BudgetTier:
    if cost_for_two < 500:
        return BudgetTier.LOW
    if cost_for_two <= 1000:
        return BudgetTier.MEDIUM
    return BudgetTier.HIGH


def build_restaurant_id(url: str, name: str, address: str) -> str:
    seed = url or f"{name}|{address}"
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]
