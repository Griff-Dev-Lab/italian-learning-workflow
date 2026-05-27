"""Flashcard builder — builds Basic and Cloze Anki CSVs from conjugation data."""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from typing import List

from .verb_conjugator import ConjugationData


class FlashcardError(Exception):
    """Raised when flashcard generation fails validation."""


@dataclass
class BasicCardRow:
    """One Basic note — front/back pair drilling a single conjugated form."""
    front: str   # e.g. "mangiare (io, present)"
    back: str    # e.g. "mangio"


@dataclass
class ClozeCardRow:
    """One Cloze note — sentence with {{c1::answer}} and an extra hint field."""
    text: str    # e.g. "Ogni mattina io {{c1::mangio}} un cornetto."
    extra: str   # e.g. "mangiare — io, present"


BASIC_CSV_HEADER = ["front", "back"]
CLOZE_CSV_HEADER = ["text", "extra"]


class FlashcardBuilder:
    """Builds Basic and Cloze card rows from ConjugationData and serialises to CSV."""

    def build_basic(self, data: ConjugationData) -> List[BasicCardRow]:
        """Return Basic card rows — one per conjugated form."""
        infinitive = data.infinitive
        rows: List[BasicCardRow] = [
            # Present tense — all 6 forms
            BasicCardRow(f"{infinitive} (io, present)",      data.present_io),
            BasicCardRow(f"{infinitive} (tu, present)",      data.present_tu),
            BasicCardRow(f"{infinitive} (lui/lei, present)", data.present_lui_lei),
            BasicCardRow(f"{infinitive} (noi, present)",     data.present_noi),
            BasicCardRow(f"{infinitive} (voi, present)",     data.present_voi),
            BasicCardRow(f"{infinitive} (loro, present)",    data.present_loro),
            # Past tense — all 6 forms
            BasicCardRow(f"{infinitive} (io, past)",         data.past_io),
            BasicCardRow(f"{infinitive} (tu, past)",         data.past_tu),
            BasicCardRow(f"{infinitive} (lui/lei, past)",    data.past_lui_lei),
            BasicCardRow(f"{infinitive} (noi, past)",        data.past_noi),
            BasicCardRow(f"{infinitive} (voi, past)",        data.past_voi),
            BasicCardRow(f"{infinitive} (loro, past)",       data.past_loro),
            # Future tense — all 6 forms
            BasicCardRow(f"{infinitive} (io, future)",       data.future_io),
            BasicCardRow(f"{infinitive} (tu, future)",       data.future_tu),
            BasicCardRow(f"{infinitive} (lui/lei, future)",  data.future_lui_lei),
            BasicCardRow(f"{infinitive} (noi, future)",      data.future_noi),
            BasicCardRow(f"{infinitive} (voi, future)",      data.future_voi),
            BasicCardRow(f"{infinitive} (loro, future)",     data.future_loro),
        ]
        return rows

    def build_cloze(self, data: ConjugationData) -> List[ClozeCardRow]:
        """Return Cloze card rows from the LLM-generated sentences."""
        rows: List[ClozeCardRow] = []
        for item in data.cloze_sentences:
            sentence = str(item.get("sentence", "")).strip()
            label = str(item.get("label", "")).strip()
            if not sentence:
                continue
            extra = f"{data.infinitive} — {label}" if label else data.infinitive
            rows.append(ClozeCardRow(text=sentence, extra=extra))

        if not rows:
            raise FlashcardError(
                f"No cloze sentences were generated for '{data.infinitive}'."
            )
        return rows

    def to_basic_csv(self, rows: List[BasicCardRow]) -> str:
        """Return RFC 4180-compliant UTF-8 CSV for Basic note type (no header row)."""
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        for row in rows:
            writer.writerow([row.front, row.back])
        return output.getvalue()

    def to_cloze_csv(self, rows: List[ClozeCardRow]) -> str:
        """Return RFC 4180-compliant UTF-8 CSV for Cloze note type (no header row)."""
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        for row in rows:
            writer.writerow([row.text, row.extra])
        return output.getvalue()
