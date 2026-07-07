from __future__ import annotations

from openai import OpenAI

from . import phase_imports as _phase_imports  # noqa: F401
from .phase_imports import LLMPrompt, get_openai_api_key, get_openai_model
from .response_parser import ResponseParser, ResponseParserError


class OpenAIClientError(RuntimeError):
    """Raised when the OpenAI API call fails."""


class OpenAIRecommendationClient:
    """Call OpenAI Chat Completions API with Phase 3 prompts."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        timeout_seconds: float = 60.0,
    ) -> None:
        self.api_key = api_key or get_openai_api_key()
        self.model = model or get_openai_model()
        self.timeout_seconds = timeout_seconds
        self.parser = ResponseParser()

        if not self.api_key:
            raise OpenAIClientError("OPENAI_API_KEY is not set.")

        self._client = OpenAI(api_key=self.api_key, timeout=self.timeout_seconds)

    def complete(self, prompt: LLMPrompt) -> str:
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt.system_prompt},
                    {"role": "user", "content": prompt.user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
            )
        except Exception as exc:
            raise OpenAIClientError(f"OpenAI API request failed: {exc}") from exc

        content = response.choices[0].message.content
        if not content:
            raise OpenAIClientError("OpenAI returned no message content.")
        return content

    def recommend(self, prompt: LLMPrompt):
        from .models import RecommendationResponse

        content = self.complete(prompt)
        try:
            return self.parser.parse(content)
        except ResponseParserError as exc:
            raise OpenAIClientError(str(exc)) from exc
