# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-27

### Added
- **Verb-focused flashcard generation** - Generate Anki cards for individual Italian verbs
- **Dual card types** - Basic cards for conjugation drilling + Cloze cards for contextual learning
- **Comprehensive conjugation coverage** - 10 Basic cards per verb (6 present + 2 past + 2 future tense forms)
- **Contextual sentences** - 8 Cloze cards with semantically accurate example sentences
- **HTML example sentences** - Clean table format showing proper verb usage with translations
- **Conjugation verification** - mlconjug3 integration for accuracy checking with warning system
- **Duplicate prevention** - Vocab tracking prevents re-processing the same verb
- **Multi-provider LLM support** - Ollama (free, local), OpenAI, or Google Gemini
- **Structured prompt engineering** - Template-based sentence generation for grammatical accuracy
- **CLI interface** - Simple `python run.py --verb [infinitive]` command
- **Anki-ready output** - RFC 4180-compliant CSV files for direct import

### Technical Features
- **Local-first architecture** - Runs entirely offline with Ollama
- **Modular design** - Single-responsibility modules with custom exception handling
- **Type hints and documentation** - Full type annotations and docstrings
- **Configuration management** - YAML-based config with environment variable support
- **Atomic file operations** - Safe artifact writing with cleanup on failure

### Output Structure
```
verb_artifacts/
├── verb_log.json           # Run history tracking
└── {verb}/                 # One folder per verb
    ├── flashcards_basic.csv    # Basic note type for Anki
    ├── flashcards_cloze.csv    # Cloze note type for Anki  
    └── passage.html            # Example sentences
```

### Requirements
- macOS with 8GB+ RAM (for Ollama)
- Python 3.10+
- Ollama installed and running (or API key for OpenAI/Gemini)

### Dependencies
- `openai>=1.0.0` - LLM API client
- `pyyaml>=6.0` - Configuration file parsing
- `python-dotenv>=1.0` - Environment variable loading
- `mlconjug3>=3.8.0` - Italian verb conjugation verification