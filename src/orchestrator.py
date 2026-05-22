"""Workflow orchestrator — wires all modules together for a single run."""

from __future__ import annotations

from pathlib import Path
from typing import List

from .theme_registry import ThemeRegistry, ThemeRegistryError, UnknownThemeError
from .vocab_tracker import VocabTracker
from .llm_client import LLMClient, LLMError
from .flashcard_builder import FlashcardBuilder, FlashcardError
from .passage_builder import PassageBuilder, PassageError
from .quiz_builder import QuizBuilder, QuizError
from .storage import StorageManager

# A1-level vocabulary pools per theme — used to seed VocabTracker on first run.
# These are the words the LLM will be asked to use; the LLM generates all
# conjugations, translations, and examples from these base forms.
VOCAB_POOLS: dict[str, dict[str, List[str]]] = {
    "food": {
        "verbs": ["mangiare", "bere", "cucinare", "assaggiare", "comprare", "portare", "volere", "preferire"],
        "nouns": ["pane", "acqua", "pizza", "pasta", "caffè", "latte", "frutta", "verdura", "tavolo", "ristorante"],
        "adjectives": ["buono", "fresco", "caldo", "freddo", "dolce", "piccante", "grande", "piccolo"],
    },
    "travel": {
        "verbs": ["andare", "partire", "arrivare", "prendere", "cercare", "prenotare", "viaggiare", "tornare"],
        "nouns": ["treno", "aereo", "autobus", "biglietto", "valigia", "hotel", "stazione", "città", "mappa", "passaporto"],
        "adjectives": ["lontano", "vicino", "veloce", "lento", "nuovo", "vecchio", "bello", "comodo"],
    },
    "family": {
        "verbs": ["avere", "essere", "vivere", "abitare", "chiamare", "visitare", "aiutare", "amare"],
        "nouns": ["madre", "padre", "fratello", "sorella", "nonno", "nonna", "figlio", "figlia", "famiglia", "casa"],
        "adjectives": ["giovane", "anziano", "simpatico", "gentile", "alto", "basso", "felice", "stanco"],
    },
    "weather": {
        "verbs": ["fare", "piovere", "nevicare", "essere", "sembrare", "cambiare", "uscire", "restare"],
        "nouns": ["sole", "pioggia", "neve", "vento", "nuvola", "temperatura", "stagione", "estate", "inverno", "primavera"],
        "adjectives": ["caldo", "freddo", "nuvoloso", "soleggiato", "umido", "secco", "bello", "brutto"],
    },
    "shopping": {
        "verbs": ["comprare", "vendere", "pagare", "cercare", "trovare", "portare", "costare", "scegliere"],
        "nouns": ["negozio", "mercato", "prezzo", "soldi", "borsa", "scarpe", "vestito", "taglia", "cassa", "scontrino"],
        "adjectives": ["caro", "economico", "grande", "piccolo", "nuovo", "bello", "colorato", "comodo"],
    },
    "health": {
        "verbs": ["stare", "sentire", "avere", "andare", "prendere", "dormire", "riposare", "mangiare"],
        "nouns": ["medico", "ospedale", "farmacia", "medicina", "testa", "stomaco", "febbre", "dolore", "salute", "corpo"],
        "adjectives": ["malato", "sano", "stanco", "forte", "debole", "bene", "male", "grave"],
    },
    "home": {
        "verbs": ["abitare", "vivere", "pulire", "aprire", "chiudere", "cucinare", "dormire", "guardare"],
        "nouns": ["casa", "camera", "cucina", "bagno", "salotto", "letto", "tavolo", "sedia", "finestra", "porta"],
        "adjectives": ["grande", "piccolo", "pulito", "sporco", "nuovo", "vecchio", "comodo", "luminoso"],
    },
    "work": {
        "verbs": ["lavorare", "studiare", "iniziare", "finire", "chiamare", "scrivere", "leggere", "parlare"],
        "nouns": ["ufficio", "lavoro", "collega", "riunione", "computer", "telefono", "email", "stipendio", "orario", "capo"],
        "adjectives": ["occupato", "libero", "difficile", "facile", "importante", "urgente", "bravo", "stanco"],
    },
    "hobbies": {
        "verbs": ["giocare", "leggere", "ascoltare", "guardare", "correre", "nuotare", "disegnare", "cantare"],
        "nouns": ["libro", "musica", "sport", "calcio", "film", "bicicletta", "parco", "palestra", "hobby", "tempo"],
        "adjectives": ["divertente", "noioso", "interessante", "facile", "difficile", "bello", "rilassante", "attivo"],
    },
    "transport": {
        "verbs": ["prendere", "guidare", "aspettare", "arrivare", "partire", "camminare", "fermare", "salire"],
        "nouns": ["macchina", "autobus", "metro", "bicicletta", "fermata", "strada", "semaforo", "parcheggio", "biglietto", "conducente"],
        "adjectives": ["veloce", "lento", "pieno", "vuoto", "diretto", "comodo", "vicino", "lontano"],
    },
}


