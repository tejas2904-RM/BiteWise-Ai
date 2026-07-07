from __future__ import annotations

import os
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
RENDER_YAML = REPO_ROOT / "render.yaml"
ENSURE_DATA_SCRIPT = REPO_ROOT / "phase8_backend_deploy" / "scripts" / "ensure_data.py"


def test_render_yaml_exists_and_has_web_service():
    assert RENDER_YAML.is_file(), "render.yaml must live at repository root for Render Blueprints"

    config = yaml.safe_load(RENDER_YAML.read_text(encoding="utf-8"))
    services = config.get("services", [])
    assert services, "render.yaml must define at least one service"

    api = services[0]
    assert api["type"] == "web"
    assert api["rootDir"] == "phase6_backend_api"
    assert api["healthCheckPath"] == "/health"
    assert "uvicorn backend.api.app:app" in api["startCommand"]
    assert "ensure_data.py" in api["buildCommand"]


def test_ensure_data_script_paths():
    text = ENSURE_DATA_SCRIPT.read_text(encoding="utf-8")
    assert "phase1_data_ingestion" in text
    assert "restaurants.parquet" in text


def test_data_path_resolution_from_config(monkeypatch: pytest.MonkeyPatch):
    phase6_root = REPO_ROOT / "phase6_backend_api"
    monkeypatch.chdir(phase6_root)
    monkeypatch.delenv("DATA_PATH", raising=False)

    import sys

    if str(phase6_root) not in sys.path:
        sys.path.insert(0, str(phase6_root))

    import backend.config as config_module
    from backend.config import get_settings, resolve_data_path

    config_module.get_settings.cache_clear()

    relative = "../phase1_data_ingestion/data/processed/restaurants.parquet"
    resolved = resolve_data_path(relative)
    assert resolved.is_absolute()
    assert resolved.name == "restaurants.parquet"
    assert "phase1_data_ingestion" in resolved.as_posix()

    settings = get_settings()
    assert settings["api_port"] == int(os.getenv("PORT", os.getenv("API_PORT", "8000")))
