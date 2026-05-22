"""Flashcard builder — generates Anki-compatible CSV from vocabulary."""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from typing import List

from .llm_client import LLMClient, LLMError


class FlashcardError(Exception):
    """Raised when flashcard generation fails validation."""


@dataclass
class FlashcardRow:
    italian_form: str        # e.g. "mangio" or "pane"
    english_translation: str # e.g. "I eat" or "bread"
    source_word: str         # infinitive or base form
    word_type: str           # "verb" | "noun" | "adjective"
    tense_label: str         # "present" | "past" | "future" | "base"
    italian_example: str     # ≤12 words
    english_example: str     # translation of italian_example


CSV_HEADER = [
    "italian_form",
    "english_translation",
    "source_word",
    "word_type",
    "tense_label",
    "italian_example",
    "english_example",
]

FLASHCARD_PROMPT = """You are an Italian language teacher creating A1-level flashcard data.

Theme: {theme_label}
Theme description: {theme_description}

Vocabulary to use:
- Verbs: {verbs}
- Nouns: {nouns}
- Adjectives: {adjectives}

Generate exactly 10 flashcard objects in a JSON array under the key "cards".

Rules:
- For each VERB: create 3 cards — one for present tense (io form), one for past tense (passato prossimo, io form), one for future tense (futuro semplice, io form)
- For each NOUN: create 1 card with the base form (include the article, e.g. "il pane")
- For each ADJECTIVE: create 1 card with the base form (masculine singular)
- Total: 2 verbs × 3 = 6 verb cards + 2 noun cards + 2 adjective cards = 10 cards
- All example sentences must be 12 words or fewer
- Use only A1-level vocabulary — simple, everyday words
- Do NOT use grammar terms like subjunctive, gerund, declension
- Tense labels must be exactly: "present", "past", "future", or "base"
- Word type must be exactly: "verb", "noun", or "adjective"

Return JSON only. Example structure:
{{
  "cards": [
    {{
      "italian_form": "mangio",
      "english_translation": "I eat",
      "source_word": "mangiare",
      "word_type": "verb",
      "tense_label": "present",
      "italian_example": "Io mangio la pizza ogni giorno.",
      "english_example": "I eat pizza every day."
    }}
  ]
}}"""


class FlashcardBuilder:
    """Generates flashcard data and writes RFC 4180-compliant UTF-8 CSV."""

    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    def build(self, theme, vocab: dict) -> List[FlashcardRow]:
        """Call LLM to generate flashcard rows. Retries once if row count is wrong."""
        prompt = FLASHCARD_PROMPT.format(
            theme_label=theme.label,
            theme_description=theme.description,
            verbs=", ".join(vocab.get("verbs", [])),
            nouns=", ".join(vocab.get("nouns", [])),
            adjectives=", ".join(vocab.get("adjectives", [])),
        )

        for attempt in range(1, 3):  # max 2 attempts
            data = self._llm.call(prompt)
            cards_raw = data.get("cards", [])
            if len(cards_raw) == 10:
                return [self._parse_row(r) for r in cards_raw]
            if attempt == 1:
                print(f"  [Flashcard] Got {len(cards_raw)} cards, expected 10. Retrying...")

        raise FlashcardError(
            f"Flashcard generation returned {len(cards_raw)} rows after 2 attempts. Expected 10."
        )

    def _parse_row(self, raw: dict) -> FlashcardRow:
        return FlashcardRow(
            italian_form=str(raw.get("italian_form", "")),
            english_translation=str(raw.get("english_translation", "")),
            source_word=str(raw.get("source_word", "")),
            word_type=str(raw.get("word_type", "")),
            tense_label=str(raw.get("tense_label", "")),
            italian_example=str(raw.get("italian_example", "")),
            english_example=str(raw.get("english_example", "")),
        )

    def to_csv(self, rows: List[FlashcardRow]) -> str:
        """Return RFC 4180-compliant UTF-8 CSV string with header row."""
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        writer.writerow(CSV_HEADER)
        for row in rows:
            writer.writerow([
                row.italian_form,
                row.english_translation,
                row.source_word,
                row.word_type,
                row.tense_label,
                row.italian_example,
                row.english_example,
            ])
        return output.getvalue()
