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

### Single-Verb Mode
The tool produces two CSV files per run — one for Basic note type, one for Cloze note type:

**Basic notes** (`flashcards_basic.csv`):
- Columns: `front`, `back`
- 18 rows per verb (6 present + 6 past + 6 future)
- Front format: `{infinitive} ({person}, {tense})` — e.g. `mangiare (io, Presente Indicativo)`
- Back: conjugated form — e.g. `mangio`
- **Gender/number agreement shown for essere-auxiliary verbs** — e.g. `sono andato / andata` (m.s./f.s.), `siamo andati / andate` (m.pl./f.pl.)
- **Avere-auxiliary verbs show invariant forms** — e.g. `ho mangiato` (same for all genders)
- Imported into Anki as note type: Basic
- Deck: Italian Verbs

**Cloze Grid notes** (`flashcards_cloze.csv`):
- Columns: `text`, `extra`
- 3 rows per verb (one per tense: present, past, future)
- `text` contains HTML grid with all 6 persons, one form hidden as `{{c1::form}}`
- Randomized hidden forms (no two cards hide the same person)
- `extra` field shows complete grid with all forms revealed
- Imported into Anki as note type: Cloze
- Deck: Italian Verbs

### Batch Definitions Mode
When using `--definitions-batch` flag:

**Definition Basic notes** (`definitions_deck.csv`):
- Columns: `front`, `back`
- 57 rows (one per A1-A2 verb)
- `front`: English translation (e.g., `to eat`)
- `back`: Italian infinitive (e.g., `mangiare`)
- Imported into Anki as note type: Basic
- Deck: Italian Verbs — Definitions

## Optional Conjugation Table
- **HTML output**: Beautiful, printable conjugation reference
- **Template-based**: Clean styling with CSS
- **100% accurate**: Same mlconjug3 data as flashcards

## Configuration Files
- `config.yaml` — output directory, max retries (no LLM config needed)

## Common Commands

```bash
# Generate flashcards for a verb
python3 run.py --verb mangiare

# Generate flashcards + conjugation table
python3 run.py --verb mangiare --table

# Custom output directory
python3 run.py --verb mangiare --output ./my_output

# Force regeneration (bypass duplicate check)
python3 run.py --verb mangiare --force

# List all processed verbs
python3 run.py --list-verbs

# Generate definition cloze cards for all 57 A1-A2 verbs
python3 run.py --definitions-batch

# Generate definitions to custom output directory
python3 run.py --definitions-batch --output ./my_output

# First-time setup
pip install -r requirements.txt
```

## No Build Step
There is no compilation, bundling, or build process. The project runs directly with `python3 run.py`.

## No Test Framework
There is currently no automated test suite in the project.

## No LLM Dependencies
- ❌ No OpenAI API keys required
- ❌ No Ollama installation needed
- ❌ No internet connection required
- ✅ Works completely offline
- ✅ 100% deterministic output
