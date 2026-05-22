"""Passage builder — generates Italian reading passage and English translation."""

from __future__ import annotations

from .llm_client import LLMClient


class PassageError(Exception):
    """Raised when passage generation fails after max retries."""


PASSAGE_PROMPT_IT = """Write a reading passage in Italian for a beginner language learner (A1 level).

Theme: {theme_label} — {theme_description}

Rules:
- Write between 100 and 200 words in Italian
- Use simple, everyday vocabulary and short sentences
- Use each of these words at least once (conjugated or inflected forms are fine): {all_vocab}
- Describe a scene or a small story related to the theme
- Write ONLY the Italian passage, nothing else — no translation, no title, no labels

Italian passage:"""

PASSAGE_PROMPT_EN = """Translate this Italian passage into English. Write only the English translation, nothing else.

Italian:
{italian_text}

English translation:"""


class PassageBuilder:
    """Generates a 100-200 word Italian passage with English translation."""

    MAX_ATTEMPTS = 3

    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    def build(self, theme, vocab: dict) -> tuple[str, str]:
        """Return (italian_text, english_text). Retries up to 3 times if word count is out of range."""
        all_vocab = ", ".join(
            vocab.get("verbs", []) + vocab.get("nouns", []) + vocab.get("adjectives", [])
        )

        last_count = 0
        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            # Step 1: generate Italian passage as plain text
            it_prompt = PASSAGE_PROMPT_IT.format(
                theme_label=theme.label,
                theme_description=theme.description,
                all_vocab=all_vocab,
            )
            italian = self._llm.call_text(it_prompt).strip()
            word_count = len(italian.split())
            last_count = word_count

            if word_count < 100:
                print(
                    f"  [Passage] Attempt {attempt}/{self.MAX_ATTEMPTS}: "
                    f"word count {word_count} is too short (need 100+). Retrying..."
                )
                continue

            # Step 2: generate English translation as plain text
            en_prompt = PASSAGE_PROMPT_EN.format(italian_text=italian)
            english = self._llm.call_text(en_prompt).strip()

            print(f"      Passage word count: {word_count}")
            return italian, english

        raise PassageError(
            f"Passage generation failed after {self.MAX_ATTEMPTS} attempts. "
            f"Last word count: {last_count}. Please try again."
        )
