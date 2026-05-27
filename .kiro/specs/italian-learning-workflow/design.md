# Technical Design: Italian Learning Workflow

## Overview

The Italian Learning Workflow is a Python CLI tool that generates Anki flashcard CSVs and optional HTML conjugation tables for Italian verbs. All conjugations are sourced from the **mlconjug3** linguistic library. There is no LLM dependency, no API keys, and no internet connection required. The tool is fully deterministic and works offline.

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    run.py (CLI entry point)               │
│  --verb <infinitive>  [--table]  [--force]  [--output]   │
│  [--list-verbs]                                          │
└─────────────────────────┬────────────────────────────────┘
                          │
              ┌───────────▼───────────┐
              │  WorkflowOrchestrator  │
              │    orchestrator.py     │
              └──┬──────────┬─────────┘
                 │          │
       ┌─────────▼──┐  ┌────▼──────────────┐
       │    Verb     │  │  Flashcard         │
       │ Conjugator  │  │  Builder           │
       │             │  │                    │
       └─────────┬───┘  └────────────────────┘
                 │
       ┌─────────▼──────────┐
       │     mlconjug3       │
       │  (local library)    │
       └────────────────────┘

  Optional (--table flag only):
       ┌──────────────────────────┐
       │  ConjugationTableBuilder  │
       └──────────────────────────┘

  Supporting modules:
       ┌──────────────┐   ┌──────────────┐
       │ VocabTracker  │   │StorageManager│
       └──────────────┘   └──────────────┘
```

---

## Pipeline — Step by Step

When `python run.py --verb mangiare` is executed:

```
[1/4] Check verb — VocabTracker.has_verb()
[2/4] Conjugate  — VerbConjugator.conjugate()  →  ConjugationData
[3/4] Build      — FlashcardBuilder.build_basic() + build_cloze()
[4/4] Write      — StorageManager writes CSVs (+ HTML table if --table)
      Update     — VocabTracker.mark_verb() + save()
