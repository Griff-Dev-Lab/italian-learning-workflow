# Technical Design: Italian Learning Workflow

## Overview

The Italian Learning Workflow is a Python command-line application. The user runs a single entry-point script with a theme name, and the system generates three learning artifacts — a flashcard CSV, a reading passage, and an offline HTML quiz — stored in a versioned week folder. Content is generated via an LLM API (OpenAI-compatible) using structured prompts. A local JSON state file tracks vocabulary usage per theme to prevent repetition across re-runs.

---

## Architecture

### High-Level Component Diagram

```
┌─────────────────────────────────────────────────────┐
│                   run.py (CLI entry point)           │
│   args: --theme <name> [--output <dir>]              │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────▼───────────┐
         │   WorkflowOrchestrator │
         │   orchestrator.py      │
         └──┬──────┬──────┬──────┘
            │      │      │
    ┌───────▼─┐ ┌──▼────┐ ┌▼──────────┐
    │Flashcard│ │Passage│ │QuizBuilder │
    │Builder  │ │Builder│ │            │
    └───────┬─┘ └──┬────┘ └┬──────────┘
            │      │       │
            └──────┴───────┘
                   │ all use
         ┌─────────▼─────────┐
         │   LLMClient        │
         │   llm_client.py    │
         └─────────┬─────────┘
                   │
         ┌─────────▼─────────┐
         │  OpenAI-compatible │
         │  API (external)    │
         └────────────────────┘

  Supporting modules (no LLM calls):
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │ThemeRegistry │  │VocabTracker  │  │StorageManager│
  │theme_registry│  │vocab_tracker │  │storage.py    │
  │.py           │  │.py           │  │              │
  └──────────────┘  └──────────────┘  └──────────────┘
```

---

## Module Descriptions

### `run.py` — CLI Entry Point

Parses command-line arguments and delegates to `WorkflowOrchestrator`.

```
Arguments:
  --theme   (required) Theme name, case-insensitive
  --output  (optional) Root output directory, default: ./weekly_artifacts
```

### `orchestrator.py` — WorkflowOrchestrator

Coordinates the full generation pipeline:

1. Load and validate theme from `ThemeRegistry`
2. Select vocabulary via `VocabTracker`
3. Call `FlashcardBuilder` → validate → get flashcard data
4. Call `PassageBuilder` → validate word count (retry up to 3×)
5. Call `QuizBuilder` → build HTML from flashcard + passage data
6. Call `StorageManager` to create the week folder and write all files atomically
7. On any failure: instruct `StorageManager` to clean up partial folder

### `theme_registry.py` — ThemeRegistry

- Loads `themes.yaml` from project root
- Validates structure on load; raises `ThemeRegistryError` with file path + parse detail on failure
- Exposes `get_theme(name: str) -> Theme` with case-insensitive lookup
- Raises `UnknownThemeError` listing all available labels if theme not found

### `vocab_tracker.py` — VocabTracker

- Reads/writes `vocab_state.json` in the output root directory
- Tracks used words per theme per category (verbs, nouns, adjectives)
- `select_words(theme, category, count) -> list[str]` — returns unused words, cycling from oldest if exhausted
- Emits console warnings when vocabulary pool is exhausted or running low

### `llm_client.py` — LLMClient

- Thin wrapper around `openai` Python SDK
- Sends structured prompts and returns parsed JSON responses
- Handles retries (up to 3) on transient API errors
- API key loaded from environment variable `OPENAI_API_KEY`

### `flashcard_builder.py` — FlashcardBuilder

- Receives selected vocabulary (2 verbs, 2 nouns, 2 adjectives)
- Calls LLM to generate all flashcard data as structured JSON
- Validates exactly 10 rows are returned
- Writes RFC 4180-compliant UTF-8 CSV via Python `csv` module

### `passage_builder.py` — PassageBuilder

- Receives vocabulary list and theme
- Calls LLM to generate Italian passage + English translation
- Counts words; retries up to 3× if outside 150–200 word range
- Returns `(passage_it: str, passage_en: str)`

### `quiz_builder.py` — QuizBuilder

- Receives flashcard data + passage text
- Generates 10+ questions (mix of translation and fill-in-the-blank types)
- Builds a single self-contained HTML string with all CSS and JS inlined
- No external network requests in the output HTML

### `storage.py` — StorageManager

- Resolves week folder name: `week-{NN}-{theme}`, auto-increments to `-v2`, `-v3` if collision
- Creates folder, writes all four files
- On failure: deletes partial folder (cleanup)
- Maintains a `run_log.json` in the output root to track sequential run count

---

## Data Models

### Theme (from `themes.yaml`)

```yaml
themes:
  - id: food
    label: Food & Eating
    description: Vocabulary for ordering food, describing meals, and eating habits.
  - id: travel
    label: Travel
    description: Getting around, transport, directions, and accommodation.
```

### VocabState (in `vocab_state.json`)

```json
{
  "food": {
    "verbs":      { "used": ["mangiare", "bere"], "pool": ["cucinare", "assaggiare"] },
    "nouns":      { "used": ["pane"],             "pool": ["acqua", "tavolo"] },
    "adjectives": { "used": ["buono"],            "pool": ["fresco", "caldo"] }
  }
}
```

### FlashcardRow (internal dataclass)

```python
@dataclass
class FlashcardRow:
    italian_form: str        # e.g. "mangio" or "pane"
    english_translation: str # e.g. "I eat" or "bread"
    source_word: str         # infinitive or base form
    word_type: str           # "verb" | "noun" | "adjective"
    tense_label: str         # "present" | "past" | "future" | "base"
    italian_example: str     # ≤12 words
    english_example: str     # translation of italian_example
```

