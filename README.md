# Italian Verb Flashcard Generator

An Anki flashcard generator focused on Italian verb conjugation for A1–A2 learners. Each run takes a single verb and produces ready-to-import Anki CSV files with 100% accurate conjugations — no AI or internet required.

## What it generates

For each verb (e.g. `mangiare`), the tool creates:

- **Basic flashcards** (`flashcards_basic.csv`) — 18 cards drilling individual conjugated forms
  - All 6 present tense forms (io, tu, lui/lei, noi, voi, loro)
  - All 6 past tense forms (passato prossimo)
  - All 6 future tense forms (futuro semplice)
  - Explicit Italian tense names (Presente Indicativo, Passato Prossimo, Futuro Semplice)

- **Cloze grid flashcards** (`flashcards_cloze.csv`) — 3 cards with all 6 persons in grid format
  - One card per tense (Presente, Passato, Futuro)
  - All 6 persons visible with one form hidden as cloze
  - Randomized hidden form (no two cards hide the same person)
  - Tests pattern recognition and conjugation accuracy

- **Conjugation table** (`conjugation_table.html`) — optional visual reference
  - Clean, printable HTML showing all forms for all 6 persons
  - Includes English translation in title (if verb is in the list)
  - Generated with `--table` flag

- **Definition flashcards** (`definitions_deck.csv`) — optional vocabulary learning
  - Generate all 57 A1-A2 verb definitions at once with `--definitions-batch`
  - One Basic card per verb: Front `to eat`, Back `mangiare`
  - Import as separate "Italian Verbs — Definitions" deck in Anki
  - Set field separator to **Comma** during import

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
python3 run.py --verb mangiare

# Generate flashcards + conjugation reference table
python3 run.py --verb mangiare --table

# Re-generate cards for an existing verb
python3 run.py --verb mangiare --force

# Custom output directory
python3 run.py --verb mangiare --output ./my_output

# Check which verbs have been processed
python3 run.py --list-verbs

# Generate definition cloze cards for all 57 A1-A2 verbs
python3 run.py --definitions-batch

# Generate definitions to custom output directory
python3 run.py --definitions-batch --output ./my_output
```

## Output

Each run creates a folder like `verb_artifacts/mangiare/` containing:

- `flashcards_basic.csv` — Import into Anki as **Basic** note type (18 cards)
- `flashcards_cloze.csv` — Import into Anki as **Cloze** note type (3 cards)
- `conjugation_table.html` — Reference table, open in any browser (with `--table`)

**Batch definitions mode** creates:

- `definitions_deck.csv` — Import into Anki as **Cloze** note type (57 cards, all A1-A2 verbs)

## Verbs Beyond the Recommended List

You can generate flashcards for **any Italian verb**, not just the recommended 57. The workflow will:

- ✅ Generate **100% accurate conjugations** (via mlconjug3)
- ✅ Create all flashcards and HTML tables
- ⚠️ Skip English translation if the verb isn't in our list

### Example: Using a Verb Not in the List

```bash
# Generate flashcards for "dormire" (not in the 57-verb list)
python3 run.py --verb dormire --table
```

**Result:**
- ✅ 18 basic cards with perfect conjugations
- ✅ 3 cloze grid cards with perfect conjugations
- ✅ HTML table with all conjugations
- ⚠️ HTML title shows just `dormire` (no English translation)

### Adding Custom Translations

To add English translations for verbs not in the list, edit `src/verb_translations.json`:

```json
{
  "dormire": "to sleep",
  "mangiare": "to eat",
  ...
}
```

Then regenerate the verb:

```bash
python3 run.py --verb dormire --table --force
```

The HTML table will now show: `dormire (to sleep)`

## Anki Import

See the complete [Anki Setup Guide](docs/ANKI_SETUP.md) for step-by-step instructions on:
- Downloading and installing Anki
- Creating a deck
- Importing basic and cloze flashcards
- Syncing to AnkiWeb for mobile access
- Troubleshooting common issues

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

## Roadmap

See the complete [Roadmap](docs/ROADMAP.md) for detailed plans on:

### 🎓 Extended CEFR Levels (B1, B2, C1, C2)
Expand beyond A1–A2 to cover intermediate and advanced learners with additional tenses and moods.

### 📚 Extended Tenses and Moods
- **Imperfetto** — imperfect past, essential for A2/B1 storytelling
- **Condizionale** — conditional mood ("I would eat")
- **Congiuntivo** — subjunctive mood, required for B2+
- **Imperativo** — commands and requests

### 📖 LLM-Powered Reading Passages
Optional `--passage` flag to generate contextual reading texts built around the verb's conjugated forms. Will support:
- Local models via **Ollama** (free, fully offline)
- API-driven models via **OpenAI** or **Google Gemini**
- Configurable via `config.yaml` — switch provider without code changes

### 🔧 Batch Processing & Automation
Generate flashcards for multiple verbs in a single command.

### 🌍 Web & Mobile Platforms
Bring the workflow to web and mobile for seamless learning across devices.

---

## License

MIT License - see LICENSE file for details.
