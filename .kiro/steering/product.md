# Product

Italian Learning Workflow is an Anki flashcard generator focused on Italian verb conjugation, targeting A1–A2 learners. Each run takes a single verb as input and produces ready-to-import Anki CSVs with 100% accuracy.

## Core Features — 100% LLM-Free

A single CLI run for one verb produces two types of cards:

**Basic cards** — one conjugated form per card, drills recall of a specific form:
- All 6 present tense forms (io, tu, lui/lei, noi, voi, loro) — one card each
- Most common past tense forms (io, tu) using passato prossimo
- Most common future tense forms (io, tu) using futuro semplice
- ~10 cards per verb

**Cloze cards** — verb used in context with clear infinitive reference:
- Subject pronoun is always explicit so only one conjugation is correct
- Infinitive shown in parentheses: "(mangiare) Ogni giorno io _____"
- Covers a spread of tenses and persons
- ~8 cards per verb

All cards go into a single **Verbs** deck.

## Optional Conjugation Table

Running with `--table` generates a beautiful HTML conjugation reference table showing all forms in a clean, printable format. Perfect for study and review.

## Key Benefits

- **100% Accurate**: Uses mlconjug3 linguistic library for perfect conjugations
- **LLM-Free**: No API keys, internet, or AI services required
- **Offline Ready**: Works completely offline
- **Handles All Verbs**: Regular, irregular, avere/essere auxiliaries
- **Clear Context**: Cloze cards show infinitive to eliminate ambiguity
- **Fast Generation**: No API calls needed

## CLI Usage

```bash
# Generate flashcards for a verb
python run.py --verb mangiare

# Generate flashcards + conjugation table
python run.py --verb mangiare --table

# Custom output directory
python run.py --verb mangiare --output ./my_output

# Force regeneration
python run.py --verb mangiare --force

# List processed verbs
python run.py --list-verbs
```

## Accuracy Guarantee

Every conjugation is verified by mlconjug3, the same library used by professional language tools. No more LLM errors like:
- ❌ "sono addormentato" (wrong reflexive forms)
- ❌ "ho andato" (wrong auxiliary verbs)
- ❌ Mixed languages or grammar mistakes

✅ Perfect Italian every time!
