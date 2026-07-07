from __future__ import annotations

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from contract.errors import ErrorCode, build_error_response
from backend.phase_bridge import ValidationError as PreferenceValidationError
from backend.services.recommendation_service import NoMatchesError
from backend.services.restaurant_service import RestaurantNotFoundError


def register_exception_handlers(app) -> None:
    @app.exception_handler(PreferenceValidationError)
    async def preference_validation_handler(_: Request, exc: PreferenceValidationError) -> JSONResponse:
        field_errors = [
            {"field": item.get("field", "input"), "message": item.get("message", "Invalid value")}
            for item in exc.errors
        ]
        body = build_error_response(
            exc.message,
            ErrorCode.VALIDATION_ERROR,
            field_errors=field_errors,
        )
        return JSONResponse(status_code=422, content=body.model_dump())

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        field_errors = []
        for error in exc.errors():
            field = ".".join(str(part) for part in error.get("loc", ()))
            if field.startswith("body."):
                field = field.removeprefix("body.")
            field_errors.append(
                {"field": field or "body", "message": error.get("msg", "Invalid value")}
            )
        body = build_error_response(
            "Invalid request body.",
            ErrorCode.VALIDATION_ERROR,
            field_errors=field_errors,
        )
        return JSONResponse(status_code=422, content=body.model_dump())

    @app.exception_handler(NoMatchesError)
    async def no_matches_handler(_: Request, exc: NoMatchesError) -> JSONResponse:
        body = build_error_response(str(exc), ErrorCode.NO_MATCHES)
        return JSONResponse(status_code=404, content=body.model_dump())

    @app.exception_handler(RestaurantNotFoundError)
    async def restaurant_not_found_handler(_: Request, exc: RestaurantNotFoundError) -> JSONResponse:
        body = build_error_response(str(exc), ErrorCode.NO_MATCHES)
        return JSONResponse(status_code=404, content=body.model_dump())

    @app.exception_handler(ValidationError)
    async def pydantic_validation_handler(_: Request, exc: ValidationError) -> JSONResponse:
        body = build_error_response("Invalid data.", ErrorCode.VALIDATION_ERROR)
        return JSONResponse(status_code=422, content=body.model_dump())

    @app.exception_handler(Exception)
    async def server_error_handler(_: Request, exc: Exception) -> JSONResponse:
        body = build_error_response("Internal server error.", ErrorCode.SERVER_ERROR)
        return JSONResponse(status_code=500, content=body.model_dump())

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        if isinstance(exc.detail, dict) and "code" in exc.detail:
            return JSONResponse(status_code=exc.status_code, content=exc.detail)
        body = build_error_response(str(exc.detail), ErrorCode.SERVER_ERROR)
        return JSONResponse(status_code=exc.status_code, content=body.model_dump())
