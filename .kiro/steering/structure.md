# Project Structure

```
italian-learning-workflow/
├── run.py                  # CLI entry point — argument parsing, error handling, calls orchestrator
├── config.yaml             # LLM provider config (model, base URL, output dir, retries)
├── themes.yaml             # Theme definitions — edit here to add new themes
├── requirements.txt        # Python dependencies
├── .env                    # API key (gitignored, copied from .env.example)
├── .env.example            # Template for .env
│
├── src/                    # All application logic
│   ├── __init__.py
│   ├── orchestrator.py     # Pipeline coordinator — wires all modules, runs 6-step workflow
│   ├── llm_client.py       # LLM wrapper — OpenAI SDK, retry logic, JSON + text modes
│   ├── theme_registry.py   # Loads/validates themes.yaml, provides Theme dataclass
│   ├── vocab_tracker.py    # Tracks used vocabulary per theme/category across runs
│   ├── flashcard_builder.py # Generates 10-row Anki CSV via LLM
│   ├── passage_builder.py  # Generates Italian passage + English translation via LLM
│   ├── quiz_builder.py     # Generates multiple-choice HTML quiz via LLM
│   └── storage.py          # Creates week folders, writes artifacts, manages run_log.json
│
└── weekly_artifacts/       # Generated output (gitignored except structure)
    ├── vocab_state.json    # Persistent vocab usage state per theme
    ├── run_log.json        # History of all runs
    └── week-NN-{theme}/    # One folder per run
        ├── flashcards.csv
        ├── passage.txt
        ├── passage_en.txt
        └── quiz.html
```

## Architecture Patterns

- **Single-responsibility modules** — each `src/` file owns one concern; builders only build, storage only stores
- **Orchestrator pattern** — `WorkflowOrchestrator` in `orchestrator.py` is the only place that knows the full pipeline sequence; individual modules are unaware of each other
- **Custom exception per module** — every module defines its own exception class (e.g. `FlashcardError`, `PassageError`, `LLMError`); `run.py` catches each specifically for user-friendly error messages
- **Dataclasses for structured data** — `Theme`, `FlashcardRow` use `@dataclass`; avoid passing raw dicts between modules
- **Config loaded at construction time** — `LLMClient` reads `config.yaml` and env vars in `__init__`; no global state
- **`from __future__ import annotations`** — used in all modules for forward-reference type hints

## Code Style

- Type hints on all function signatures
- Docstrings on all public classes and methods
- `Path` (from `pathlib`) used for all file system operations — no raw string paths
- File I/O always uses `encoding="utf-8"` explicitly
- JSON files written with `indent=2` and `ensure_ascii=False`
- Print statements (not logging) for user-facing progress output, prefixed with step numbers or `[ModuleName]`

## Adding a New Content Builder

1. Create `src/{name}_builder.py` with a `{Name}Error` exception and a `{Name}Builder` class that accepts `LLMClient`
2. Add the builder to `WorkflowOrchestrator.__init__` and call it in the `run()` pipeline
3. Add the new artifact to `StorageManager.write_artifacts()`
4. Catch the new exception in `run.py`
