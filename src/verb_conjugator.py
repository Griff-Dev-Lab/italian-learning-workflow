"""Verb conjugator — generates conjugation data for an Italian verb via LLM."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .llm_client import LLMClient, LLMError

try:
    from mlconjug3 import Conjugator
    MLCONJUG_AVAILABLE = True
except ImportError:
    MLCONJUG_AVAILABLE = False


class ConjugatorError(Exception):
    """Raised when conjugation generation fails validation."""


@dataclass
class ConjugationData:
    """All conjugation forms needed to build flashcards for one verb."""
    infinitive: str

    # Present tense — all 6 forms
    present_io: str
    present_tu: str
    present_lui_lei: str
    present_noi: str
    present_voi: str
    present_loro: str

    # Past tense (passato prossimo) — most common forms
    past_io: str
    past_tu: str

    # Future tense (futuro semplice) — most common forms
    future_io: str
    future_tu: str

    # Example sentences for cloze cards — one per conjugated form
    # Each sentence must use the specific form and make it the only correct answer
    cloze_sentences: List[dict]  # [{"sentence": "...", "answer": "...", "label": "io, present"}, ...]


CONJUGATION_PROMPT = """You are an Italian language teacher. Generate conjugation data for the Italian verb: {infinitive}

Return a JSON object with this exact structure:

{{
  "infinitive": "{infinitive}",
  "present": {{
    "io": "...",
    "tu": "...",
    "lui_lei": "...",
    "noi": "...",
    "voi": "...",
    "loro": "..."
  }},
  "past": {{
    "io": "...",
    "tu": "..."
  }},
  "future": {{
    "io": "...",
    "tu": "..."
  }},
  "cloze_sentences": [
    {{
      "sentence": "Ogni mattina io {{{{c1::mangio}}}} un cornetto.",
      "answer": "mangio",
      "label": "io, present"
    }}
  ]
}}

Rules for cloze_sentences:
- Generate exactly 8 sentences
- Cover a spread of forms: at least 4 present tense (different persons), 2 past, 2 future
- Always include the subject pronoun explicitly in the sentence (io, tu, lui, lei, noi, voi, loro)
- The subject pronoun makes the blanked form the ONLY correct answer
- Wrap the answer in {{{{c1::answer}}}} — this is Anki cloze syntax
- Use simple A1-A2 level Italian — short sentences, everyday vocabulary
- Each sentence must be natural and make sense in context
- Do not repeat the same person/tense combination

Return JSON only. No markdown, no code fences, no extra text.
"""


class VerbConjugator:
    """Calls the LLM to generate all conjugation forms and cloze sentences for a verb."""

    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm
        self._mlconjug = None
        if MLCONJUG_AVAILABLE:
            try:
                self._mlconjug = Conjugator(language='it')
            except Exception:
                # If mlconjug fails to initialize, continue without verification
                pass

    def _verify_conjugation(self, infinitive: str, form: str, expected: str) -> bool:
        """Verify a conjugated form using mlconjug3. Returns True if correct or if verification unavailable."""
        if not self._mlconjug:
            return True  # Skip verification if mlconjug not available
        
        try:
            # Get the full conjugation from mlconjug
            conjugated = self._mlconjug.conjugate(infinitive)
            
            # Extract the specific form we're checking
            # This is a simplified check - mlconjug has complex nested structure
            conjugation_dict = conjugated.conjug_info
            
            # For basic verification, check if the expected form appears anywhere in the conjugation
            # This is not perfect but catches obvious errors
            all_forms = str(conjugation_dict).lower()
            return expected.lower() in all_forms
            
        except Exception:
            # If verification fails for any reason, assume the LLM is correct
            return True

    def conjugate(self, infinitive: str) -> ConjugationData:
        """Return full conjugation data for the given infinitive.

        Raises ConjugatorError if the LLM response is missing required fields.
        """
        prompt = CONJUGATION_PROMPT.format(infinitive=infinitive.lower().strip())

        for attempt in range(1, 3):
            data = self._llm.call(prompt)

            try:
                present = data["present"]
                past = data["past"]
                future = data["future"]
                cloze = data.get("cloze_sentences", [])

                if len(cloze) < 6:
                    if attempt == 1:
                        print(f"  [Conjugator] Got {len(cloze)} cloze sentences, expected 8. Retrying...")
                    continue

                conjugation_data = ConjugationData(
                    infinitive=data.get("infinitive", infinitive),
                    present_io=present["io"],
                    present_tu=present["tu"],
                    present_lui_lei=present["lui_lei"],
                    present_noi=present["noi"],
                    present_voi=present["voi"],
                    present_loro=present["loro"],
                    past_io=past["io"],
                    past_tu=past["tu"],
                    future_io=future["io"],
                    future_tu=future["tu"],
                    cloze_sentences=cloze,
                )

                # Optional verification with mlconjug3
                if self._mlconjug:
                    warnings = []
                    forms_to_check = [
                        ("present_io", conjugation_data.present_io),
                        ("present_tu", conjugation_data.present_tu),
                        ("present_lui_lei", conjugation_data.present_lui_lei),
                    ]
                    
                    for form_name, form_value in forms_to_check:
                        if not self._verify_conjugation(infinitive, form_name, form_value):
                            warnings.append(f"{form_name}: {form_value}")
                    
                    if warnings:
                        print(f"  [Conjugator] ⚠️  Verification warnings for: {', '.join(warnings)}")

                return conjugation_data

            except (KeyError, TypeError) as exc:
                if attempt == 1:
                    print(f"  [Conjugator] Missing fields in response: {exc}. Retrying...")
                continue

        raise ConjugatorError(
            f"Failed to generate conjugation data for '{infinitive}' after 2 attempts."
        )
