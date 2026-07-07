from __future__ import annotations

from pathlib import Path
from typing import Union

from integration.phase_imports import Restaurant, RestaurantDataStore, UserPreferences

from .candidate_selector import CandidateSelector
from .context_formatter import ContextFormatter
from .filter_service import FilterService
from .models import IntegrationResult
from .prompt_builder import PromptBuilder

DEFAULT_MAX_CANDIDATES = 20
DEFAULT_MAX_PROMPT_TOKENS = 8000


def run_integration(
    preferences: UserPreferences,
    store: RestaurantDataStore,
    *,
    max_candidates: int = DEFAULT_MAX_CANDIDATES,
    max_prompt_tokens: int = DEFAULT_MAX_PROMPT_TOKENS,
) -> IntegrationResult:
    """Filter restaurants, select candidates, and build an LLM-ready prompt."""
    filter_service = FilterService()
    selector = CandidateSelector(max_candidates=max_candidates)
    formatter = ContextFormatter()
    prompt_builder = PromptBuilder()

    filter_result = filter_service.filter(store, preferences)
    selected = selector.select(filter_result.restaurants)
    candidates = formatter.format_many(selected)

    prompt = prompt_builder.build(preferences, candidates, filter_result.relaxed_filters)

    while candidates and prompt.estimated_tokens > max_prompt_tokens:
        candidates = candidates[:-5]
        prompt = prompt_builder.build(preferences, candidates, filter_result.relaxed_filters)

    return IntegrationResult(
        preferences=preferences.model_dump(),
        total_matches=len(filter_result.restaurants),
        candidate_count=len(candidates),
        relaxed_filters=filter_result.relaxed_filters,
        candidates=candidates,
        prompt=prompt,
    )


def _normalize_record(row: dict[str, object]) -> dict[str, object]:
    import pandas as pd

    record = dict(row)
    cuisines = record.get("cuisines")
    if cuisines is not None:
        record["cuisines"] = list(cuisines)

    for field in ("address", "rest_type", "votes", "online_order", "book_table"):
        value = record.get(field)
        if value is not None and pd.isna(value):
            record[field] = None

    return record


def load_data_store(path: Union[str, Path]) -> RestaurantDataStore:
    import pandas as pd

    data_path = Path(path)
    if data_path.suffix == ".parquet":
        df = pd.read_parquet(data_path)
        restaurants = [
            Restaurant(**_normalize_record(row))
            for row in df.to_dict(orient="records")
        ]
        return RestaurantDataStore(restaurants)
    if data_path.suffix == ".csv":
        return RestaurantDataStore.from_csv(data_path)
    raise ValueError(f"Unsupported data file format: {data_path}")
