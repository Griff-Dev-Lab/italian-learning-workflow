"""Verb conjugator — generates conjugation data for an Italian verb via mlconjug3."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

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

Generate ONLY simple tense forms — do not use reflexive verbs, compound tenses, or past participles.

For PRESENT tense, use simple present indicative forms:
- dormire → dormo, dormi, dorme, dormiamo, dormite, dormono
- mangiare → mangio, mangi, mangia, mangiamo, mangiate, mangiano
- leggere → leggo, leggi, legge, leggiamo, leggete, leggono

For PAST tense, use passato prossimo (compound past):
- dormire → ho dormito, hai dormito (with avere auxiliary)
- andare → sono andato, sei andato (with essere auxiliary)

For FUTURE tense, use futuro semplice (simple future):
- dormire → dormirò, dormirai
- mangiare → mangerò, mangerai

CRITICAL: Do NOT generate reflexive forms (addormentarsi), compound forms (sono addormentato), or wrong auxiliaries.

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
      "sentence": "Ogni mattina io {{{{c1::dormo}}}} otto ore.",
      "answer": "dormo",
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
    """Generates all conjugation forms and cloze sentences for a verb using mlconjug3."""

    def __init__(self) -> None:
        self._mlconjug = None
        if not MLCONJUG_AVAILABLE:
            raise ConjugatorError(
                "mlconjug3 library is required but not installed. "
                "Install it with: pip install mlconjug3"
            )
        
        try:
            self._mlconjug = Conjugator(language='it')
        except Exception as exc:
            raise ConjugatorError(f"Failed to initialize mlconjug3: {exc}")

    def conjugate(self, infinitive: str) -> ConjugationData:
        """Return full conjugation data for the given infinitive using mlconjug3.

        Raises ConjugatorError if conjugation fails.
        """
        try:
            # Get conjugations from mlconjug3
            conjugated = self._mlconjug.conjugate(infinitive)
            conjugation_dict = conjugated.conjug_info
            
            # Extract present tense forms
            present_forms = self._extract_present_forms(conjugation_dict, infinitive)
            past_forms = self._extract_past_forms(conjugation_dict, infinitive)
            future_forms = self._extract_future_forms(conjugation_dict, infinitive)
            
            # Generate cloze sentences using templates
            cloze_sentences = self._generate_cloze_sentences(infinitive, present_forms, past_forms, future_forms)
            
            return ConjugationData(
                infinitive=infinitive,
                present_io=present_forms["io"],
                present_tu=present_forms["tu"],
                present_lui_lei=present_forms["lui_lei"],
                present_noi=present_forms["noi"],
                present_voi=present_forms["voi"],
                present_loro=present_forms["loro"],
                past_io=past_forms["io"],
                past_tu=past_forms["tu"],
                future_io=future_forms["io"],
                future_tu=future_forms["tu"],
                cloze_sentences=cloze_sentences,
            )
            
        except Exception as exc:
            raise ConjugatorError(f"Failed to conjugate '{infinitive}': {exc}")

    def _extract_present_forms(self, conjugation_dict: dict, infinitive: str) -> dict:
        """Extract present tense forms from mlconjug3 output."""
        try:
            # Navigate mlconjug3's nested structure to find present indicative
            present_indicative = conjugation_dict.get('Indicativo', {}).get('Indicativo presente', {})
            
            return {
                "io": present_indicative.get('1s', ''),
                "tu": present_indicative.get('2s', ''),
                "lui_lei": present_indicative.get('3s', ''),
                "noi": present_indicative.get('1p', ''),
                "voi": present_indicative.get('2p', ''),
                "loro": present_indicative.get('3p', ''),
            }
        except Exception:
            # If extraction fails, use known patterns for common verbs
            return self._fallback_present_forms(infinitive)

    def _extract_past_forms(self, conjugation_dict: dict, infinitive: str) -> dict:
        """Extract past tense forms from mlconjug3 output."""
        try:
            # Get the past participle from passato prossimo
            past_participle_forms = conjugation_dict.get('Indicativo', {}).get('Indicativo passato prossimo', {})
            past_participle = past_participle_forms.get('1s', '')  # All persons have same participle
            
            if past_participle:
                # Most verbs use 'avere' as auxiliary
                # Special cases that use 'essere' would need a lookup table
                auxiliary = self._get_auxiliary_verb(infinitive)
                
                # For essere verbs, past participle agrees with subject
                if auxiliary[0] == "sono":  # essere auxiliary
                    # Use masculine singular forms for simplicity (andato, not andata)
                    return {
                        "io": f"{auxiliary[0]} {past_participle}",
                        "tu": f"{auxiliary[1]} {past_participle}",
                    }
                else:  # avere auxiliary
                    return {
                        "io": f"{auxiliary[0]} {past_participle}",
                        "tu": f"{auxiliary[1]} {past_participle}",
                    }
            else:
                return self._fallback_past_forms(infinitive)
        except Exception:
            return self._fallback_past_forms(infinitive)

    def _extract_future_forms(self, conjugation_dict: dict, infinitive: str) -> dict:
        """Extract future tense forms from mlconjug3 output."""
        try:
            future_forms = conjugation_dict.get('Indicativo', {}).get('Indicativo futuro semplice', {})
            
            return {
                "io": future_forms.get('1s', ''),
                "tu": future_forms.get('2s', ''),
            }
        except Exception:
            return self._fallback_future_forms(infinitive)

    def _get_auxiliary_verb(self, infinitive: str) -> tuple:
        """Return the auxiliary verb forms (io, tu) for passato prossimo.
        
        Most verbs use 'avere', but some movement/state verbs use 'essere'.
        """
        # Verbs that typically use 'essere' as auxiliary
        essere_verbs = {
            'andare', 'venire', 'arrivare', 'partire', 'uscire', 'entrare',
            'nascere', 'morire', 'diventare', 'rimanere', 'restare', 'stare',
            'essere', 'divenire', 'cadere', 'scendere', 'salire', 'tornare'
        }
        
        if infinitive in essere_verbs:
            return ("sono", "sei")
        else:
            # Default to 'avere' for most verbs including dormire, mangiare, etc.
            return ("ho", "hai")

    def _fallback_present_forms(self, infinitive: str) -> dict:
        """Fallback present forms for common verbs when mlconjug3 extraction fails."""
        # Basic patterns for common verb endings
        if infinitive == "dormire":
            return {
                "io": "dormo", "tu": "dormi", "lui_lei": "dorme",
                "noi": "dormiamo", "voi": "dormite", "loro": "dormono"
            }
        elif infinitive == "mangiare":
            return {
                "io": "mangio", "tu": "mangi", "lui_lei": "mangia",
                "noi": "mangiamo", "voi": "mangiate", "loro": "mangiano"
            }
        else:
            # Generic -are, -ere, -ire patterns - this is approximate
            if infinitive.endswith("are"):
                root = infinitive[:-3]
                return {
                    "io": f"{root}o", "tu": f"{root}i", "lui_lei": f"{root}a",
                    "noi": f"{root}iamo", "voi": f"{root}ate", "loro": f"{root}ano"
                }
            elif infinitive.endswith("ere"):
                root = infinitive[:-3]
                return {
                    "io": f"{root}o", "tu": f"{root}i", "lui_lei": f"{root}e",
                    "noi": f"{root}iamo", "voi": f"{root}ete", "loro": f"{root}ono"
                }
            elif infinitive.endswith("ire"):
                root = infinitive[:-3]
                return {
                    "io": f"{root}o", "tu": f"{root}i", "lui_lei": f"{root}e",
                    "noi": f"{root}iamo", "voi": f"{root}ite", "loro": f"{root}ono"
                }
            else:
                # Unknown pattern - return empty, will trigger LLM fallback
                return {"io": "", "tu": "", "lui_lei": "", "noi": "", "voi": "", "loro": ""}

    def _fallback_past_forms(self, infinitive: str) -> dict:
        """Fallback past forms using standard patterns."""
        auxiliary = self._get_auxiliary_verb(infinitive)
        
        if infinitive == "dormire":
            return {"io": "ho dormito", "tu": "hai dormito"}
        elif infinitive == "mangiare":
            return {"io": "ho mangiato", "tu": "hai mangiato"}
        elif infinitive == "andare":
            return {"io": "sono andato", "tu": "sei andato"}
        else:
            # Generate past participle based on verb ending
            if infinitive.endswith("are"):
                past_participle = infinitive[:-3] + "ato"
            elif infinitive.endswith("ere"):
                past_participle = infinitive[:-3] + "uto"
            elif infinitive.endswith("ire"):
                past_participle = infinitive[:-3] + "ito"
            else:
                past_participle = infinitive + "to"  # fallback
            
            return {
                "io": f"{auxiliary[0]} {past_participle}",
                "tu": f"{auxiliary[1]} {past_participle}"
            }

    def _fallback_future_forms(self, infinitive: str) -> dict:
        """Fallback future forms using standard patterns."""
        if infinitive == "dormire":
            return {"io": "dormirò", "tu": "dormirai"}
        elif infinitive == "mangiare":
            return {"io": "mangerò", "tu": "mangerai"}
        else:
            # Standard future formation
            if infinitive.endswith("are"):
                future_root = infinitive[:-3] + "er"
            else:
                future_root = infinitive[:-1]  # remove final 'e'
            
            return {
                "io": f"{future_root}ò",
                "tu": f"{future_root}ai"
            }

    def _generate_cloze_sentences(self, infinitive: str, present: dict, past: dict, future: dict) -> list:
        """Generate cloze sentences using deterministic templates for maximum accuracy."""
        
        # Template patterns for different verb types and contexts
        templates = [
            # Present tense templates (4 sentences)
            {
                "template": f"({infinitive}) Ogni giorno io {{verb}}.",
                "person": "io", "tense": "present",
                "label": "io, present"
            },
            {
                "template": f"({infinitive}) Tu {{verb}} spesso?",
                "person": "tu", "tense": "present", 
                "label": "tu, present"
            },
            {
                "template": f"({infinitive}) Lui {{verb}} sempre.",
                "person": "lui_lei", "tense": "present",
                "label": "lui/lei, present"
            },
            {
                "template": f"({infinitive}) Noi {{verb}} insieme.",
                "person": "noi", "tense": "present",
                "label": "noi, present"
            },
            
            # Past tense templates (2 sentences)
            {
                "template": f"({infinitive}) Ieri io {{verb}}.",
                "person": "io", "tense": "past",
                "label": "io, past"
            },
            {
                "template": f"({infinitive}) Tu {{verb}} ieri?",
                "person": "tu", "tense": "past",
                "label": "tu, past"
            },
            
            # Future tense templates (2 sentences)
            {
                "template": f"({infinitive}) Domani io {{verb}}.",
                "person": "io", "tense": "future",
                "label": "io, future"
            },
            {
                "template": f"({infinitive}) Tu {{verb}} domani?",
                "person": "tu", "tense": "future",
                "label": "tu, future"
            }
        ]
        
        sentences = []
        
        for template_info in templates:
            # Get the correct conjugated form
            if template_info["tense"] == "present":
                verb_form = present[template_info["person"]]
            elif template_info["tense"] == "past":
                verb_form = past[template_info["person"]]
            else:  # future
                verb_form = future[template_info["person"]]
            
            # Create the sentence with cloze deletion
            sentence = template_info["template"].replace("{verb}", f"{{{{c1::{verb_form}}}}}")
            
            sentences.append({
                "sentence": sentence,
                "answer": verb_form,
                "label": template_info["label"]
            })
        
        return sentences
