# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-05-27

### Changed — Major Accuracy Overhaul
- **Removed all LLM dependencies** — conjugations now powered entirely by mlconjug3
- **Replaced passage builder with conjugation table** — 100% accurate HTML reference tables via `--table` flag
- **Template-based cloze sentences** — deterministic, grammatically perfect sentence generation
- **Cloze cards now show infinitive context** — format: `(mangiare) Ogni giorno io _____`
- **Correct auxiliary verbs** — avere vs essere handled accurately for all verbs
- **Simplified CLI** — removed `--passage` flag, added `--table` flag

### Removed
- `src/passage_builder.py` — LLM-generated passages were inaccurate, removed entirely
- `src/llm_client.py` — no LLM dependencies remain in the project
- `.env` / `.env.example` — no API keys needed
- LLM provider config from `config.yaml`
- `openai`, `python-dotenv` from `requirements.txt`

### Added
- `src/conjugation_table_builder.py` — generates beautiful HTML conjugation reference tables
- `--table` CLI flag — optional conjugation table output

### Fixed
- Present tense forms now always use simple present (dormo, not sono addormentato)
- Past tense auxiliary verbs now correct (ho dormito, not sono dormito)
- Future tense forms now use futuro semplice (dormirò, not sarò dormito)
- Cloze sentences now 100% Italian with no mixed languages

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

### Dependencies
- `openai>=1.0.0` - LLM API client
- `pyyaml>=6.0` - Configuration file parsing
- `python-dotenv>=1.0` - Environment variable loading
- `mlconjug3>=3.8.0` - Italian verb conjugation verification