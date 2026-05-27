# Tech Stack

## Language & Runtime
- Python 3.10+
- macOS (primary platform)

## Dependencies (`requirements.txt`)
- `pyyaml>=6.0` — config file parsing
- `mlconjug3>=3.8.0` — accurate Italian verb conjugations

## Conjugation Engine
- **Primary**: mlconjug3 library (100% accurate, linguistic-based)
- **No LLM dependency**: Completely offline and deterministic
- Handles all verb types: regular, irregular, avere/essere auxiliaries
- Provides perfect present, past (passato prossimo), and future forms

## Anki CSV Format
The tool produces two CSV files per run — one for Basic note type, one for Cloze note type:

**Basic notes** (`flashcards_basic.csv`):
- Columns: `front`, `back`
- Imported into Anki as note type: Basic
- Deck tag included via Anki import dialog

**Cloze notes** (`flashcards_cloze.csv`):
- Columns: `text`, `extra`
- `text` contains the sentence with `{{c1::answer}}` syntax
- Infinitive context: "(mangiare) Ogni giorno io {{c1::mangio}}."
- Imported into Anki as note type: Cloze

## Optional Conjugation Table
- **HTML output**: Beautiful, printable conjugation reference
- **Template-based**: Clean styling with CSS
- **100% accurate**: Same mlconjug3 data as flashcards

## Configuration Files
- `config.yaml` — output directory, max retries (no LLM config needed)

## Common Commands

```bash
# Generate flashcards for a verb
python run.py --verb mangiare

# Generate flashcards + conjugation table
python run.py --verb mangiare --table

# Custom output directory
python run.py --verb mangiare --output ./my_output

# First-time setup
pip install -r requirements.txt
```

## No Build Step
There is no compilation, bundling, or build process. The project runs directly with `python run.py`.

## No Test Framework
There is currently no automated test suite in the project.

## No LLM Dependencies
- ❌ No OpenAI API keys required
- ❌ No Ollama installation needed
- ❌ No internet connection required
- ✅ Works completely offline
- ✅ 100% deterministic output
