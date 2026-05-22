# Italian Learning Workflow

A weekly content generator for A1-level Italian learners. Each run produces:

- **Anki flashcard CSV** — 10 cards (2 verbs × 3 tenses + 2 nouns + 2 adjectives)
- **Reading passage** — 150–200 word Italian text with English translation
- **Offline HTML quiz** — Duolingo-style multiple choice, runs in any browser without internet

Runs entirely on your Mac using Ollama — no API key, no cost, no data leaves your machine.

---

## Setup

### Step 1 — Install Ollama

Ollama runs AI models locally on your Mac. Free, private, no account needed.

**Option A — Homebrew (recommended if you have it):**
```bash
brew install ollama
```

**Option B — Direct download:**
Go to [ollama.com/download](https://ollama.com/download) and download the Mac app. Open it and follow the installer.

### Step 2 — Download the Mistral model

```bash
ollama pull mistral
```

This downloads the model (~4GB) once. You only need to do this once.

### Step 3 — Start Ollama

```bash
ollama serve
```

Keep this running in a terminal tab while you use the workflow. If you installed the Mac app, it runs automatically in the menu bar.

### Step 4 — Set up the project

```bash
cp .env.example .env
pip install -r requirements.txt
```

The `.env` file already has `OPENAI_API_KEY=ollama` set — no changes needed.

---

## Usage

```bash
python run.py --theme food
python run.py --theme travel
python run.py --theme family --output ./my_output
```

List all available themes:
```bash
python run.py --list-themes
```

---

## Output structure

```
weekly_artifacts/
├── vocab_state.json        # tracks used vocabulary per theme
├── run_log.json            # tracks run history
├── week-01-food/
│   ├── flashcards.csv      # import into Anki
│   ├── passage.txt         # Italian reading passage
│   ├── passage_en.txt      # English translation
│   └── quiz.html           # open in any browser
└── week-02-travel/
    └── ...
```

Re-running the same theme creates a new folder (`week-02-food`, `week-03-food`, etc.) with fresh vocabulary.

---

## Adding themes

Edit `themes.yaml` and add a new entry:

```yaml
- id: music
  label: Music
  description: Instruments, listening, concerts, and Italian songs.
```

No code changes needed — the new theme is available immediately.

---

## Switching AI provider

Edit `config.yaml`. Options are documented inside the file:

| Provider | Cost | Notes |
|---|---|---|
| Ollama (default) | Free | Runs locally, no internet needed |
| OpenAI | ~$0.001/run | Requires API key from platform.openai.com |
| Google Gemini | Free tier | Requires key from aistudio.google.com |

---

## Requirements

- macOS with 8GB+ RAM (for Ollama)
- Python 3.10+
- Ollama installed and running
