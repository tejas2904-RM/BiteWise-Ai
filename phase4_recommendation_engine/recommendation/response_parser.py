from __future__ import annotations

import json
import re
from typing import Any

from pydantic import ValidationError

from .models import RecommendationResponse

_JSON_BLOCK_PATTERN = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL | re.IGNORECASE)


class ResponseParserError(ValueError):
    """Raised when OpenAI output cannot be parsed into recommendations."""


class ResponseParser:
    """Extract and validate ranked recommendations from OpenAI JSON output."""

    def extract_json_text(self, content: str) -> str:
        text = content.strip()
        if not text:
            raise ResponseParserError("OpenAI returned an empty response.")

        block_match = _JSON_BLOCK_PATTERN.search(text)
        if block_match:
            return block_match.group(1).strip()

        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return text[start : end + 1]

        raise ResponseParserError("No JSON object found in OpenAI response.")

    def parse(self, content: str) -> RecommendationResponse:
        json_text = self.extract_json_text(content)
        try:
            payload: dict[str, Any] = json.loads(json_text)
        except json.JSONDecodeError as exc:
            raise ResponseParserError(f"Invalid JSON from OpenAI: {exc}") from exc

        try:
            return RecommendationResponse.model_validate(payload)
        except ValidationError as exc:
            raise ResponseParserError(f"OpenAI JSON does not match schema: {exc}") from exc
