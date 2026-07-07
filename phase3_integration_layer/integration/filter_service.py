from __future__ import annotations

from dataclasses import dataclass

from integration.phase_imports import BudgetTier, Restaurant, RestaurantDataStore, UserPreferences


def _query_kwargs(preferences: UserPreferences) -> dict[str, object]:
    kwargs = preferences.to_filter_kwargs()
    budget = kwargs.get("budget")
    if budget is not None:
        kwargs["budget"] = BudgetTier(budget.value if hasattr(budget, "value") else budget)
    return kwargs


@dataclass
class FilterResult:
    restaurants: list[Restaurant]
    relaxed_filters: list[str]


class FilterService:
    """Apply hard filters from user preferences with graceful fallback."""

    def filter(self, store: RestaurantDataStore, preferences: UserPreferences) -> FilterResult:
        base_kwargs = _query_kwargs(preferences)
        matches = store.query(**base_kwargs)
        if matches:
            return FilterResult(restaurants=matches, relaxed_filters=[])

        relaxed: list[str] = []

        without_budget = {key: value for key, value in base_kwargs.items() if key != "budget"}
        matches = store.query(**without_budget)
        if matches:
            relaxed.append("budget")
            return FilterResult(restaurants=matches, relaxed_filters=relaxed)

        without_rating = {key: value for key, value in without_budget.items() if key != "min_rating"}
        matches = store.query(**without_rating)
        if matches:
            relaxed.extend(["budget", "min_rating"])
            return FilterResult(restaurants=matches, relaxed_filters=relaxed)

        location_only = {"location": preferences.location}
        matches = store.query(**location_only)
        if matches:
            relaxed.extend(["budget", "min_rating", "cuisine"])
            return FilterResult(restaurants=matches, relaxed_filters=relaxed)

        return FilterResult(restaurants=[], relaxed_filters=["all"])
