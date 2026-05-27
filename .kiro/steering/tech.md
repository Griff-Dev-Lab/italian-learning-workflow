# Tech Stack

## Language & Runtime
- Python 3.10+
- macOS (primary platform)

## Dependencies (`requirements.txt`)
- `openai>=1.0.0` — LLM API client (used for Ollama, OpenAI, and Gemini via OpenAI-compatible interface)
- `pyyaml>=6.0` — config file parsing
- `python-dotenv>=1.0` — loads `OPENAI_API_KEY` from `.env`

## AI / LLM
- Default: Ollama running locally (`http://localhost:11434/v1`) with the `mistral` model
- The OpenAI SDK is used for all providers — Ollama, OpenAI, and Gemini all expose an OpenAI-compatible API
- Provider is switched by editing `config.yaml` (model name + base URL)
- `OPENAI_API_KEY` is always required; for Ollama it is set to the literal string `ollama`
- `llm.call()` — used for structured JSON responses (flashcard generation)
- `llm.call_text()` — used for free-text responses (passage generation)

## Anki CSV Format
The tool produces two CSV files per run — one for Basic note type, one for Cloze note type:

**Basic notes** (`flashcards_basic.csv`):
- Columns: `front`, `back`
- Imported into Anki as note type: Basic
- Deck tag included via Anki import dialog

**Cloze notes** (`flashcards_cloze.csv`):
- Columns: `text`, `extra`
- `text` contains the sentence with `{{c1::answer}}` syntax
- Imported into Anki as note type: Cloze

## Configuration Files
- `config.yaml` — LLM provider, model, base URL, output directory, max retries
- `.env` — API key (copied from `.env.example`)

## Common Commands

```bash
# Generate flashcards for a verb
python run.py --verb mangiare

# Generate flashcards + HTML reading passage
python run.py --verb mangiare --passage

# Custom output directory
python run.py --verb mangiare --output ./my_output

# First-time setup
cp .env.example .env
pip install -r requirements.txt

# Start Ollama (must be running before executing the workflow)
ollama serve

# Pull the default model (one-time)
ollama pull mistral
```

## No Build Step
There is no compilation, bundling, or build process. The project runs directly with `python run.py`.

## No Test Framework
There is currently no automated test suite in the project.
