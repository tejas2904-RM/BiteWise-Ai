from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import ValidationError as PydanticValidationError

from .models import PreferenceInput, UserPreferences
from .validator import ValidationError, validate_preferences

app = FastAPI(
    title="Restaurant Recommendation API",
    description="Phase 2: User preference input and validation",
    version="1.0.0",
)

_FORM_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Restaurant Preferences</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 520px; margin: 2rem auto; padding: 0 1rem; }
    h1 { font-size: 1.5rem; }
    label { display: block; margin-top: 1rem; font-weight: 600; }
    input, select, textarea { width: 100%; margin-top: 0.35rem; padding: 0.5rem; box-sizing: border-box; }
    button { margin-top: 1.25rem; padding: 0.6rem 1rem; cursor: pointer; }
    .error { color: #b00020; margin-top: 1rem; }
  </style>
</head>
<body>
  <h1>Restaurant Preferences</h1>
  <p>Tell us what you're looking for and we'll find matching restaurants.</p>
  <form method="post" action="/preferences/form">
    <label for="location">Location</label>
    <input id="location" name="location" placeholder="Bangalore" required />

    <label for="cuisine">Cuisine</label>
    <input id="cuisine" name="cuisine" placeholder="Chinese" required />

    <label for="budget">Budget</label>
    <select id="budget" name="budget" required>
      <option value="">Select budget</option>
      <option value="low">Low</option>
      <option value="medium">Medium</option>
      <option value="high">High</option>
    </select>

    <label for="min_rating">Minimum rating</label>
    <input id="min_rating" name="min_rating" type="number" min="0" max="5" step="0.1" value="4.0" required />

    <label for="additional_notes">Additional notes (optional)</label>
    <textarea id="additional_notes" name="additional_notes" rows="3" placeholder="family-friendly, quick service"></textarea>

    <button type="submit">Submit preferences</button>
  </form>
</body>
</html>
"""


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def preference_form() -> str:
    return _FORM_HTML


@app.get("/api/schema")
def preference_schema() -> dict[str, Any]:
    return PreferenceInput.model_json_schema()


@app.post("/api/preferences", response_model=UserPreferences)
def submit_preferences_json(payload: PreferenceInput) -> UserPreferences:
    try:
        return validate_preferences(payload)
    except ValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail={"message": exc.message, "errors": exc.errors},
        ) from exc


@app.post("/preferences/form", response_class=HTMLResponse)
def submit_preferences_form(
    location: str = Form(...),
    cuisine: str = Form(...),
    budget: str = Form(...),
    min_rating: float = Form(...),
    additional_notes: str = Form(default=""),
) -> HTMLResponse:
    payload = {
        "location": location,
        "cuisine": cuisine,
        "budget": budget,
        "min_rating": min_rating,
        "additional_notes": additional_notes or None,
    }

    try:
        preferences = validate_preferences(payload)
    except ValidationError as exc:
        error_lines = "".join(f"<li>{e['field']}: {e['message']}</li>" for e in exc.errors)
        return HTMLResponse(
            content=_FORM_HTML + f'<div class="error"><p>{exc.message}</p><ul>{error_lines}</ul></div>',
            status_code=422,
        )

    result = preferences.model_dump_json(indent=2)
    return HTMLResponse(
        content=f"""
        <html><body style="font-family: system-ui, sans-serif; max-width: 640px; margin: 2rem auto;">
          <h1>Preferences saved</h1>
          <pre>{result}</pre>
          <p><a href="/">Submit another</a></p>
        </body></html>
        """
    )


@app.exception_handler(PydanticValidationError)
async def pydantic_validation_handler(_: Request, exc: PydanticValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"message": "Invalid request.", "errors": exc.errors()})
