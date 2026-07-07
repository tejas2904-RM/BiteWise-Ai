from __future__ import annotations

from typing import Any

from datasets import load_dataset

DEFAULT_DATASET_ID = "ManikaSaini/zomato-restaurant-recommendation"


def load_raw_dataset(dataset_id: str = DEFAULT_DATASET_ID) -> list[dict[str, Any]]:
    """Fetch the Zomato dataset from Hugging Face."""
    dataset = load_dataset(dataset_id, split="train")
    return [dict(row) for row in dataset]
