# Product

Italian Learning Workflow is an Anki flashcard generator focused on Italian verb conjugation, targeting A1–A2 learners. Each run takes a single verb as input and produces a ready-to-import Anki CSV.

## Phase 1 — Verb Generator

A single CLI run for one verb produces two types of cards, both in the same CSV output:

**Basic cards** — one conjugated form per card, drills recall of a specific form:
- All 6 present tense forms (io, tu, lui/lei, noi, voi, loro) — one card each
- Most common past tense forms (io, tu) using passato prossimo
- Most common future tense forms (io, tu) using futuro semplice
- ~10 cards per verb

**Cloze cards** — verb used in a sentence, one specific form blanked out:
- Subject pronoun is always explicit in the sentence so only one conjugation is correct
- Covers a spread of tenses and persons
- ~6 cards per verb

All cards go into a single **Verbs** deck.

## Optional Passage

Running with `--passage` generates a short HTML reading text built around the verb and its conjugated forms. The passage is a clean, readable HTML file — no markdown, no code fences — that opens directly in any browser.

## Key Constraints

- Phase 1 is verb-only — nouns and adjectives are out of scope for now
- Each card has exactly one correct answer
- Vocabulary tracking prevents the same verb being added twice across runs
- No quiz output — the HTML quiz has been removed
- Runs locally via Ollama (default) or any OpenAI-compatible provider

## CLI Usage

```bash
# Generate flashcards for a verb
python run.py --verb mangiare

# Generate flashcards + reading passage
python run.py --verb mangiare --passage

# Custom output directory
python run.py --verb mangiare --output ./my_output
```

## Future Phases (out of scope for now)
- Noun deck with cloze cards drilling articles
- Adjective deck with basic cards drilling agreement forms
- Multi-verb runs