```

---

## Module Descriptions

### `run.py` — CLI Entry Point

Parses arguments via `argparse` and delegates to `WorkflowOrchestrator`. No business logic.

**Arguments:**

| Flag | Type | Description |
|---|---|---|
| `--verb` | required | Italian infinitive, e.g. `mangiare` |
| `--table` | flag | Generate HTML conjugation table |
| `--output` | optional | Output root directory (default: `./verb_artifacts`) |
| `--force` | flag | Bypass duplicate verb check |
| `--list-verbs` | flag | Print all processed verbs and exit |

**Error handling:** catches `ConjugatorError`, `FlashcardError`, `ConjugationTableError`, `KeyboardInterrupt`, and a generic `Exception` fallback. All print user-friendly messages and exit with code 1.

---

### `src/orchestrator.py` — WorkflowOrchestrator

Single public method: `run(infinitive, output_dir, force, table)`.

Wires all modules together in sequence. The only place that knows the full pipeline order. Individual modules are unaware of each other.

On any failure after the verb folder is created, calls `StorageManager.cleanup()` to remove the partial folder before exiting.

---

### `src/verb_conjugator.py` — VerbConjugator

**Responsibility:** Extract all conjugation forms from mlconjug3 and generate cloze sentence templates.

**Initialisation:** Creates a `mlconjug3.Conjugator(language='it')` instance. Raises `ConjugatorError` immediately if mlconjug3 is not installed or fails to initialise.

**`conjugate(infinitive) -> ConjugationData`:**

1. Calls `self._mlconjug.conjugate(infinitive)` to get the full conjugation object
2. Navigates `conjug_info` (an `OrderedDict`) to extract tense forms:
   - Present: `conjug_info['Indicativo']['Indicativo presente']` → keys `1s`, `2s`, `3s`, `1p`, `2p`, `3p`
   - Past participle: `conjug_info['Indicativo']['Indicativo passato prossimo']['1s']`
   - Future: `conjug_info['Indicativo']['Indicativo futuro semplice']` → keys `1s`, `2s`
3. Prepends the correct auxiliary to the past participle using `_get_auxiliary_verb()`
4. Generates 8 cloze sentences via `_generate_cloze_sentences()` (deterministic templates)
5. Returns a `ConjugationData` dataclass

**Auxiliary verb selection** — module-level constant `ESSERE_VERBS`:
```python
ESSERE_VERBS = {
    'andare', 'venire', 'arrivare', 'partire', 'uscire', 'entrare',
    'nascere', 'morire', 'diventare', 'rimanere', 'restare', 'stare',
    'essere', 'divenire', 'cadere', 'scendere', 'salire', 'tornare'
}
```
All other verbs default to `avere` (`ho`/`hai`).

**Fallback methods** — if mlconjug3 extraction fails for any tense, pattern-based fallbacks are used (`_fallback_present_forms`, `_fallback_past_forms`, `_fallback_future_forms`). These cover common verb endings (`-are`, `-ere`, `-ire`) and hardcoded forms for `mangiare`, `dormire`, `andare`.

**Cloze sentence templates** — 18 fixed templates, one per person/tense slot:

| # | Template | Person | Tense |
|---|---|---|---|
| 1 | `({inf}) Ogni giorno io {verb}.` | io | present |
| 2 | `({inf}) Tu {verb} spesso?` | tu | present |
| 3 | `({inf}) Lui {verb} sempre.` | lui/lei | present |
| 4 | `({inf}) Noi {verb} insieme.` | noi | present |
| 5 | `({inf}) Voi {verb} domani?` | voi | present |
| 6 | `({inf}) Loro {verb} sempre.` | loro | present |
| 7 | `({inf}) Ieri io {verb}.` | io | past |
| 8 | `({inf}) Tu {verb} ieri?` | tu | past |
| 9 | `({inf}) Lui {verb} ieri.` | lui/lei | past |
| 10 | `({inf}) Noi {verb} ieri.` | noi | past |
| 11 | `({inf}) Voi {verb} ieri?` | voi | past |
| 12 | `({inf}) Loro {verb} ieri.` | loro | past |
| 13 | `({inf}) Domani io {verb}.` | io | future |
| 14 | `({inf}) Tu {verb} domani?` | tu | future |
| 15 | `({inf}) Lui {verb} domani.` | lui/lei | future |
| 16 | `({inf}) Noi {verb} domani.` | noi | future |
| 17 | `({inf}) Voi {verb} domani?` | voi | future |
| 18 | `({inf}) Loro {verb} domani.` | loro | future |

`{verb}` is replaced with `{{c1::conjugated_form}}` for Anki cloze syntax.

---

### `src/flashcard_builder.py` — FlashcardBuilder

**Responsibility:** Transform `ConjugationData` into CSV-ready row objects.

**`build_basic(data) -> list[BasicCardRow]`** — produces exactly 18 rows:
- 6 present tense (io, tu, lui/lei, noi, voi, loro)
- 6 past tense (io, tu, lui/lei, noi, voi, loro)
- 6 future tense (io, tu, lui/lei, noi, voi, loro)

Front format: `mangiare (io, present)` | Back: `mangio`

**`build_cloze(data) -> list[ClozeCardRow]`** — iterates `data.cloze_sentences`, creates one row per sentence. Raises `FlashcardError` if the list is empty.

Extra field format: `mangiare — io, present`

**`to_basic_csv(rows) -> str`** and **`to_cloze_csv(rows) -> str`** — use Python's `csv.writer` with `QUOTE_MINIMAL` and `\n` line terminator. Returns UTF-8 string with header row.

---

### `src/conjugation_table_builder.py` — ConjugationTableBuilder

**Responsibility:** Generate a self-contained HTML reference table from `ConjugationData`.

**`build_html_table(data) -> str`** — returns a complete HTML page string with:
- Inline CSS (no external stylesheets or fonts)
- Three tense sections: Presente Indicativo, Passato Prossimo, Futuro Semplice
- Person labels in the left column, conjugated forms in green on the right
- Responsive layout, card-style sections with box shadows
- Footer: "Generato con Italian Learning Workflow"

Raises `ConjugationTableError` on failure.

---

### `src/vocab_tracker.py` — VocabTracker

**Responsibility:** Prevent the same verb being processed twice across runs.

Reads/writes `vocab_state.json` in the output root:
```json
{
  "verbs": ["mangiare", "dormire", "andare"]
}
```

**Methods:**
- `has_verb(infinitive) -> bool`
- `mark_verb(infinitive)` — adds to in-memory list
- `save()` — persists to disk (called after successful run)
- `all_verbs() -> list[str]` — used by `--list-verbs`

---

### `src/storage.py` — StorageManager

**Responsibility:** All file system operations.

Reads/writes `verb_log.json` in the output root on initialisation.

**Methods:**
- `resolve_folder_name(infinitive) -> str` — returns `mangiare`, or `mangiare-v2`, `mangiare-v3` etc. if the base name already exists
- `create_verb_folder(name) -> Path` — creates the folder
- `write_flashcards(folder, basic_csv, cloze_csv)` — writes both CSV files
- `write_conjugation_table(folder, table_html)` — writes `conjugation_table.html`
- `record_run(folder_name, infinitive, table)` — appends entry to `verb_log.json`:
  ```json
  { "run": 1, "folder": "mangiare", "verb": "mangiare", "table": true, "timestamp": "..." }
  ```
- `cleanup(folder)` — `shutil.rmtree` on partial folder

---

## Data Models

### `ConjugationData` (dataclass, `verb_conjugator.py`)

```python
@dataclass
class ConjugationData:
    infinitive: str
    present_io: str        # "mangio"
    present_tu: str        # "mangi"
    present_lui_lei: str   # "mangia"
    present_noi: str       # "mangiamo"
    present_voi: str       # "mangiate"
    present_loro: str      # "mangiano"
    past_io: str           # "ho mangiato"
    past_tu: str           # "hai mangiato"
    past_lui_lei: str      # "ha mangiato"
    past_noi: str          # "abbiamo mangiato"
    past_voi: str          # "avete mangiato"
    past_loro: str         # "hanno mangiato"
    future_io: str         # "mangerò"
    future_tu: str         # "mangerai"
    future_lui_lei: str    # "mangerà"
    future_noi: str        # "mangeremo"
    future_voi: str        # "mangerete"
    future_loro: str       # "mangeranno"
    cloze_sentences: List[dict]
    # Each dict: {"sentence": "...", "answer": "...", "label": "..."}
