# Project Structure

```
italian-learning-workflow/
├── run.py                      # CLI entry point — argument parsing, error handling, calls orchestrator
├── config.yaml                 # Output directory config (no LLM config needed)
├── requirements.txt            # Python dependencies (pyyaml, mlconjug3)
│
├── src/                        # All application logic
│   ├── __init__.py
│   ├── orchestrator.py         # Pipeline coordinator — wires all modules for a single verb run
│   ├── verb_conjugator.py      # Generates conjugation data using mlconjug3 (100% accurate)
│   ├── flashcard_builder.py    # Builds Basic and Cloze card rows from conjugation data
│   ├── conjugation_table_builder.py  # Generates HTML conjugation reference tables
│   ├── vocab_tracker.py        # Tracks which verbs have been processed to prevent duplicates
│   └── storage.py              # Creates output folders, writes CSV and HTML files
│
└── verb_artifacts/             # Generated output (gitignored except structure)
    ├── verb_log.json           # History of all runs (verb, timestamp, folder)
    ├── vocab_state.json        # Tracks which verbs have been used
    └── mangiare/               # One folder per verb
        ├── flashcards_basic.csv    # Basic note type — import into Anki as Basic
        ├── flashcards_cloze.csv    # Cloze note type — import into Anki as Cloze
        └── conjugation_table.html  # Optional HTML conjugation table (--table flag)
```

## Architecture Patterns

- **Single-responsibility modules** — each `src/` file owns one concern; builders only build, storage only stores
- **Orchestrator pattern** — `WorkflowOrchestrator` in `orchestrator.py` is the only place that knows the full pipeline sequence; individual modules are unaware of each other
- **Custom exception per module** — every module defines its own exception class (e.g. `FlashcardError`, `ConjugationTableError`, `ConjugatorError`); `run.py` catches each specifically for user-friendly error messages
- **Dataclasses for structured data** — use `@dataclass` for card rows and conjugation data; avoid passing raw dicts between modules
- **No global state** — all configuration loaded at construction time
- **`from __future__ import annotations`** — used in all modules for forward-reference type hints

## Card Data Model

**BasicCardRow** (for `flashcards_basic.csv`):
- `front` — e.g. `mangiare (io, present)`
- `back` — e.g. `mangio`

**ClozeCardRow** (for `flashcards_cloze.csv`):
- `text` — e.g. `(mangiare) Ogni mattina io {{c1::mangio}}.`
- `extra` — e.g. `mangiare — io, present` (shown on back as context)

## Code Style

- Type hints on all function signatures
- Docstrings on all public classes and methods
- `Path` (from `pathlib`) used for all file system operations — no raw string paths
- File I/O always uses `encoding="utf-8"` explicitly
- JSON files written with `indent=2` and `ensure_ascii=False`
- Print statements (not logging) for user-facing progress output, prefixed with step numbers or `[ModuleName]`

## Removed Components (Cleaned Up)
- `passage_builder.py` — removed for accuracy (LLM-generated content was unreliable)
- `llm_client.py` — removed entirely (no LLM dependencies)
- `quiz_builder.py` — HTML quiz removed entirely; inaccurate and not useful
- `theme_registry.py` — theme system replaced by direct verb input
- `themes.yaml` — no longer needed
- `.env` files — no API keys needed

## 100% Accuracy Architecture

**mlconjug3 Integration**:
- `VerbConjugator` uses mlconjug3 as primary conjugation source
- Template-based cloze sentence generation (no LLM)
- Deterministic auxiliary verb selection (avere vs essere)
- Fallback patterns for edge cases

**No LLM Dependencies**:
- All conjugations from linguistic library
- All sentences from templates
- All tables from structured data
- Zero network calls required

## Adding a New Output Type (future phases)
1. Create `src/{name}_builder.py` with a `{Name}Error` exception and a `{Name}Builder` class
2. Add the builder to `WorkflowOrchestrator` and call it in the `run()` pipeline
3. Add the new artifact to `StorageManager.write_{name}()`
4. Add CLI flag and update help text
5. Catch the new exception in `run.py`
