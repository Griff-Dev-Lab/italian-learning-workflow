"""LLM client — thin wrapper around the OpenAI SDK with retry logic."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import yaml
from openai import OpenAI, APIError, APIConnectionError, RateLimitError


class LLMError(Exception):
    """Raised when the LLM call fails after all retries."""


def _load_config() -> dict:
    config_path = Path(__file__).parent.parent / "config.yaml"
    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


class LLMClient:
    """Wraps the OpenAI SDK, loads config from config.yaml and API key from env."""

    def __init__(self) -> None:
        config = _load_config()
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise LLMError(
                "OPENAI_API_KEY environment variable is not set. "
                "Copy .env.example to .env and add your API key."
            )
        self._model: str = config.get("openai_model", "gpt-4o-mini")
        base_url: str = config.get("openai_base_url", "https://api.openai.com/v1")
        self._max_retries: int = int(config.get("max_retries", 3))
        self._client = OpenAI(api_key=api_key, base_url=base_url)

    def call_text(self, prompt: str) -> str:
        """Send a prompt and return the raw text response (no JSON parsing).

        Used for passage generation where plain text output is more reliable.
        """
        last_error: Exception | None = None
        for attempt in range(1, self._max_retries + 1):
            try:
                response = self._client.chat.completions.create(
                    model=self._model,
                    messages=[
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                )
                return response.choices[0].message.content or ""
            except (APIConnectionError, RateLimitError) as exc:
                last_error = exc
                wait = 2 ** attempt
                print(f"  [LLM] Transient error on attempt {attempt}/{self._max_retries}: {exc}. Retrying in {wait}s...")
                time.sleep(wait)
            except APIError as exc:
                last_error = exc
                if attempt < self._max_retries:
                    wait = 2 ** attempt
                    print(f"  [LLM] API error on attempt {attempt}/{self._max_retries}: {exc}. Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    break

        raise LLMError(
            f"LLM call failed after {self._max_retries} attempts. Last error: {last_error}"
        )

    def call(self, prompt: str) -> dict:
        """Send a prompt to the LLM and return the parsed JSON response.

        Retries up to max_retries times on transient errors with exponential backoff.
        Raises LLMError after all retries are exhausted.
        """
        last_error: Exception | None = None
        for attempt in range(1, self._max_retries + 1):
            try:
                response = self._client.chat.completions.create(
                    model=self._model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful Italian language teacher. "
                                "Always respond with valid JSON only — no markdown, "
                                "no code fences, no extra text."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.7,
                )
                content = response.choices[0].message.content
                return json.loads(content)
            except (APIConnectionError, RateLimitError) as exc:
                last_error = exc
                wait = 2 ** attempt
                print(f"  [LLM] Transient error on attempt {attempt}/{self._max_retries}: {exc}. Retrying in {wait}s...")
                time.sleep(wait)
            except APIError as exc:
                last_error = exc
                if attempt < self._max_retries:
                    wait = 2 ** attempt
                    print(f"  [LLM] API error on attempt {attempt}/{self._max_retries}: {exc}. Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    break
            except json.JSONDecodeError as exc:
                last_error = exc
                if attempt < self._max_retries:
                    print(f"  [LLM] JSON parse error on attempt {attempt}/{self._max_retries}. Retrying...")
                else:
                    break

        raise LLMError(
            f"LLM call failed after {self._max_retries} attempts. Last error: {last_error}"
        )