```

### `BasicCardRow` (dataclass, `flashcard_builder.py`)

```python
@dataclass
class BasicCardRow:
    front: str   # "mangiare (io, present)"
    back: str    # "mangio"
```

### `ClozeCardRow` (dataclass, `flashcard_builder.py`)

```python
@dataclass
class ClozeCardRow:
    text: str    # "(mangiare) Ogni giorno io {{c1::mangio}}."
    extra: str   # "mangiare — io, present"
```

---

## File Structure

```
italian-learning-workflow/
├── run.py                           # CLI entry point
├── config.yaml                      # output_dir setting
├── requirements.txt                 # pyyaml, mlconjug3
├── src/
│   ├── __init__.py
│   ├── orchestrator.py              # Pipeline coordinator
│   ├── verb_conjugator.py           # mlconjug3 engine + cloze templates
│   ├── flashcard_builder.py         # CSV row builders
│   ├── conjugation_table_builder.py # HTML table generator
│   ├── vocab_tracker.py             # Duplicate verb prevention
│   └── storage.py                   # File system operations
└── verb_artifacts/                  # Generated output (gitignored)
    ├── verb_log.json                # Run history
    ├── vocab_state.json             # Processed verbs list
    └── mangiare/                    # One folder per verb run
        ├── flashcards_basic.csv
        ├── flashcards_cloze.csv
        └── conjugation_table.html   # Only present if --table was used
```

---

## Error Handling

| Scenario | Exception | Behaviour |
|---|---|---|
| mlconjug3 not installed | `ConjugatorError` | Print install instructions, exit 1 |
| mlconjug3 fails to conjugate verb | `ConjugatorError` | Print verb name + error, exit 1 |
| No cloze sentences produced | `FlashcardError` | Print verb name, exit 1 |
| Table generation fails | `ConjugationTableError` | Print error, exit 1 |
| Verb already processed | — | Warning message, clean exit 0 (bypass with `--force`) |
| Partial folder on failure | — | `StorageManager.cleanup()` deletes folder before exit |
| Unknown CLI argument | — | argparse prints usage, exit 2 |

---

## Dependencies

```
pyyaml>=6.0        # config.yaml parsing
mlconjug3>=3.8.0   # Italian verb conjugation (sole source of truth)
```

Python 3.10+ required. No API keys, no internet connection, no LLM.

---

## Future Design Considerations

### Extended CEFR Levels (B1, B2, C1, C2)
- Add `--level` flag to `run.py` and `orchestrator.run()`
- Extend `ConjugationData` with additional tense fields (imperfetto, condizionale, congiuntivo, imperativo)
- mlconjug3 already provides all these tenses — extraction methods exist in `VerbConjugator`
- Add new tense sections to `ConjugationTableBuilder`
- Add new card rows to `FlashcardBuilder.build_basic()`

### LLM-Powered Reading Passages
- Re-introduce `src/passage_builder.py` with a `PassageBuilder` class
- Accept `LLMClient` at construction — provider-agnostic via OpenAI-compatible API
- `config.yaml` controls model name and base URL (Ollama, OpenAI, Gemini)
- `--passage` flag in CLI triggers passage generation after flashcard writing
- Passages use the verified mlconjug3 conjugations as input — LLM only writes prose, never conjugates

## Components and Interfaces

### VerbConjugator

```python
class VerbConjugator:
    def __init__(self) -> None
        # Raises ConjugatorError if mlconjug3 unavailable

    def conjugate(self, infinitive: str) -> ConjugationData
        # Raises ConjugatorError on failure
