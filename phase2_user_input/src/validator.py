from __future__ import annotations

from typing import Any

from pydantic import ValidationError as PydanticValidationError

from .models import PreferenceInput, UserPreferences


class ValidationError(Exception):
    """Raised when user preference input fails validation."""

    def __init__(self, message: str, errors: list[dict[str, Any]] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.errors = errors or []


def _format_pydantic_errors(exc: PydanticValidationError) -> list[dict[str, Any]]:
    formatted: list[dict[str, Any]] = []
    for error in exc.errors():
        field = ".".join(str(part) for part in error.get("loc", ()))
        formatted.append(
            {
                "field": field or "input",
                "message": error.get("msg", "Invalid value"),
                "type": error.get("type", "value_error"),
            }
        )
    return formatted


def validate_preferences(data: dict[str, Any] | PreferenceInput) -> UserPreferences:
    """
    Validate and normalize user preferences.

    Raises ValidationError with clear field-level messages on failure.
    """
    try:
        payload = data if isinstance(data, PreferenceInput) else PreferenceInput.model_validate(data)
    except PydanticValidationError as exc:
        errors = _format_pydantic_errors(exc)
        raise ValidationError("Invalid user preferences.", errors=errors) from exc

    location = payload.location.strip()
    cuisine = payload.cuisine.strip()
    additional_notes = payload.additional_notes.strip() if payload.additional_notes else None

    if not location:
        raise ValidationError(
            "Invalid user preferences.",
            errors=[{"field": "location", "message": "Location is required.", "type": "missing"}],
        )

    if not cuisine:
        raise ValidationError(
            "Invalid user preferences.",
            errors=[{"field": "cuisine", "message": "Cuisine is required.", "type": "missing"}],
        )

    return UserPreferences(
        location=location,
        budget=payload.budget,
        cuisine=cuisine,
        min_rating=round(payload.min_rating, 1),
        additional_notes=additional_notes or None,
    )
