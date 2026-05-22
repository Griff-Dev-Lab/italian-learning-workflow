# Product

Italian Learning Workflow is a weekly content generator for A1-level Italian learners. Each run produces three learning artifacts for a chosen theme (e.g. food, travel, family):

- **Anki flashcard CSV** — 10 cards: 2 verbs × 3 tenses (present/past/future) + 2 nouns + 2 adjectives
- **Reading passage** — 150–200 word Italian text plus an English translation
- **Offline HTML quiz** — Duolingo-style multiple-choice, runs in any browser without internet

The tool runs entirely locally via Ollama (default) but can be switched to OpenAI or Google Gemini by editing `config.yaml`. No API key is required for the default Ollama setup.

## Key Constraints

- All generated content must be A1-level Italian — simple, everyday vocabulary only
- Vocabulary is tracked across runs per theme to avoid word reuse (`vocab_state.json`)
- Adding a new theme requires only editing `themes.yaml` — no code changes
- The workflow is a single CLI command: `python run.py --theme <name>`