```

### FlashcardBuilder

```python
class FlashcardBuilder:
    def build_basic(self, data: ConjugationData) -> list[BasicCardRow]
    def build_cloze(self, data: ConjugationData) -> list[ClozeCardRow]
        # Raises FlashcardError if cloze_sentences is empty
    def to_basic_csv(self, rows: list[BasicCardRow]) -> str
    def to_cloze_csv(self, rows: list[ClozeCardRow]) -> str
```

### ConjugationTableBuilder

```python
class ConjugationTableBuilder:
    def build_html_table(self, data: ConjugationData) -> str
        # Raises ConjugationTableError on failure
```

### VocabTracker

```python
class VocabTracker:
    def __init__(self, output_root: Path | str) -> None
    def has_verb(self, infinitive: str) -> bool
    def mark_verb(self, infinitive: str) -> None
    def save(self) -> None
    def all_verbs(self) -> list[str]
```

### StorageManager

```python
class StorageManager:
    def __init__(self, output_root: Path | str) -> None
    def resolve_folder_name(self, infinitive: str) -> str
    def create_verb_folder(self, folder_name: str) -> Path
    def write_flashcards(self, folder: Path, basic_csv: str, cloze_csv: str) -> None
    def write_conjugation_table(self, folder: Path, table_html: str) -> None
    def record_run(self, folder_name: str, infinitive: str, table: bool) -> None
    def cleanup(self, folder: Path | None) -> None
```

### WorkflowOrchestrator

```python
class WorkflowOrchestrator:
    def run(
        self,
        infinitive: str,
        output_dir: str = "./verb_artifacts",
        force: bool = False,
        table: bool = False,
    ) -> None
```

---

## Correctness Properties

### Property 1: Conjugation accuracy
**Validates: Requirements 4.4**

Every conjugated form in the output must match the mlconjug3 source exactly — no transformation or modification after extraction.

### Property 2: Correct auxiliary verb
**Validates: Requirements 4.2**

The auxiliary verb (avere/essere) must be correct for every verb — determined by the `ESSERE_VERBS` lookup set. Verbs not in the set default to avere.

### Property 3: Unambiguous cloze cards
**Validates: Requirements 3.1, 3.2, 3.3**

Cloze sentences must always include the subject pronoun so only one conjugated form is correct. The infinitive prefix `(mangiare)` must appear on every cloze card to eliminate verb ambiguity.

### Property 4: Correct card counts
**Validates: Requirements 1.2, 1.3**

Basic CSV must always contain exactly 18 rows (6 present + 6 past + 6 future). Cloze CSV must always contain exactly 18 rows (6 present + 6 past + 6 future).

### Property 5: No folder overwrites
**Validates: Requirements 6.2**

No verb folder should ever be overwritten — versioning (`-v2`, `-v3`) must be applied when a folder already exists.

### Property 6: Atomic state update
**Validates: Requirements 7.4**

`vocab_state.json` must be updated only after a fully successful run — never on partial or failed runs.

---

## Testing Strategy

Since there is no automated test suite, correctness is validated manually:

**Conjugation accuracy:**
- Run a known regular verb (`mangiare`) and verify all 10 basic card forms against a reference grammar
- Run a known irregular verb (`andare`) and verify present tense irregular forms (`vado`, `vai`, `va`, `andiamo`, `andate`, `vanno`)
- Run an essere-auxiliary verb (`andare`, `venire`) and verify past tense uses `sono`/`sei` not `ho`/`hai`
- Run an avere-auxiliary verb (`dormire`, `mangiare`) and verify past tense uses `ho`/`hai`

**Cloze card format:**
- Verify each cloze card starts with `(infinitive)` prefix
- Verify `{{c1::form}}` syntax is present and the blanked form matches the basic card back

**Duplicate prevention:**
- Run the same verb twice and verify the second run shows the warning and exits cleanly
- Run with `--force` and verify a new versioned folder is created

**Future testing approach:**
- Unit tests for `VerbConjugator` extraction methods using known verb/form pairs
- Unit tests for `FlashcardBuilder` verifying row counts and field formats
- Integration test running the full pipeline for a set of representative verbs
