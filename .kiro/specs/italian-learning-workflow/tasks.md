# Implementation Plan: Italian Learning Workflow

## Overview

A Python CLI tool that generates Anki flashcard CSVs and optional HTML conjugation tables for Italian verbs. All conjugations are sourced from the mlconjug3 linguistic library — no LLM, no API keys, no internet required.

## Tasks

- [x] 1. Project scaffold and configuration
  - Project directory structure: `src/`, `verb_artifacts/`
  - `requirements.txt` with: `pyyaml>=6.0`, `mlconjug3>=3.8.0`
  - `config.yaml` with `output_dir: ./verb_artifacts`
  - `.gitignore` ignoring `verb_artifacts/`, `__pycache__/`, `*.pyc`, `.env`
  - `README.md` with setup and usage instructions
  - _Requirements: R6, R8_

- [x] 2. Vocabulary tracker (`src/vocab_tracker.py`)
  - `VocabTracker` class reading/writing `vocab_state.json`
  - `has_verb(infinitive) -> bool`
  - `mark_verb(infinitive)` and `save()`
  - `all_verbs() -> list[str]`
  - _Requirements: R7_

- [x] 3. Verb conjugator (`src/verb_conjugator.py`)
  - `VerbConjugator` class initialising mlconjug3 `Conjugator(language='it')`
  - Raises `ConjugatorError` if mlconjug3 unavailable or init fails
  - `conjugate(infinitive) -> ConjugationData`
  - Extracts present tense from `Indicativo > Indicativo presente`
  - Extracts past participle from `Indicativo > Indicativo passato prossimo`
  - Prepends correct auxiliary (avere/essere) based on curated essere-verb set
  - Extracts future tense from `Indicativo > Indicativo futuro semplice`
  - Generates 8 cloze sentences from deterministic templates (no LLM)
  - Cloze sentences include infinitive prefix: `(mangiare) Ogni giorno io {{c1::mangio}}.`
  - _Requirements: R1, R3, R4_

- [x] 4. Flashcard builder (`src/flashcard_builder.py`)
  - `BasicCardRow` and `ClozeCardRow` dataclasses
  - `FlashcardBuilder.build_basic(data) -> list[BasicCardRow]` — 10 cards
  - `FlashcardBuilder.build_cloze(data) -> list[ClozeCardRow]` — 8 cards
  - `to_basic_csv(rows) -> str` — RFC 4180-compliant UTF-8 CSV
  - `to_cloze_csv(rows) -> str` — RFC 4180-compliant UTF-8 CSV
  - Raises `FlashcardError` if cloze sentences missing
  - _Requirements: R2, R3_

- [x] 5. Conjugation table builder (`src/conjugation_table_builder.py`)
  - `ConjugationTableBuilder.build_html_table(data) -> str`
  - Self-contained HTML with inline CSS
  - Groups forms by tense: Presente Indicativo, Passato Prossimo, Futuro Semplice
  - No external URLs or network requests in output
  - Raises `ConjugationTableError` on failure
  - _Requirements: R5_

- [x] 6. Storage manager (`src/storage.py`)
  - `resolve_folder_name(infinitive) -> str` — versioned name if base exists
  - `create_verb_folder(name) -> Path`
  - `write_flashcards(folder, basic_csv, cloze_csv)`
  - `write_conjugation_table(folder, table_html)`
  - `record_run(folder_name, infinitive, table)` — appends to `verb_log.json`
  - `cleanup(folder)` — deletes partial folder on failure
  - _Requirements: R6_

- [x] 7. Workflow orchestrator (`src/orchestrator.py`)
  - `WorkflowOrchestrator.run(infinitive, output_dir, force, table)`
  - Step 1: Duplicate check via `VocabTracker`
  - Step 2: Conjugate via `VerbConjugator`
  - Step 3: Build flashcards via `FlashcardBuilder`
  - Step 4: Write files via `StorageManager`
  - Step 5 (optional): Generate table via `ConjugationTableBuilder`
  - On failure: `StorageManager.cleanup()`, print error, exit
  - _Requirements: R1, R6, R7_

- [x] 8. CLI entry point (`run.py`)
  - `argparse` with: `--verb`, `--table`, `--output`, `--force`, `--list-verbs`
  - No `.env` loading — no API keys needed
  - User-friendly error messages for all known error types
  - Exit code 0 on success, 1 on error
  - _Requirements: R8_

- [x] 9. Steering files updated
  - `product.md` — reflects LLM-free, verb-focused product
  - `tech.md` — reflects mlconjug3 as primary engine, no LLM dependencies
  - `structure.md` — reflects current file structure and removed modules
  - _N/A_

- [x] 10. End-to-end validation
  - `python run.py --verb mangiare` → correct present/past/future forms
  - `python run.py --verb dormire` → dormo/dormi/dorme (not sono addormentato)
  - `python run.py --verb andare` → vado/vai/va + sono andato (essere auxiliary)
  - `python run.py --verb mangiare --table` → conjugation_table.html generated
  - Re-running same verb → duplicate warning shown
  - Re-running with `--force` → new versioned folder created
  - _Requirements: R1–R8_

## Task Dependency Graph

```
1 (scaffold)
├── 2 (vocab tracker)     ← no code deps
├── 3 (verb conjugator)   ← no code deps
├── 4 (flashcard builder) ← depends on 3
├── 5 (table builder)     ← depends on 3
├── 6 (storage manager)   ← no code deps
└── 7 (orchestrator)      ← depends on 2,3,4,5,6
    └── 8 (CLI)           ← depends on 7
        └── 9 (steering)  ← depends on 8
            └── 10 (validation)
```

Tasks 2, 3, and 6 can be built in parallel after task 1.
Tasks 4 and 5 can be built in parallel after task 3.

## Notes

- Python 3.10+ required
- No API keys or environment variables needed
- mlconjug3 is the sole source of conjugation truth — no LLM fallback
- `vocab_state.json` and `verb_log.json` are created automatically on first run
- `verb_artifacts/` is gitignored — generated content is not committed
- Removed modules: `llm_client.py`, `passage_builder.py` (LLM-generated content was inaccurate)
