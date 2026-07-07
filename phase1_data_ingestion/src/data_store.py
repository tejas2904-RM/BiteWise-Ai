from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import pandas as pd

from .models import BudgetTier, Restaurant


class RestaurantDataStore:
    """In-memory restaurant store with query helpers and parquet persistence."""

    def __init__(self, restaurants: Optional[list[Restaurant]] = None) -> None:
        self._restaurants = restaurants or []
        self._df: Optional[pd.DataFrame] = None
        if self._restaurants:
            self._refresh_dataframe()

    @property
    def restaurants(self) -> list[Restaurant]:
        return list(self._restaurants)

    @property
    def dataframe(self) -> pd.DataFrame:
        if self._df is None:
            self._refresh_dataframe()
        return self._df.copy()

    def __len__(self) -> int:
        return len(self._restaurants)

    def _refresh_dataframe(self) -> None:
        records = [restaurant.model_dump() for restaurant in self._restaurants]
        self._df = pd.DataFrame(records)

    def load(self, restaurants: list[Restaurant]) -> None:
        self._restaurants = restaurants
        self._refresh_dataframe()

    def save_parquet(self, path: Union[str, Path]) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.dataframe.to_parquet(output_path, index=False)
        return output_path

    def save_csv(self, path: Union[str, Path]) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.dataframe.to_csv(output_path, index=False)
        return output_path

    @classmethod
    def from_parquet(cls, path: Union[str, Path]) -> "RestaurantDataStore":
        df = pd.read_parquet(path)
        restaurants = [Restaurant(**row) for row in df.to_dict(orient="records")]
        return cls(restaurants)

    @classmethod
    def from_csv(cls, path: Union[str, Path]) -> "RestaurantDataStore":
        df = pd.read_csv(path)
        restaurants = [Restaurant(**row) for row in df.to_dict(orient="records")]
        return cls(restaurants)

    def query(
        self,
        *,
        location: Optional[str] = None,
        cuisine: Optional[str] = None,
        budget: Optional[Union[BudgetTier, str]] = None,
        min_rating: Optional[float] = None,
        limit: Optional[int] = None,
    ) -> list[Restaurant]:
        """Filter restaurants by location, cuisine, budget tier, and minimum rating."""
        results = self._restaurants
        location_query = location.strip().lower() if location else None
        cuisine_query = cuisine.strip().lower() if cuisine else None

        if location_query:
            results = [
                restaurant
                for restaurant in results
                if location_query in restaurant.city.lower()
                or location_query in restaurant.locality.lower()
                or location_query in restaurant.location.lower()
            ]

        if cuisine_query:
            results = [
                restaurant
                for restaurant in results
                if any(cuisine_query in item.lower() for item in restaurant.cuisines)
            ]

        if budget is not None:
            budget_tier = budget if isinstance(budget, BudgetTier) else BudgetTier(str(budget).lower())
            results = [restaurant for restaurant in results if restaurant.budget_tier == budget_tier]

        if min_rating is not None:
            results = [restaurant for restaurant in results if restaurant.rating >= min_rating]

        if limit is not None:
            results = results[:limit]

        return results

    def summary(self) -> dict[str, object]:
        df = self.dataframe
        return {
            "total_restaurants": len(self),
            "cities": int(df["city"].nunique()) if not df.empty else 0,
            "cuisines": int(df["cuisines"].explode().nunique()) if not df.empty else 0,
            "avg_rating": round(float(df["rating"].mean()), 2) if not df.empty else 0.0,
            "budget_distribution": (
                df["budget_tier"].value_counts().to_dict() if not df.empty else {}
            ),
        }
