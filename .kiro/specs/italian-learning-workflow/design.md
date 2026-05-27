# Technical Design: Italian Learning Workflow

## Overview

The Italian Learning Workflow is a Python CLI tool that generates Anki flashcard CSVs and optional HTML conjugation tables for Italian verbs. All conjugations are sourced from the **mlconjug3** linguistic library — there is no LLM dependency, no API keys, and no internet connection required. The tool is fully deterministic and works offline.

---

## Architecture

### High-Level Component Diagram

```
┌─────────────────────────────────────────────────────┐
│                   run.py (CLI entry point)           │
│   args: --verb <infinitive> [--table] [--force]      │
│         [--output <dir>] [--list-verbs]              │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────▼───────────┐
         │   WorkflowOrchestrator │
         │   orchestrator.py      │
         └──┬──────────┬─────────┘
            │          │
    ┌───────▼──┐  ┌────▼──────────────────┐
    │ Verb     │  │ Flashcard              │
    │Conjugator│  │ Builder                │
    │          │  │                        │
    └───────┬──┘  └────────────────────────┘
            │
    ┌───────▼──────────┐
    │   mlconjug3       │
    │   (local library) │
    └───────────────────┘

  Optional output:
    ┌──────────────────────────┐
    │ ConjugationTableBuilder  │  (--table flag only)
    └──────────────────────────┘

  Supporting modules (no conjugation calls):
  ┌──────────────┐  ┌──────────────┐
  │VocabTracker  │  │StorageManager│
  │vocab_tracker │  │storage.py    │
  │.py           │  │              │
  └──────────────┘  └──────────────┘
```

---

## Module Descriptions

### `run.py` — CLI Entry Point

Parses command-line arguments and delegates to `WorkflowOrchestrator`.

```
Arguments:
  --verb        (required) Italian verb infinitive, e.g. mangiare
  --table       (optional) Generate HTML conjugation reference table
  --output      (optional) Root output directory, default: ./verb_artifacts
  --force       (optional) Bypass duplicate verb check
  --list-verbs  (optional) List all processed verbs and exit
```

Catches and displays user-friendly messages for: `ConjugatorError`, `FlashcardError`, `ConjugationTableError`, `KeyboardInterrupt`.

### `orchestrator.py` — WorkflowOrchestrator

Coordinates the full generation pipeline:

1. Check for duplicate verb via `VocabTracker` (skip if `--force`)
2. Generate conjugation data via `VerbConjugator`
3. Build flashcard rows via `FlashcardBuilder`
4. Write CSV files via `StorageManager`
5. Optionally generate conjugation table via `ConjugationTableBuilder` (if `--table`)
6. Update `VocabTracker` state
7. On any failure: call `StorageManager.cleanup()` to remove partial folder

### `verb_conjugator.py` — VerbConjugator

- Initialises mlconjug3 `Conjugator` for Italian on construction
- Raises `ConjugatorError` if mlconjug3 is not installed or fails to initialise
- `conjugate(infinitive) -> ConjugationData` — extracts all required forms from mlconjug3
- Extracts present tense from `Indicativo > Indicativo presente`
- Extracts past participle from `Indicativo > Indicativo passato prossimo` and prepends correct auxiliary
- Extracts future tense from `Indicativo > Indicativo futuro semplice`
- Determines auxiliary verb (avere/essere) via a curated lookup set of essere-verbs
- Generates cloze sentences using deterministic templates (no LLM)

### `flashcard_builder.py` — FlashcardBuilder

- Receives `ConjugationData` dataclass
- `build_basic(data) -> list[BasicCardRow]` — produces 10 basic cards
- `build_cloze(data) -> list[ClozeCardRow]` — produces 8 cloze cards from `data.cloze_sentences`
- `to_basic_csv(rows) -> str` — RFC 4180-compliant UTF-8 CSV string
- `to_cloze_csv(rows) -> str` — RFC 4180-compliant UTF-8 CSV string
- Raises `FlashcardError` if cloze sentences are missing

### `conjugation_table_builder.py` — ConjugationTableBuilder

- Receives `ConjugationData` dataclass
- `build_html_table(data) -> str` — generates a complete, self-contained HTML page
- HTML includes inline CSS with clean table styling
- Groups forms by tense: Presente Indicativo, Passato Prossimo, Futuro Semplice
- No external URLs, fonts, or network requests in the output HTML
- Raises `ConjugationTableError` on failure

### `vocab_tracker.py` — VocabTracker

- Reads/writes `vocab_state.json` in the output root
- `has_verb(infinitive) -> bool` — checks if verb has been processed
- `mark_verb(infinitive)` — records verb as processed
- `all_verbs() -> list[str]` — returns all processed verbs
- `save()` — persists state to disk

