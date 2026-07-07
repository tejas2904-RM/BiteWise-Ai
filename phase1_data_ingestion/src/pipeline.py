from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

from .data_store import RestaurantDataStore
from .loader import DEFAULT_DATASET_ID, load_raw_dataset
from .schema_mapper import map_raw_records

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"


def run_ingestion_pipeline(
    *,
    dataset_id: str = DEFAULT_DATASET_ID,
    output_dir: Union[str, Path] = DEFAULT_OUTPUT_DIR,
    save_outputs: bool = True,
) -> RestaurantDataStore:
    """Load, preprocess, map, and optionally persist restaurant data."""
    raw_records = load_raw_dataset(dataset_id)
    restaurants = map_raw_records(raw_records)
    store = RestaurantDataStore(restaurants)

    if save_outputs:
        output_path = Path(output_dir)
        store.save_parquet(output_path / "restaurants.parquet")
        store.save_csv(output_path / "restaurants.csv")

    return store
