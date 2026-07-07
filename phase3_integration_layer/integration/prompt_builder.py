from __future__ import annotations

import json

from integration.phase_imports import UserPreferences

from .models import CandidateRestaurant, LLMPrompt
from .token_utils import estimate_tokens

SYSTEM_PROMPT = """You are a restaurant recommendation assistant for an Indian dining app.
Your job is to rank restaurants from a provided candidate list based on user preferences.
Only recommend restaurants present in the candidate list.
Respond with valid JSON only, matching the requested schema exactly."""

OUTPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "required": ["summary", "recommendations"],
    "properties": {
        "summary": {
            "type": "string",
            "description": "Brief overview of the top choices and trade-offs.",
        },
        "recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "rank",
                    "restaurant_id",
                    "name",
                    "cuisine",
                    "rating",
                    "estimated_cost",
                    "explanation",
                ],
                "properties": {
                    "rank": {"type": "integer"},
                    "restaurant_id": {"type": "string"},
                    "name": {"type": "string"},
                    "cuisine": {"type": "string"},
                    "rating": {"type": "number"},
                    "estimated_cost": {"type": ["number", "string"]},
                    "explanation": {"type": "string"},
                },
            },
        },
    },
}


class PromptBuilder:
    """Assemble system and user prompts with preferences and candidate context."""

    def build(
        self,
        preferences: UserPreferences,
        candidates: list[CandidateRestaurant],
        relaxed_filters: list[str],
    ) -> LLMPrompt:
        candidate_payload = [candidate.model_dump(exclude_none=True) for candidate in candidates]
        notes = preferences.additional_notes or "None"

        relaxation_note = ""
        if relaxed_filters and relaxed_filters != ["all"]:
            relaxation_note = (
                f"\nNote: Strict filters were relaxed for: {', '.join(relaxed_filters)}. "
                "Mention any trade-offs in your explanations."
            )

        user_prompt = f"""User preferences:
- Location: {preferences.location}
- Budget tier: {preferences.budget.value}
- Cuisine: {preferences.cuisine}
- Minimum rating: {preferences.min_rating}
- Additional notes: {notes}{relaxation_note}

Candidate restaurants (JSON):
{json.dumps(candidate_payload, indent=2)}

Task:
1. Rank the best 3 to 5 restaurants for this user.
2. Explain why each recommendation fits the preferences and notes.
3. Provide a short summary comparing the top options.

Return JSON with this schema:
{json.dumps(OUTPUT_SCHEMA, indent=2)}"""

        estimated_tokens = estimate_tokens(SYSTEM_PROMPT) + estimate_tokens(user_prompt)
        return LLMPrompt(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            estimated_tokens=estimated_tokens,
            output_schema=OUTPUT_SCHEMA,
        )
