from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class ErrorCode(str, Enum):
    VALIDATION_ERROR = "validation_error"
    NO_MATCHES = "no_matches"
    OPENAI_ERROR = "openai_error"
    SERVER_ERROR = "server_error"


class FieldError(BaseModel):
    field: str
    message: str


class ErrorDetails(BaseModel):
    errors: Optional[list[FieldError]] = None
    extra: Optional[dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Standard error payload for Phase 6 API and Phase 7 UI."""

    message: str = Field(..., min_length=1)
    code: ErrorCode
    details: Optional[ErrorDetails | dict[str, Any]] = None


def build_error_response(
    message: str,
    code: ErrorCode,
    *,
    field_errors: Optional[list[dict[str, str]]] = None,
    extra: Optional[dict[str, Any]] = None,
) -> ErrorResponse:
    details: Optional[ErrorDetails] = None
    if field_errors or extra:
        details = ErrorDetails(
            errors=[FieldError(**item) for item in field_errors] if field_errors else None,
            extra=extra,
        )
    return ErrorResponse(message=message, code=code, details=details)
