from __future__ import annotations

from backend.models.schemas import RestaurantDetailResponse
from backend.config import get_settings
from backend.phase_bridge import load_data_store


class RestaurantNotFoundError(Exception):
    def __init__(self, restaurant_id: str) -> None:
        super().__init__(f"Restaurant not found: {restaurant_id}")
        self.restaurant_id = restaurant_id


class RestaurantService:
    """Lookup restaurant details from Phase 1 data store."""

    def __init__(self) -> None:
        self._store = None

    def _get_store(self):
        if self._store is None:
            settings = get_settings()
            self._store = load_data_store(settings["data_path"])
        return self._store

    @property
    def restaurant_count(self) -> int:
        return len(self._get_store())

    def get_by_id(self, restaurant_id: str) -> RestaurantDetailResponse:
        store = self._get_store()
        for restaurant in store.restaurants:
            if restaurant.id == restaurant_id:
                return RestaurantDetailResponse(
                    id=restaurant.id,
                    name=restaurant.name,
                    location=restaurant.location,
                    city=restaurant.city,
                    locality=restaurant.locality,
                    cuisines=restaurant.cuisines,
                    cost_for_two=restaurant.cost_for_two,
                    budget_tier=restaurant.budget_tier.value,
                    rating=restaurant.rating,
                    address=restaurant.address,
                    votes=restaurant.votes,
                    rest_type=restaurant.rest_type,
                    online_order=restaurant.online_order,
                    book_table=restaurant.book_table,
                )
        raise RestaurantNotFoundError(restaurant_id)


restaurant_service = RestaurantService()