### QuizQuestion (internal dataclass)

```python
@dataclass
class QuizQuestion:
    question_type: str       # "translation" | "fill-in-the-blank"
    prompt: str              # question text shown to user
    options: list[str]       # exactly 4 options
    correct_index: int       # index into options (0–3)
```

---

## File Structure

```
italian-learning-workflow/
├── run.py                        # CLI entry point
├── themes.yaml                   # Theme registry (user-editable)
├── config.yaml                   # Output dir, API model, other settings
├── requirements.txt              # Python dependencies
├── src/
│   ├── orchestrator.py
│   ├── theme_registry.py
│   ├── vocab_tracker.py
│   ├── llm_client.py
│   ├── flashcard_builder.py
│   ├── passage_builder.py
│   ├── quiz_builder.py
│   └── storage.py
└── weekly_artifacts/             # Generated output (gitignored)
    ├── run_log.json
    ├── vocab_state.json
    ├── week-01-food/
    │   ├── flashcards.csv
    │   ├── passage.txt
    │   ├── passage_en.txt
    │   └── quiz.html
    └── week-02-travel/
        ├── flashcards.csv
        ├── passage.txt
        ├── passage_en.txt
        └── quiz.html
```

---

## LLM Prompt Design

All prompts request JSON responses to enable reliable parsing. The system uses a single `LLMClient` with a `call(prompt: str, schema: dict) -> dict` interface.

### Flashcard Prompt (abbreviated)

```
You are an Italian language teacher generating A1-level flashcard data.
Theme: {theme_label}
Vocabulary: {vocab_list}

Return a JSON object with key "cards" containing exactly 10 objects.
Each object must have: italian_form, english_translation, source_word,
word_type, tense_label, italian_example, english_example.

Rules:
- Verbs: 3 cards each (present, past using passato prossimo, future using futuro semplice)
- Nouns and adjectives: 1 card each (base form)
- Example sentences: max 12 words, A1 vocabulary only
- No grammar terminology beyond verb/noun/adjective/present/past/future
```

### Passage Prompt (abbreviated)

```
You are an Italian language teacher writing a short reading passage for an A1 learner.
Theme: {theme_label}
Vocabulary to include: {vocab_list}

Write a passage in Italian between 150 and 200 words.
Then write a complete English translation.

Return JSON: { "italian": "...", "english": "...", "word_count": N }

Rules:
- Use every vocabulary word at least once (conjugated/inflected forms allowed)
- A1 vocabulary only — simple, conversational sentences
- Setting and characters must relate to the theme
```

### Quiz Prompt (abbreviated)

```
You are generating quiz questions for an A1 Italian learner.
Flashcard data: {flashcard_json}
Passage: {passage_text}

Generate exactly 12 multiple-choice questions.
At least 6 must be Italian-to-English translation questions.
At least 4 must be fill-in-the-blank sentence completion questions.

Return JSON: { "questions": [ { "type": "...", "prompt": "...",
  "options": ["a","b","c","d"], "correct_index": N } ] }

Rules:
- Exactly 4 options per question
- Use only vocabulary from the flashcards or passage
- No grammar terminology
```

---

## Quiz HTML Design

The quiz is a single HTML file with all styles and logic inlined. No CDN links, no external fonts, no network requests.

### Structure

```
quiz.html
├── <head>  — inline <style> (CSS variables, layout, button states)
└── <body>
    ├── Header: week title + progress bar
    ├── Question card: prompt text
    ├── Answer grid: 2×2 button layout
    ├── Feedback area: correct/incorrect message + correct answer reveal
    ├── Next button (hidden until answer selected)
    └── Score screen (hidden until all questions answered)
    └── <script> — all quiz logic inline
```

### JavaScript Behaviour

- Questions array embedded as a JSON literal in the script block
- `shuffle()` called on load to randomize question order and option positions
- On answer click: apply `.correct` or `.incorrect` CSS class within 300ms, disable all buttons, show feedback
- On incorrect: reveal correct answer text, show Next button
- On correct: auto-advance after 1 second OR show Next button (consistent UX)
- Score screen: shows `X / 10 correct (Y%)` with a simple colour-coded result

---

## Configuration

`config.yaml` in project root:

```yaml
output_dir: ./weekly_artifacts
openai_model: gpt-4o-mini
openai_base_url: https://api.openai.com/v1   # override for local LLMs
max_retries: 3
```

API key is never stored in config — loaded from `OPENAI_API_KEY` environment variable only.

---

## Error Handling Summary

| Scenario | Behaviour |
|---|---|
| `themes.yaml` missing or malformed | Print file path + parse error, halt |
| Unknown theme name | Print unrecognised name + list all available themes, halt |
| LLM API error (transient) | Retry up to 3×, then halt with error message |
| Passage word count out of range | Regenerate up to 3×, then halt with notification |
| Flashcard row count ≠ 10 | Regenerate once, then halt with error |
| Week folder already exists | Auto-increment to `-v2`, `-v3`, etc. |
| Partial folder on failure | Delete partial folder before exit |
| Vocabulary pool exhausted | Warn user, cycle from oldest used words |

---

## Dependencies

```
openai>=1.0.0        # LLM API client
pyyaml>=6.0          # themes.yaml and config.yaml parsing
python-dotenv>=1.0   # load OPENAI_API_KEY from .env file
```

Python 3.10+ required. No other runtime dependencies.
