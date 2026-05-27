# Product

Italian Learning Workflow is an Anki flashcard generator focused on Italian verb conjugation, targeting A1–A2 learners. Each run takes a single verb as input and produces ready-to-import Anki CSVs with 100% accuracy.

## Core Features — 100% LLM-Free

A single CLI run for one verb produces two types of cards:

**Basic cards** — one conjugated form per card, drills recall of a specific form:
- All 6 present tense forms (io, tu, lui/lei, noi, voi, loro) — one card each
- All 6 past tense forms (passato prossimo) — one card each
- All 6 future tense forms (futuro semplice) — one card each
- 18 cards per verb

**Cloze cards** — verb used in context with clear infinitive reference:
- Subject pronoun is always explicit so only one conjugation is correct
- Infinitive shown in parentheses: "(mangiare) Ogni giorno io _____"
- All 6 persons for present, past, and future tenses
- 18 cards per verb

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
python3 run.py --verb mangiare

# Generate flashcards + conjugation table
python3 run.py --verb mangiare --table

# Custom output directory
python3 run.py --verb mangiare --output ./my_output

# Force regeneration
python3 run.py --verb mangiare --force

# List processed verbs
python3 run.py --list-verbs
```

## Accuracy Guarantee

Every conjugation is verified by mlconjug3, the same library used by professional language tools. No more LLM errors like:
- ❌ "sono addormentato" (wrong reflexive forms)
- ❌ "ho andato" (wrong auxiliary verbs)
- ❌ Mixed languages or grammar mistakes

✅ Perfect Italian every time!

---

## Future Enhancements

### 🎓 Extended CEFR Level Support (B1, B2, C1, C2)
- Expand beyond A1–A2 to cover intermediate and advanced learners
- B1/B2: subjunctive mood (congiuntivo), conditional (condizionale), imperative (imperativo)
- C1/C2: all remaining moods and tenses (trapassato, futuro anteriore, congiuntivo trapassato)
- Level flag: `python3 run.py --verb mangiare --level B1`

### 📚 Extended Tenses and Moods
- Imperfetto (imperfect past) — essential for A2/B1 storytelling
- Condizionale presente (conditional) — "I would eat"
- Congiuntivo presente (subjunctive) — required for B2+
- Imperativo (imperative) — commands and requests

### 📖 LLM-Powered Reading Passages
- Optional `--passage` flag to generate contextual reading texts
- Support for local models via Ollama (free, offline)
- Support for API-driven models (OpenAI, Google Gemini)
- Passages built around the verb's conjugated forms for contextual reinforcement
- Configurable via `config.yaml` — switch provider without code changes
