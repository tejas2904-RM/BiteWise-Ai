from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def _load_module(module_name: str, file_path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _load_phase1() -> None:
    phase1_root = PROJECT_ROOT / "phase1_data_ingestion"
    if str(phase1_root) not in sys.path:
        sys.path.insert(0, str(phase1_root))


def _load_phase2_models_and_validator() -> tuple[ModuleType, ModuleType]:
    phase2_root = PROJECT_ROOT / "phase2_user_input"
    src_pkg = ModuleType("phase2_src")
    src_pkg.__path__ = [str(phase2_root / "src")]
    sys.modules["phase2_src"] = src_pkg

    models = _load_module(
        "phase2_src.models",
        phase2_root / "src" / "models.py",
    )
    src_pkg.models = models

    validator = _load_module(
        "phase2_src.validator",
        phase2_root / "src" / "validator.py",
    )
    return models, validator


_load_phase1()

from src.data_store import RestaurantDataStore  # noqa: E402
from src.models import BudgetTier, Restaurant  # noqa: E402

_phase2_models, _phase2_validator = _load_phase2_models_and_validator()

UserPreferences = _phase2_models.UserPreferences
PreferenceInput = _phase2_models.PreferenceInput
validate_preferences = _phase2_validator.validate_preferences
ValidationError = _phase2_validator.ValidationError

__all__ = [
    "BudgetTier",
    "PreferenceInput",
    "Restaurant",
    "RestaurantDataStore",
    "UserPreferences",
    "ValidationError",
    "validate_preferences",
]
