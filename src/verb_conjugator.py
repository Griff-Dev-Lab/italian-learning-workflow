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

    # Past tense (passato prossimo) — all 6 forms
    past_io: str
    past_tu: str
    past_lui_lei: str
    past_noi: str
    past_voi: str
    past_loro: str

    # Future tense (futuro semplice) — all 6 forms
    future_io: str
    future_tu: str
    future_lui_lei: str
    future_noi: str
    future_voi: str
    future_loro: str

    # Example sentences for cloze cards — one per conjugated form
    # Each sentence must use the specific form and make it the only correct answer
    cloze_sentences: List[dict]  # [{"sentence": "...", "answer": "...", "label": "io, present"}, ...]


ESSERE_VERBS = {
    'andare', 'venire', 'arrivare', 'partire', 'uscire', 'entrare',
    'nascere', 'morire', 'diventare', 'rimanere', 'restare', 'stare',
    'essere', 'divenire', 'cadere', 'scendere', 'salire', 'tornare'
}


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
                past_lui_lei=past_forms["lui_lei"],
                past_noi=past_forms["noi"],
                past_voi=past_forms["voi"],
                past_loro=past_forms["loro"],
                future_io=future_forms["io"],
                future_tu=future_forms["tu"],
                future_lui_lei=future_forms["lui_lei"],
                future_noi=future_forms["noi"],
                future_voi=future_forms["voi"],
                future_loro=future_forms["loro"],
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
        """Extract past tense forms (passato prossimo) from mlconjug3 output — all 6 persons."""
        try:
            # Get the past participle from passato prossimo
            past_participle_forms = conjugation_dict.get('Indicativo', {}).get('Indicativo passato prossimo', {})
            past_participle = past_participle_forms.get('1s', '')  # All persons have same participle
            
            if past_participle:
                # Get auxiliary verb forms for all 6 persons
                auxiliary = self._get_auxiliary_verb_all_forms(infinitive)
                
                # Combine auxiliary + past participle for all 6 forms
                return {
                    "io": f"{auxiliary['io']} {past_participle}",
                    "tu": f"{auxiliary['tu']} {past_participle}",
                    "lui_lei": f"{auxiliary['lui_lei']} {past_participle}",
                    "noi": f"{auxiliary['noi']} {past_participle}",
                    "voi": f"{auxiliary['voi']} {past_participle}",
                    "loro": f"{auxiliary['loro']} {past_participle}",
                }
            else:
                return self._fallback_past_forms(infinitive)
        except Exception:
            return self._fallback_past_forms(infinitive)

    def _extract_future_forms(self, conjugation_dict: dict, infinitive: str) -> dict:
        """Extract future tense forms (futuro semplice) from mlconjug3 output — all 6 persons."""
        try:
            future_forms = conjugation_dict.get('Indicativo', {}).get('Indicativo futuro semplice', {})
            
            return {
                "io": future_forms.get('1s', ''),
                "tu": future_forms.get('2s', ''),
                "lui_lei": future_forms.get('3s', ''),
                "noi": future_forms.get('1p', ''),
                "voi": future_forms.get('2p', ''),
                "loro": future_forms.get('3p', ''),
            }
        except Exception:
            return self._fallback_future_forms(infinitive)

    def _get_auxiliary_verb(self, infinitive: str) -> tuple:
        """Return the auxiliary verb forms (io, tu) for passato prossimo.
        
        Most verbs use 'avere', but some movement/state verbs use 'essere'.
        """
        if infinitive in ESSERE_VERBS:
            return ("sono", "sei")
        else:
            return ("ho", "hai")

    def _get_auxiliary_verb_all_forms(self, infinitive: str) -> dict:
        """Return all 6 auxiliary verb forms for passato prossimo.
        
        Most verbs use 'avere', but some movement/state verbs use 'essere'.
        """
        if infinitive in ESSERE_VERBS:
            return {
                "io": "sono",
                "tu": "sei",
                "lui_lei": "è",
                "noi": "siamo",
                "voi": "siete",
                "loro": "sono"
            }
        else:
            return {
                "io": "ho",
                "tu": "hai",
                "lui_lei": "ha",
                "noi": "abbiamo",
                "voi": "avete",
                "loro": "hanno"
            }

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
        """Fallback past forms using standard patterns — all 6 persons."""
        auxiliary = self._get_auxiliary_verb_all_forms(infinitive)
        
        if infinitive == "dormire":
            return {
                "io": "ho dormito", "tu": "hai dormito", "lui_lei": "ha dormito",
                "noi": "abbiamo dormito", "voi": "avete dormito", "loro": "hanno dormito"
            }
        elif infinitive == "mangiare":
            return {
                "io": "ho mangiato", "tu": "hai mangiato", "lui_lei": "ha mangiato",
                "noi": "abbiamo mangiato", "voi": "avete mangiato", "loro": "hanno mangiato"
            }
        elif infinitive == "andare":
            return {
                "io": "sono andato", "tu": "sei andato", "lui_lei": "è andato",
                "noi": "siamo andati", "voi": "siete andati", "loro": "sono andati"
            }
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
                "io": f"{auxiliary['io']} {past_participle}",
                "tu": f"{auxiliary['tu']} {past_participle}",
                "lui_lei": f"{auxiliary['lui_lei']} {past_participle}",
                "noi": f"{auxiliary['noi']} {past_participle}",
                "voi": f"{auxiliary['voi']} {past_participle}",
                "loro": f"{auxiliary['loro']} {past_participle}"
            }

    def _fallback_future_forms(self, infinitive: str) -> dict:
        """Fallback future forms using standard patterns — all 6 persons."""
        if infinitive == "dormire":
            return {
                "io": "dormirò", "tu": "dormirai", "lui_lei": "dormirà",
                "noi": "dormiremo", "voi": "dormirete", "loro": "dormiranno"
            }
        elif infinitive == "mangiare":
            return {
                "io": "mangerò", "tu": "mangerai", "lui_lei": "mangerà",
                "noi": "mangeremo", "voi": "mangerete", "loro": "mangeranno"
            }
        else:
            # Standard future formation
            if infinitive.endswith("are"):
                future_root = infinitive[:-3] + "er"
            else:
                future_root = infinitive[:-1]  # remove final 'e'
            
            return {
                "io": f"{future_root}ò",
                "tu": f"{future_root}ai",
                "lui_lei": f"{future_root}à",
                "noi": f"{future_root}emo",
                "voi": f"{future_root}ete",
                "loro": f"{future_root}anno"
            }

    def _generate_cloze_sentences(self, infinitive: str, present: dict, past: dict, future: dict) -> list:
        """Generate cloze sentences using deterministic templates for maximum accuracy."""
        
        # Template patterns for different verb types and contexts
        templates = [
            # Present tense templates (6 sentences)
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
            {
                "template": f"({infinitive}) Voi {{verb}} domani?",
                "person": "voi", "tense": "present",
                "label": "voi, present"
            },
            {
                "template": f"({infinitive}) Loro {{verb}} sempre.",
                "person": "loro", "tense": "present",
                "label": "loro, present"
            },
            
            # Past tense templates (6 sentences)
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
            {
                "template": f"({infinitive}) Lui {{verb}} ieri.",
                "person": "lui_lei", "tense": "past",
                "label": "lui/lei, past"
            },
            {
                "template": f"({infinitive}) Noi {{verb}} ieri.",
                "person": "noi", "tense": "past",
                "label": "noi, past"
            },
            {
                "template": f"({infinitive}) Voi {{verb}} ieri?",
                "person": "voi", "tense": "past",
                "label": "voi, past"
            },
            {
                "template": f"({infinitive}) Loro {{verb}} ieri.",
                "person": "loro", "tense": "past",
                "label": "loro, past"
            },
            
            # Future tense templates (6 sentences)
            {
                "template": f"({infinitive}) Domani io {{verb}}.",
                "person": "io", "tense": "future",
                "label": "io, future"
            },
            {
                "template": f"({infinitive}) Tu {{verb}} domani?",
                "person": "tu", "tense": "future",
                "label": "tu, future"
            },
            {
                "template": f"({infinitive}) Lui {{verb}} domani.",
                "person": "lui_lei", "tense": "future",
                "label": "lui/lei, future"
            },
            {
                "template": f"({infinitive}) Noi {{verb}} domani.",
                "person": "noi", "tense": "future",
                "label": "noi, future"
            },
            {
                "template": f"({infinitive}) Voi {{verb}} domani?",
                "person": "voi", "tense": "future",
                "label": "voi, future"
            },
            {
                "template": f"({infinitive}) Loro {{verb}} domani.",
                "person": "loro", "tense": "future",
                "label": "loro, future"
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
