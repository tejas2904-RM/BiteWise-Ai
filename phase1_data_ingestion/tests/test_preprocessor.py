from src.preprocessor import (
    assign_budget_tier,
    extract_city,
    parse_cost_for_two,
    parse_cuisines,
    parse_rating,
)
from src.models import BudgetTier


def test_parse_rating():
    assert parse_rating("4.1/5") == 4.1
    assert parse_rating("NEW") == 0.0


def test_parse_cost_for_two():
    assert parse_cost_for_two("800") == 800.0
    assert parse_cost_for_two("300-400") == 350.0


def test_parse_cuisines():
    assert parse_cuisines("North Indian, Chinese") == ["North Indian", "Chinese"]


def test_extract_city():
    assert extract_city("942, Banashankari, Bangalore") == "Bangalore"
    assert extract_city("", fallback="Banashankari") == "Banashankari"


def test_assign_budget_tier():
    assert assign_budget_tier(300) == BudgetTier.LOW
    assert assign_budget_tier(750) == BudgetTier.MEDIUM
    assert assign_budget_tier(1500) == BudgetTier.HIGH
