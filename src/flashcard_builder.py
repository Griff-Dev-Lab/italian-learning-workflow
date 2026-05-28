"""Flashcard builder — builds Basic and Cloze Anki CSVs from conjugation data."""

from __future__ import annotations

import csv
import io
import random
from dataclasses import dataclass
from typing import List

from .verb_conjugator import ConjugationData


class FlashcardError(Exception):
    """Raised when flashcard generation fails validation."""


@dataclass
class BasicCardRow:
    """One Basic note — front/back pair drilling a single conjugated form."""
    front: str   # e.g. "mangiare (io, Presente Indicativo)"
    back: str    # e.g. "mangio"


@dataclass
class ClozeCardRow:
    """One Cloze note — grid with {{c1::answer}} and an extra hint field."""
    text: str    # e.g. HTML table with one form hidden as {{c1::mangio}}
    extra: str   # e.g. "mangiare — Presente Indicativo"


BASIC_CSV_HEADER = ["front", "back"]
CLOZE_CSV_HEADER = ["text", "extra"]

# Persons in order for consistent randomization
PERSONS = ["io", "tu", "lui/lei", "noi", "voi", "loro"]


class FlashcardBuilder:
    """Builds Basic and Cloze card rows from ConjugationData and serialises to CSV."""

    def build_basic(self, data: ConjugationData) -> List[BasicCardRow]:
        """Return Basic card rows — one per conjugated form."""
        infinitive = data.infinitive
        rows: List[BasicCardRow] = [
            # Present tense — all 6 forms
            BasicCardRow(f"{infinitive} (io, Presente Indicativo)",      data.present_io),
            BasicCardRow(f"{infinitive} (tu, Presente Indicativo)",      data.present_tu),
            BasicCardRow(f"{infinitive} (lui/lei, Presente Indicativo)", data.present_lui_lei),
            BasicCardRow(f"{infinitive} (noi, Presente Indicativo)",     data.present_noi),
            BasicCardRow(f"{infinitive} (voi, Presente Indicativo)",     data.present_voi),
            BasicCardRow(f"{infinitive} (loro, Presente Indicativo)",    data.present_loro),
            # Past tense — all 6 forms
            BasicCardRow(f"{infinitive} (io, Passato Prossimo)",         data.past_io),
            BasicCardRow(f"{infinitive} (tu, Passato Prossimo)",         data.past_tu),
            BasicCardRow(f"{infinitive} (lui/lei, Passato Prossimo)",    data.past_lui_lei),
            BasicCardRow(f"{infinitive} (noi, Passato Prossimo)",        data.past_noi),
            BasicCardRow(f"{infinitive} (voi, Passato Prossimo)",        data.past_voi),
            BasicCardRow(f"{infinitive} (loro, Passato Prossimo)",       data.past_loro),
            # Future tense — all 6 forms
            BasicCardRow(f"{infinitive} (io, Futuro Semplice)",       data.future_io),
            BasicCardRow(f"{infinitive} (tu, Futuro Semplice)",       data.future_tu),
            BasicCardRow(f"{infinitive} (lui/lei, Futuro Semplice)",  data.future_lui_lei),
            BasicCardRow(f"{infinitive} (noi, Futuro Semplice)",      data.future_noi),
            BasicCardRow(f"{infinitive} (voi, Futuro Semplice)",      data.future_voi),
            BasicCardRow(f"{infinitive} (loro, Futuro Semplice)",     data.future_loro),
        ]
        return rows

    def build_cloze(self, data: ConjugationData) -> List[ClozeCardRow]:
        """Return 3 grid-based Cloze cards (one per tense) with randomized hidden forms.
        
        Ensures no two cards hide the same person across the 3 tenses.
        """
        infinitive = data.infinitive
        
        # Select 3 different persons to hide (one per tense)
        hidden_persons = random.sample(PERSONS, 3)
        
        # Build grid cards for each tense
        rows: List[ClozeCardRow] = [
            self._build_grid_cloze_card(
                infinitive,
                "Presente Indicativo",
                hidden_persons[0],
                [data.present_io, data.present_tu, data.present_lui_lei,
                 data.present_noi, data.present_voi, data.present_loro]
            ),
            self._build_grid_cloze_card(
                infinitive,
                "Passato Prossimo",
                hidden_persons[1],
                [data.past_io, data.past_tu, data.past_lui_lei,
                 data.past_noi, data.past_voi, data.past_loro]
            ),
            self._build_grid_cloze_card(
                infinitive,
                "Futuro Semplice",
                hidden_persons[2],
                [data.future_io, data.future_tu, data.future_lui_lei,
                 data.future_noi, data.future_voi, data.future_loro]
            ),
        ]
        
        return rows

    def _build_grid_cloze_card(
        self,
        infinitive: str,
        tense_name: str,
        hidden_person: str,
        forms: List[str]
    ) -> ClozeCardRow:
        """Build a single grid-based cloze card with one hidden form.
        
        Args:
            infinitive: Verb infinitive (e.g., "mangiare")
            tense_name: Italian tense name (e.g., "Presente Indicativo")
            hidden_person: Person to hide (e.g., "io")
            forms: List of 6 conjugated forms in order [io, tu, lui/lei, noi, voi, loro]
        
        Returns:
            ClozeCardRow with HTML table grid
        """
        # Build table rows
        table_rows = []
        for person, form in zip(PERSONS, forms):
            if person == hidden_person:
                # Hide this form with cloze syntax
                table_rows.append(f"| {person} | {{{{c1::{form}}}}} |")
            else:
                table_rows.append(f"| {person} | {form} |")
        
        # Build complete HTML table
        table_html = (
            f"<b>{infinitive} — {tense_name}</b><br/><br/>"
            f"<table style='border-collapse: collapse; width: 100%;'>"
            f"<tr style='border: 1px solid #ccc;'>"
            f"<th style='border: 1px solid #ccc; padding: 8px; text-align: left;'>Persona</th>"
            f"<th style='border: 1px solid #ccc; padding: 8px; text-align: left;'>Forma</th>"
            f"</tr>"
        )
        
        for person, form in zip(PERSONS, forms):
            if person == hidden_person:
                table_html += (
                    f"<tr style='border: 1px solid #ccc;'>"
                    f"<td style='border: 1px solid #ccc; padding: 8px;'>{person}</td>"
                    f"<td style='border: 1px solid #ccc; padding: 8px;'>{{{{c1::{form}}}}}</td>"
                    f"</tr>"
                )
            else:
                table_html += (
                    f"<tr style='border: 1px solid #ccc;'>"
                    f"<td style='border: 1px solid #ccc; padding: 8px;'>{person}</td>"
                    f"<td style='border: 1px solid #ccc; padding: 8px;'>{form}</td>"
                    f"</tr>"
                )
        
        table_html += "</table>"
        
        extra = f"{infinitive} — {tense_name}"
        
        return ClozeCardRow(text=table_html, extra=extra)

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
