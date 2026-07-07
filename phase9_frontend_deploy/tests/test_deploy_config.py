from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_ROOT = REPO_ROOT / "phase7_frontend"
VERCEL_JSON = FRONTEND_ROOT / "vercel.json"
PACKAGE_JSON = FRONTEND_ROOT / "package.json"
VERIFY_SCRIPT = REPO_ROOT / "phase9_frontend_deploy" / "scripts" / "verify_env.mjs"
ENV_TS = FRONTEND_ROOT / "lib" / "env.ts"


def test_vercel_json_in_frontend_root():
    assert VERCEL_JSON.is_file(), "vercel.json must live in phase7_frontend for Vercel root directory deploys"

    config = json.loads(VERCEL_JSON.read_text(encoding="utf-8"))
    assert config["framework"] == "nextjs"
    assert config["buildCommand"] == "npm run build"


def test_node_version_and_prebuild_hook():
    package = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    assert package["engines"]["node"] == ">=20.0.0"
    assert "verify_env.mjs" in package["scripts"]["prebuild"]

    nvmrc = (FRONTEND_ROOT / ".nvmrc").read_text(encoding="utf-8").strip()
    assert nvmrc == "20"


def test_api_url_helper_strips_trailing_slash():
    text = ENV_TS.read_text(encoding="utf-8")
    assert "replace(/\\/+$/, \"\")" in text
    assert "NEXT_PUBLIC_API_URL" in text


def test_verify_env_script_exists():
    assert VERIFY_SCRIPT.is_file()
    text = VERIFY_SCRIPT.read_text(encoding="utf-8")
    assert "NEXT_PUBLIC_API_URL" in text
    assert "VERCEL" in text