class WorkflowOrchestrator:
    """Runs the full weekly content generation pipeline."""

    def __init__(self) -> None:
        self._registry = ThemeRegistry()

    def run(self, theme_name: str, output_dir: str = "./weekly_artifacts") -> None:
        output_root = Path(output_dir)
        storage = StorageManager(output_root)
        vocab_tracker = VocabTracker(output_root)

        week_folder: Path | None = None

        try:
            # Step 1: Load and validate theme (before initialising LLM client)
            print(f"[1/6] Loading theme '{theme_name}'...")
            theme = self._registry.get_theme(theme_name)

            # Initialise LLM client only after theme is validated
            llm = LLMClient()
            self._flashcard_builder = FlashcardBuilder(llm)
            self._passage_builder = PassageBuilder(llm)
            self._quiz_builder = QuizBuilder(llm)
            print(f"      Theme: {theme.label}")
            # Step 2: Seed vocab pool and select words
            print("[2/6] Selecting vocabulary...")
            pool = VOCAB_POOLS.get(theme.id, {})
            for category, words in pool.items():
                vocab_tracker.set_pool(theme.id, category, words)

            vocab = {
                "verbs": vocab_tracker.select_words(theme.id, "verbs", 2),
                "nouns": vocab_tracker.select_words(theme.id, "nouns", 2),
                "adjectives": vocab_tracker.select_words(theme.id, "adjectives", 2),
            }
            print(f"      Verbs: {vocab['verbs']}")
            print(f"      Nouns: {vocab['nouns']}")
            print(f"      Adjectives: {vocab['adjectives']}")

            # Step 3: Generate flashcards
            print("[3/6] Generating flashcards...")
            flashcard_rows = self._flashcard_builder.build(theme, vocab)
            flashcards_csv = self._flashcard_builder.to_csv(flashcard_rows)
            print(f"      Generated {len(flashcard_rows)} flashcard rows.")

            # Step 4: Generate reading passage
            print("[4/6] Generating reading passage...")
            passage_it, passage_en = self._passage_builder.build(theme, vocab)
            word_count = len(passage_it.split())
            print(f"      Passage: {word_count} words.")

            # Step 5: Generate quiz
            print("[5/6] Generating quiz...")
            questions = self._quiz_builder.build_questions(flashcard_rows, passage_it)
            week_num = storage.next_run_number()
            folder_name = storage.resolve_folder_name(week_num, theme.id)
            quiz_html = self._quiz_builder.to_html(questions, f"Week {week_num:02d} — {theme.label}")
            print(f"      Generated {len(questions)} quiz questions.")

            # Step 6: Write artifacts
            print("[6/6] Writing artifacts...")
            week_folder = storage.create_week_folder(folder_name)
            storage.write_artifacts(week_folder, flashcards_csv, passage_it, passage_en, quiz_html)
            storage.record_run(folder_name, theme.id, vocab)
            vocab_tracker.save()

            print(f"\n✅ Done! Artifacts written to: {week_folder}")
            print(f"   flashcards.csv  — import into Anki")
            print(f"   passage.txt     — Italian reading passage ({word_count} words)")
            print(f"   passage_en.txt  — English translation")
            print(f"   quiz.html       — open in any browser")

        except (ThemeRegistryError, UnknownThemeError, LLMError,
                FlashcardError, PassageError, QuizError) as exc:
            storage.cleanup(week_folder)
            raise
        except Exception as exc:
            storage.cleanup(week_folder)
            raise
