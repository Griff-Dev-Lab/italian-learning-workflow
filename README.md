# Italian Verb Flashcard Generator

An Anki flashcard generator focused on Italian verb conjugation for A1–A2 learners. Each run takes a single verb and produces ready-to-import Anki CSV files with 100% accurate conjugations — no AI or internet required.

## What it generates

For each verb (e.g. `mangiare`), the tool creates:

- **Basic flashcards** (`flashcards_basic.csv`) — 10 cards drilling individual conjugated forms
  - All 6 present tense forms (io, tu, lui/lei, noi, voi, loro)
  - Common past tense forms (io, tu) using passato prossimo
  - Common future tense forms (io, tu) using futuro semplice

- **Cloze flashcards** (`flashcards_cloze.csv`) — 8 cards with verb used in context
  - Infinitive shown in parentheses: `(mangiare) Ogni giorno io _____`
  - Subject pronouns ensure only one correct answer
  - Covers present, past, and future tenses

- **Conjugation table** (`conjugation_table.html`) — optional visual reference
  - Clean, printable HTML showing all forms
  - Generated with `--table` flag

## Why 100% Accurate?

Conjugations come from **mlconjug3**, a professional Italian linguistics library — not an AI. This means:

- ✅ Perfect present, past, and future forms every time
- ✅ Correct auxiliary verbs (avere vs essere)
- ✅ Handles all irregular verbs (essere, avere, andare, venire...)
- ✅ No API keys, no internet, no Ollama required
- ✅ Works completely offline

## Setup

### Prerequisites
- Python 3.10+

### Installation

```bash
git clone https://github.com/Griff-Dev-Lab/italian-learning-workflow.git
cd italian-learning-workflow
pip install -r requirements.txt
```

That's it — no API keys, no Ollama, no extra setup.

## Usage

```bash
# Generate flashcards for a verb
python run.py --verb mangiare

# Generate flashcards + conjugation reference table
python run.py --verb mangiare --table

# Re-generate cards for an existing verb
python run.py --verb mangiare --force

# Custom output directory
python run.py --verb mangiare --output ./my_output

# Check which verbs have been processed
python run.py --list-verbs
```

## Output

Each run creates a folder like `verb_artifacts/mangiare/` containing:

- `flashcards_basic.csv` — Import into Anki as **Basic** note type
- `flashcards_cloze.csv` — Import into Anki as **Cloze** note type
- `conjugation_table.html` — Reference table, open in any browser (with `--table`)

## Anki Import

1. **Download Anki desktop** from [apps.ankiweb.net](https://apps.ankiweb.net)
2. **Import Basic cards**: File → Import → select `flashcards_basic.csv` → set note type to **Basic**
3. **Import Cloze cards**: File → Import → select `flashcards_cloze.csv` → set note type to **Cloze**
4. **Sync to AnkiWeb** to access on mobile

## Project Structure

```
italian-learning-workflow/
├── run.py                          # CLI entry point
├── config.yaml                     # Output directory config
├── requirements.txt                # Python dependencies
├── src/                            # Application modules
│   ├── orchestrator.py             # Main workflow coordinator
│   ├── verb_conjugator.py          # mlconjug3 conjugation engine
│   ├── flashcard_builder.py        # CSV generation for Anki
│   ├── conjugation_table_builder.py # HTML reference table
│   ├── vocab_tracker.py            # Duplicate prevention
│   └── storage.py                  # File management
└── verb_artifacts/                 # Generated output
    ├── verb_log.json               # Run history
    └── {verb}/                     # One folder per verb
        ├── flashcards_basic.csv
        ├── flashcards_cloze.csv
        └── conjugation_table.html  # (optional, --table flag)
```

## License

MIT License - see LICENSE file for details.
