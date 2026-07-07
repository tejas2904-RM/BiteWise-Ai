"""Ensure processed restaurant data exists before Render starts the API."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PARQUET_PATH = REPO_ROOT / "phase1_data_ingestion" / "data" / "processed" / "restaurants.parquet"
PHASE1_DIR = REPO_ROOT / "phase1_data_ingestion"
PHASE1_REQUIREMENTS = PHASE1_DIR / "requirements.txt"


def main() -> int:
    if PARQUET_PATH.is_file():
        print(f"Restaurant data found: {PARQUET_PATH}")
        return 0

    print(f"Restaurant data missing at {PARQUET_PATH}; running Phase 1 ingestion...")
    PARQUET_PATH.parent.mkdir(parents=True, exist_ok=True)

    if PHASE1_REQUIREMENTS.is_file():
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(PHASE1_REQUIREMENTS)],
            check=True,
        )

    subprocess.run(
        [sys.executable, "main.py"],
        cwd=PHASE1_DIR,
        check=True,
    )

    if not PARQUET_PATH.is_file():
        print("Phase 1 completed but parquet file was not created.", file=sys.stderr)
        return 1

    print(f"Restaurant data generated: {PARQUET_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
