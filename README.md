# Italian Verb Flashcard Generator

An Anki flashcard generator focused on Italian verb conjugation for A1–A2 learners. Each run takes a single verb and produces ready-to-import Anki CSV files plus example sentences.

## What it generates

For each verb (e.g. `mangiare`), the tool creates:

- **Basic flashcards** (10 cards) — individual conjugated forms for drilling recall
  - All 6 present tense forms (io, tu, lui/lei, noi, voi, loro)
  - Common past tense forms (io, tu) using passato prossimo  
  - Common future tense forms (io, tu) using futuro semplice

- **Cloze flashcards** (8 cards) — verb used in context with one form blanked out
  - Subject pronouns ensure only one correct answer
  - Covers present, past, and future tenses

- **Example sentences** (HTML) — clean table showing proper usage
  - 8 sentences covering all conjugated forms
  - Italian sentence with English translation
  - Semantically accurate and grammatically correct

## Setup

### Prerequisites
- macOS with 8GB+ RAM
- Python 3.10+
- Ollama installed and running (or OpenAI/Gemini API key)

### Installation

1. **Install Ollama** (free, runs locally)
   ```bash
   brew install ollama
   # OR download from https://ollama.com/download
   ```

2. **Download the Mistral model**
   ```bash
   ollama pull mistral
   ```

3. **Start Ollama**
   ```bash
   ollama serve
   ```

4. **Set up the project**
   ```bash
   git clone https://github.com/Griff-Dev-Lab/italian-learning-workflow.git
   cd italian-learning-workflow
   cp .env.example .env
   pip install -r requirements.txt
   ```

## Usage

```bash
# Generate flashcards for a verb
python run.py --verb mangiare

# Check which verbs have been processed
python run.py --list-verbs

# Re-generate cards for an existing verb
python run.py --verb mangiare --force

# Custom output directory
python run.py --verb mangiare --output ./my_output
```

## Output

Each run creates a folder like `verb_artifacts/mangiare/` containing:

- `flashcards_basic.csv` — Import into Anki as **Basic** note type
- `flashcards_cloze.csv` — Import into Anki as **Cloze** note type  
- `passage.html` — Example sentences, open in any browser

## Anki Import

1. **Download Anki desktop** from [apps.ankiweb.net](https://apps.ankiweb.net)
2. **Import Basic cards**: File → Import → select `flashcards_basic.csv` → set note type to **Basic**
3. **Import Cloze cards**: File → Import → select `flashcards_cloze.csv` → set note type to **Cloze**
4. **Sync to AnkiWeb** to access on mobile

## Features

- **Accuracy verification** — Uses mlconjug3 to verify LLM-generated conjugations
- **Semantic constraints** — Structured prompts prevent nonsensical sentences
- **Duplicate prevention** — Tracks processed verbs to avoid repeats
- **Local-first** — Runs entirely on your Mac via Ollama (no API costs)
- **Provider flexibility** — Switch to OpenAI or Gemini by editing `config.yaml`

## Switching AI Providers

Edit `config.yaml` to use different LLM providers:

| Provider | Cost | Configuration |
|---|---|---|
| **Ollama** (default) | Free | `openai_model: mistral`<br>`openai_base_url: http://localhost:11434/v1` |
| **OpenAI** | ~$0.001/run | `openai_model: gpt-4o-mini`<br>`openai_base_url: https://api.openai.com/v1` |
| **Google Gemini** | Free tier | `openai_model: gemini-1.5-flash`<br>`openai_base_url: https://generativelanguage.googleapis.com/v1beta/openai` |

## Project Structure

```
italian-learning-workflow/
├── run.py                      # CLI entry point
├── config.yaml                 # LLM provider configuration
├── requirements.txt            # Python dependencies
├── .env                        # API key (gitignored)
├── src/                        # Application modules
│   ├── orchestrator.py         # Main workflow coordinator
│   ├── verb_conjugator.py      # LLM + mlconjug3 conjugation
│   ├── flashcard_builder.py    # CSV generation for Anki
│   ├── passage_builder.py      # HTML example sentences
│   ├── vocab_tracker.py        # Duplicate prevention
│   └── storage.py              # File management
└── verb_artifacts/             # Generated output
    ├── verb_log.json           # Run history
    └── {verb}/                 # One folder per verb
        ├── flashcards_basic.csv
        ├── flashcards_cloze.csv
        └── passage.html
```

## Requirements

- macOS with 8GB+ RAM (for Ollama)
- Python 3.10+
- Ollama installed and running (or API key for OpenAI/Gemini)

## License

MIT License - see LICENSE file for details.