### `storage.py` — StorageManager

- `resolve_folder_name(infinitive) -> str` — returns versioned name (`-v2`, `-v3`) if base exists
- `create_verb_folder(name) -> Path` — creates folder and returns path
- `write_flashcards(folder, basic_csv, cloze_csv)` — writes both CSV files
- `write_conjugation_table(folder, table_html)` — writes optional HTML table
- `record_run(folder_name, infinitive, table)` — appends to `verb_log.json`
- `cleanup(folder)` — deletes partial folder on failure

---

## Data Models

### ConjugationData (dataclass)

```python
@dataclass
class ConjugationData:
    infinitive: str

    # Present tense — all 6 forms
    present_io: str       # e.g. "mangio"
    present_tu: str       # e.g. "mangi"
    present_lui_lei: str  # e.g. "mangia"
    present_noi: str      # e.g. "mangiamo"
    present_voi: str      # e.g. "mangiate"
    present_loro: str     # e.g. "mangiano"

    # Past tense (passato prossimo) — io, tu only
    past_io: str          # e.g. "ho mangiato"
    past_tu: str          # e.g. "hai mangiato"

    # Future tense (futuro semplice) — io, tu only
    future_io: str        # e.g. "mangerò"
    future_tu: str        # e.g. "mangerai"

    # Cloze sentences — generated from templates
    cloze_sentences: list[dict]
    # Each dict: {"sentence": "...", "answer": "...", "label": "..."}
```

### BasicCardRow (dataclass)

```python
@dataclass
class BasicCardRow:
    front: str   # e.g. "mangiare (io, present)"
    back: str    # e.g. "mangio"
```

### ClozeCardRow (dataclass)

```python
@dataclass
class ClozeCardRow:
    text: str    # e.g. "(mangiare) Ogni giorno io {{c1::mangio}}."
    extra: str   # e.g. "mangiare — io, present"
```

---

## Cloze Sentence Templates

Sentences are generated deterministically from fixed templates — no LLM involved:

| Person | Tense   | Template                              |
|--------|---------|---------------------------------------|
| io     | present | `({inf}) Ogni giorno io {verb}.`      |
| tu     | present | `({inf}) Tu {verb} spesso?`           |
| lui    | present | `({inf}) Lui {verb} sempre.`          |
| noi    | present | `({inf}) Noi {verb} insieme.`         |
| io     | past    | `({inf}) Ieri io {verb}.`             |
| tu     | past    | `({inf}) Tu {verb} ieri?`             |
| io     | future  | `({inf}) Domani io {verb}.`           |
| tu     | future  | `({inf}) Tu {verb} domani?`           |

---

## Auxiliary Verb Selection

For passato prossimo, the correct auxiliary is determined by a curated set:

```python
ESSERE_VERBS = {
    'andare', 'venire', 'arrivare', 'partire', 'uscire', 'entrare',
    'nascere', 'morire', 'diventare', 'rimanere', 'restare', 'stare',
    'essere', 'divenire', 'cadere', 'scendere', 'salire', 'tornare'
}
# All other verbs default to avere
```

---

## File Structure

```
italian-learning-workflow/
├── run.py                          # CLI entry point
├── config.yaml                     # Output directory config
├── requirements.txt                # pyyaml, mlconjug3
├── src/
│   ├── __init__.py
│   ├── orchestrator.py             # Pipeline coordinator
│   ├── verb_conjugator.py          # mlconjug3 conjugation engine
│   ├── flashcard_builder.py        # CSV generation for Anki
│   ├── conjugation_table_builder.py # HTML reference table
│   ├── vocab_tracker.py            # Duplicate verb prevention
│   └── storage.py                  # File management
└── verb_artifacts/                 # Generated output (gitignored)
    ├── verb_log.json               # Run history
    ├── vocab_state.json            # Processed verbs tracking
    └── mangiare/                   # One folder per verb
        ├── flashcards_basic.csv
        ├── flashcards_cloze.csv
        └── conjugation_table.html  # Optional (--table flag)
```

---

## Error Handling

| Scenario | Behaviour |
|---|---|
| mlconjug3 not installed | `ConjugatorError` with install instructions, halt |
| mlconjug3 fails to conjugate verb | `ConjugatorError` with verb name, halt |
| No cloze sentences generated | `FlashcardError`, halt |
| Verb already processed | Warning message, exit cleanly (bypass with `--force`) |
| Partial folder on failure | Delete partial folder before exit |
| Unknown CLI argument | argparse error with usage, exit 1 |

---

## Dependencies

```
pyyaml>=6.0          # config.yaml parsing
mlconjug3>=3.8.0     # Italian verb conjugation (primary engine)
```

Python 3.10+ required. No API keys, no internet connection, no LLM.
