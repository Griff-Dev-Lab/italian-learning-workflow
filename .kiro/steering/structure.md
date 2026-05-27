# Project Structure

```
italian-learning-workflow/
├── run.py                      # CLI entry point — argument parsing, error handling, calls orchestrator
├── config.yaml                 # LLM provider config (model, base URL, output dir, retries)
├── requirements.txt            # Python dependencies
├── .env                        # API key (gitignored, copied from .env.example)
├── .env.example                # Template for .env
│
├── src/                        # All application logic
│   ├── __init__.py
│   ├── orchestrator.py         # Pipeline coordinator — wires all modules for a single verb run
│   ├── llm_client.py           # LLM wrapper — OpenAI SDK, retry logic, JSON + text modes
│   ├── verb_conjugator.py      # Generates conjugation data for a verb via LLM
│   ├── flashcard_builder.py    # Builds Basic and Cloze card rows from conjugation data
│   ├── passage_builder.py      # Generates HTML reading passage for a verb
│   ├── vocab_tracker.py        # Tracks which verbs have been processed to prevent duplicates
│   └── storage.py              # Creates output folders, writes CSV and HTML files
│
└── verb_artifacts/             # Generated output (gitignored except structure)
    ├── verb_log.json           # History of all runs (verb, timestamp, folder)
    ├── vocab_state.json        # Tracks which verbs have been used
    └── mangiare/               # One folder per verb
        ├── flashcards_basic.csv    # Basic note type — import into Anki as Basic
        ├── flashcards_cloze.csv    # Cloze note type — import into Anki as Cloze
        └── passage.html            # Optional HTML reading passage (--passage flag only)
```

## Architecture Patterns

- **Single-responsibility modules** — each `src/` file owns one concern; builders only build, storage only stores
- **Orchestrator pattern** — `WorkflowOrchestrator` in `orchestrator.py` is the only place that knows the full pipeline sequence; individual modules are unaware of each other
- **Custom exception per module** — every module defines its own exception class (e.g. `FlashcardError`, `PassageError`, `LLMError`); `run.py` catches each specifically for user-friendly error messages
- **Dataclasses for structured data** — use `@dataclass` for card rows and conjugation data; avoid passing raw dicts between modules
- **Config loaded at construction time** — `LLMClient` reads `config.yaml` and env vars in `__init__`; no global state
- **`from __future__ import annotations`** — used in all modules for forward-reference type hints

## Card Data Model

**BasicCardRow** (for `flashcards_basic.csv`):
- `front` — e.g. `mangiare (io, present)`
- `back` — e.g. `mangio`

**ClozeCardRow** (for `flashcards_cloze.csv`):
- `text` — e.g. `Ogni mattina io {{c1::mangio}} un cornetto.`
- `extra` — e.g. `mangiare — io, present` (shown on back as context)

## Code Style

- Type hints on all function signatures
- Docstrings on all public classes and methods
- `Path` (from `pathlib`) used for all file system operations — no raw string paths
- File I/O always uses `encoding="utf-8"` explicitly
- JSON files written with `indent=2` and `ensure_ascii=False`
- Print statements (not logging) for user-facing progress output, prefixed with step numbers or `[ModuleName]`

## Removed Components (Phase 1)
- `quiz_builder.py` — HTML quiz removed entirely; inaccurate and not useful
- `theme_registry.py` — theme system replaced by direct verb input
- `themes.yaml` — no longer needed

## Adding a New Output Type (future phases)
1. Create `src/{name}_builder.py` with a `{Name}Error` exception and a `{Name}Builder` class that accepts `LLMClient`
2. Add the builder to `WorkflowOrchestrator` and call it in the `run()` pipeline
3. Add the new artifact to `StorageManager.write_artifacts()`
4. Catch the new exception in `run.py`
