# Implementation Plan: Italian Learning Workflow

## Overview

Build a Python CLI tool that generates weekly Italian learning artifacts (Anki flashcard CSV, reading passage, offline HTML quiz) from a chosen theme. Content is generated via an LLM API. All artifacts are stored in versioned per-week folders.

## Tasks

- [x] 1. Project scaffold and configuration
  - Create project directory structure: `src/`, `weekly_artifacts/`
  - Create `requirements.txt` with pinned dependencies: `openai>=1.0.0`, `pyyaml>=6.0`, `python-dotenv>=1.0`
  - Create `config.yaml` with default `output_dir`, `openai_model`, `openai_base_url`, `max_retries`
  - Create `.env.example` with `OPENAI_API_KEY=your-key-here`
  - Create `.gitignore` ignoring `weekly_artifacts/`, `.env`, `__pycache__/`, `*.pyc`
  - Create top-level `README.md` with setup and usage instructions
  - _Requirements: R1, R5, R7_

- [x] 2. Theme registry (`themes.yaml` + `src/theme_registry.py`)
  - Create `themes.yaml` with 10 pre-defined themes: food, travel, family, weather, shopping, health, home, work, hobbies, transport — each with `id`, `label`, and `description`
  - Implement `ThemeRegistry` class that loads and validates `themes.yaml` on init
  - Implement `get_theme(name: str) -> Theme` with case-insensitive lookup
  - Raise `ThemeRegistryError` with file path and parse detail if file is missing or malformed
  - Raise `UnknownThemeError` listing all available labels if theme name not found
  - _Requirements: R7_

- [x] 3. Vocabulary tracker (`src/vocab_tracker.py`)
  - Implement `VocabTracker` class that reads/writes `vocab_state.json` in the output root
  - Implement `select_words(theme_id, category, count) -> list[str]` returning unused words first
  - Track used words per theme per category (verbs, nouns, adjectives)
  - When fewer than `count` unused words remain, emit a console warning and reuse oldest words to fill the count
  - When a category pool is fully exhausted, emit a named warning and cycle from oldest run
  - Persist updated state back to `vocab_state.json` after each successful run
  - _Requirements: R6_

- [x] 4. LLM client (`src/llm_client.py`)
  - Implement `LLMClient` class wrapping the `openai` SDK
  - Load `OPENAI_API_KEY` from environment (via `python-dotenv`); raise clear error if missing
  - Load model and base URL from `config.yaml`
  - Implement `call(prompt: str) -> dict` that sends prompt, expects JSON response, and parses it
  - Retry up to `max_retries` times on transient API errors with exponential backoff
  - Raise `LLMError` with detail after all retries exhausted
  - _Requirements: R1, R8_

- [x] 5. Flashcard builder (`src/flashcard_builder.py`)
  - Implement `FlashcardBuilder` class accepting `LLMClient`
  - Define `FlashcardRow` dataclass with all 7 fields
  - Implement `build(theme, vocab) -> list[FlashcardRow]` that calls LLM with structured flashcard prompt
  - Validate exactly 10 rows returned; retry once if count is wrong, then raise `FlashcardError`
  - Implement `to_csv(rows, filepath)` writing RFC 4180-compliant UTF-8 CSV with header row
  - Quote all fields containing commas using Python `csv.writer` with `quoting=csv.QUOTE_MINIMAL`
  - _Requirements: R2_

- [x] 6. Passage builder (`src/passage_builder.py`)
  - Implement `PassageBuilder` class accepting `LLMClient`
  - Implement `build(theme, vocab) -> tuple[str, str]` returning `(italian_text, english_text)`
  - Call LLM with passage prompt requesting JSON with `italian`, `english`, `word_count` fields
  - Validate word count is 150–200; retry up to 3 times if outside range
  - After 3 failed attempts, raise `PassageError` with notification message
  - _Requirements: R3_

- [x] 7. Quiz builder (`src/quiz_builder.py`)
  - Implement `QuizBuilder` class accepting `LLMClient`
  - Define `QuizQuestion` dataclass with `question_type`, `prompt`, `options`, `correct_index`
  - Implement `build_questions(flashcard_rows, passage_text) -> list[QuizQuestion]` calling LLM
  - Validate at least 10 questions returned, at least 2 types present, exactly 4 options each
  - Implement `to_html(questions, week_title) -> str` generating fully self-contained HTML
  - HTML must inline all CSS and JavaScript — no external URLs
  - JavaScript must shuffle question order and option positions on page load
  - Implement correct/incorrect visual feedback within 300ms, Next button reveal on incorrect, auto-advance on correct
  - Render final score screen showing `X / N correct (Y%)`
  - _Requirements: R4_

- [x] 8. Storage manager (`src/storage.py`)
  - Implement `StorageManager` class accepting output root path
  - Implement `resolve_folder_name(week_num, theme_id) -> Path` returning versioned name (`-v2`, `-v3`) if base name exists
  - Implement `create_week_folder(name) -> Path` creating folder and returning path
  - Implement `write_artifacts(folder, flashcards_csv, passage_it, passage_en, quiz_html)` writing all 4 files
  - Implement `cleanup(folder)` deleting a partially written folder on failure
  - Maintain `run_log.json` in output root tracking sequential run count and folder names
  - Create output root directory if it does not exist
  - _Requirements: R5_

- [x] 9. Workflow orchestrator (`src/orchestrator.py`)
  - Implement `WorkflowOrchestrator` class wiring all modules together
  - Implement `run(theme_name, output_dir)` executing the full pipeline in order
  - On any step failure: call `StorageManager.cleanup()`, print which artifact failed, exit with non-zero code
  - On success: print output folder path and summary of generated files
  - _Requirements: R1, R5, R6_

- [x] 10. CLI entry point (`run.py`)
  - Implement argument parsing with `argparse`: `--theme` (required), `--output` (optional, default `./weekly_artifacts`)
  - Load `.env` via `python-dotenv` before any other imports
  - Instantiate and call `WorkflowOrchestrator`
  - Print user-friendly error messages for all known error types
  - Exit with code 0 on success, 1 on any error
  - _Requirements: R1, R7_

- [ ] 11. End-to-end validation
  - Run `python run.py --theme food` and verify `weekly_artifacts/week-01-food/` is created
  - Verify `flashcards.csv` has header row and exactly 10 data rows
  - Verify `passage.txt` word count is between 150 and 200
  - Verify `quiz.html` loads offline and score screen displays
  - Run with unknown theme and verify error message lists available themes
  - _Requirements: R1, R2, R3, R4, R5, R6, R7, R8_

## Task Dependency Graph

```
1 (scaffold)
├── 2 (theme registry)   ← no code deps
├── 3 (vocab tracker)    ← no code deps
├── 4 (llm client)       ← no code deps
│   ├── 5 (flashcard builder)
│   ├── 6 (passage builder)
│   └── 7 (quiz builder)
├── 8 (storage manager)  ← no code deps
└── 9 (orchestrator)     ← depends on 2,3,4,5,6,7,8
    └── 10 (CLI)         ← depends on 9
        └── 11 (validation)
```

Tasks 2, 3, 4, and 8 can be built in parallel after task 1.
Tasks 5, 6, 7 can be built in parallel after task 4.
Tasks 9, 10, 11 must be sequential.

## Notes

- Python 3.10+ required
- API key loaded from `OPENAI_API_KEY` environment variable only — never stored in config files
- All LLM prompts request JSON responses for reliable parsing
- `vocab_state.json` and `run_log.json` are created automatically on first run
- The `weekly_artifacts/` folder is gitignored — generated content is not committed
