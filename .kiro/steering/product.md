# Product

Italian Learning Workflow is an Anki flashcard generator focused on Italian verb conjugation, targeting A1–A2 learners. Each run takes a single verb as input and produces ready-to-import Anki CSVs with 100% accuracy.

## Core Features — 100% LLM-Free

A single CLI run for one verb produces three types of cards:

**Basic cards** — one conjugated form per card, drills recall of a specific form:
- All 6 present tense forms (io, tu, lui/lei, noi, voi, loro) — one card each
- All 6 past tense forms (passato prossimo) — one card each
  - **Gender/number agreement shown for essere-auxiliary verbs** (andare, venire, etc.)
  - **Invariant forms for avere-auxiliary verbs** (mangiare, dormire, etc.)
- All 6 future tense forms (futuro semplice) — one card each
- Explicit Italian tense names (Presente Indicativo, Passato Prossimo, Futuro Semplice)
- 18 cards per verb

**Cloze grid cards** — all 6 persons in grid format with one hidden form:
- Grid showing all 6 persons with one form hidden as cloze
- Randomized hidden form (no two cards hide the same person)
- One card per tense (Presente, Passato, Futuro)
- Tests pattern recognition and conjugation accuracy
- 3 cards per verb

**Definition cards** — vocabulary learning (batch mode):
- Generate all 57 A1-A2 verb definitions at once with `--definitions-batch`
- One cloze card per verb: `{{c1::mangiare}}` → `to eat`
- Import as separate "Italian Verbs — Definitions" deck
- 57 cards total (one-time generation)

All cards go into **two decks**:
- **Italian Verbs** — Conjugation drilling and pattern recognition
- **Italian Verbs — Definitions** — Vocabulary learning

## Complete Learning System

Three complementary card types for comprehensive learning:

| Card Type | Purpose | Count | Deck |
|-----------|---------|-------|------|
| **Basic** | Conjugation recall | 18/verb | Italian Verbs |
| **Cloze Grid** | Pattern recognition | 3/verb | Italian Verbs |
| **Definition** | Vocabulary | 1/verb | Italian Verbs — Definitions |

**Total: 1,254 cards for 57 A1-A2 verbs**

## Optional Conjugation Table

Running with `--table` generates a beautiful HTML conjugation reference table showing all forms in a clean, printable format. Includes English translation in the title (e.g., "mangiare (to eat)"). Perfect for study and review.

## Extended A1-A2 Coverage

57 verified Italian verbs organized by priority:
- **Tier 1:** Core 10 (essere, avere, fare, andare, dire, potere, volere, dovere, sapere, stare)
- **Tier 2:** High-frequency 10 (mangiare, bere, venire, uscire, prendere, mettere, dare, vedere, guardare, parlare)
- **Tier 3:** Life/work 10 (vivere, abitare, lavorare, trovare, sentire, chiedere, arrivare, partire, comprare, capire)
- **High-priority 4:** (piacere, rimanere, tornare, passare)
- **Medium-priority 13:** (entrare, portare, lasciare, seguire, tenere, aprire, chiudere, correre, camminare, nuotare, studiare, giocare, suonare)
- **Lower-priority 10:** (spedire, preferire, pulire, costare, viaggiare, descrivere, decidere, provare, ricordare, dimenticare)

## Key Benefits

- **100% Accurate**: Uses mlconjug3 linguistic library for perfect conjugations
- **LLM-Free**: No API keys, internet, or AI services required
- **Offline Ready**: Works completely offline
- **Handles All Verbs**: Regular, irregular, avere/essere auxiliaries
- **Complete Learning System**: Conjugations + Vocabulary + Pattern Recognition
- **Fast Generation**: No API calls needed
- **Extensible**: Users can add custom verbs and translations

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

# Generate definition cloze cards for all 57 A1-A2 verbs
python3 run.py --definitions-batch

# Generate definitions to custom output directory
python3 run.py --definitions-batch --output ./my_output
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

### 🔧 Batch Processing & Automation
- Generate flashcards for multiple verbs in a single command
- Predefined batches (tier1, tier2, tier3, all)
- Custom batch files

### 🌍 Web & Mobile Platforms
- Web interface for flashcard generation
- Mobile app for offline review
- Cloud sync across devices
