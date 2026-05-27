# Roadmap — Future Enhancements

The Italian Learning Workflow is actively evolving. Here's what's planned for future releases.

---

## 🎓 v1.3.0 — Extended CEFR Levels (B1, B2, C1, C2)

**Target:** Q3 2026

Expand beyond A1–A2 to support intermediate and advanced learners with additional tenses and moods.

### Features

- **`--level` flag** — Generate cards for specific CEFR levels
  ```bash
  python3 run.py --verb mangiare --level B1 --table
  ```

- **B1 Level** — Intermediate learner
  - Imperfetto (imperfect past) — "I was eating"
  - Condizionale presente (conditional) — "I would eat"
  - Imperativo (imperative) — Commands and requests

- **B2 Level** — Upper intermediate
  - Congiuntivo presente (subjunctive) — "I want you to eat"
  - Congiuntivo passato (past subjunctive)
  - Trapassato prossimo (pluperfect)

- **C1/C2 Levels** — Advanced
  - Congiuntivo imperfetto (imperfect subjunctive)
  - Futuro anteriore (future perfect)
  - Congiuntivo trapassato (past perfect subjunctive)
  - All remaining moods and tenses

### Card Generation

- **B1:** ~30 cards per verb (present + past + future + conditional + imperative)
- **B2:** ~40 cards per verb (adds subjunctive forms)
- **C1/C2:** ~50+ cards per verb (complete conjugation coverage)

### Conjugation Table

- HTML tables will expand to show all tenses for the selected level
- Organized by mood (indicative, conditional, subjunctive, imperative)

---

## 📖 v1.4.0 — LLM-Powered Reading Passages

**Target:** Q4 2026

Generate contextual reading texts built around verb conjugations for immersive learning.

### Features

- **`--passage` flag** — Generate reading passages
  ```bash
  python3 run.py --verb mangiare --passage --model ollama
  ```

- **Local Models** — Via Ollama (free, fully offline)
  - Download models: `ollama pull mistral`, `ollama pull llama2`
  - No API keys required
  - Complete privacy

- **API-Driven Models** — Via OpenAI or Google Gemini
  - Optional for users who prefer cloud models
  - Configurable via `config.yaml`
  - Switch providers without code changes

- **Passage Features**
  - A1–A2 level: Simple, present-tense narratives
  - B1+ level: Complex stories with multiple tenses
  - All passages use verified mlconjug3 conjugations
  - LLM only writes prose, never conjugates verbs

### Output

- **`passage.txt`** — Plain text reading passage
- **`passage_with_blanks.txt`** — Cloze-style passage for self-testing
- **`passage_vocabulary.csv`** — New vocabulary introduced

### Example

```
Input:  python3 run.py --verb mangiare --passage
Output: 
  - passage.txt (500 words about eating in Italy)
  - passage_with_blanks.txt (same passage with verbs blanked)
  - passage_vocabulary.csv (new words to learn)
```

---

## 🎯 v1.5.0 — Batch Processing & Automation

**Target:** Q1 2027

Generate flashcards for multiple verbs in a single command.

### Features

- **Batch mode** — Process multiple verbs at once
  ```bash
  python3 run.py --batch tier1 --table
  python3 run.py --batch tier2 --table
  python3 run.py --batch custom.txt --table
  ```

- **Predefined batches**
  - `--batch tier1` — All 10 core verbs
  - `--batch tier2` — All 10 everyday verbs
  - `--batch tier3` — All 10 descriptive verbs
  - `--batch all` — All 30 verbs

- **Custom batch files**
  ```
  # my_verbs.txt
  mangiare
  dormire
  andare
  ```

- **Progress tracking**
  - Real-time progress bar
  - Estimated time remaining
  - Summary report at end

### Output

- Single Anki deck with all verbs
- Combined conjugation table (all verbs)
- Batch report (cards generated, time taken, etc.)

---

## 🔧 v1.6.0 — Customization & Templates

**Target:** Q2 2027

Allow users to customize sentence templates and card formats.

### Features

- **Custom templates** — User-defined cloze sentences
  ```yaml
  # config.yaml
  templates:
    present:
      - "({{verb}}) {{subject}} {{verb_form}} ogni giorno."
      - "({{verb}}) {{subject}} {{verb_form}} spesso?"
  ```

- **Custom card formats**
  - Add pronunciation (IPA)
  - Add English translations
  - Add example images
  - Custom styling

- **Template library**
  - Community-contributed templates
  - Downloadable from GitHub
  - Easy to share and reuse

---

## 📊 v1.7.0 — Analytics & Learning Insights

**Target:** Q3 2027

Track learning progress and provide personalized recommendations.

### Features

- **Learning dashboard**
  - Cards studied per day
  - Retention rate by tense
  - Weak verbs (low retention)
  - Strong verbs (high retention)

- **Recommendations**
  - "You're struggling with subjunctive — here are 5 verbs to focus on"
  - "You've mastered Tier 1 — ready for Tier 2?"
  - "Review these 3 verbs before moving forward"

- **Export reports**
  - PDF learning summary
  - CSV data for analysis
  - Shareable progress badges

---

## 🌍 v2.0.0 — Web Interface & Mobile App

**Target:** 2028

Bring the workflow to the web and mobile platforms.

### Features

- **Web interface**
  - Generate flashcards without CLI
  - Browse verb library
  - Preview cards before import
  - Manage multiple decks

- **Mobile app** (iOS/Android)
  - Offline flashcard review
  - Sync with Anki
  - Spaced repetition algorithm
  - Progress tracking

- **Cloud sync**
  - Save preferences across devices
  - Backup decks to cloud
  - Share decks with friends

---

## 🎓 Ongoing Improvements

### Quality & Accuracy
- ✅ Continuous mlconjug3 updates
- ✅ Community feedback integration
- ✅ Bug fixes and performance improvements

### Documentation
- ✅ Video tutorials
- ✅ Interactive guides
- ✅ Community wiki

### Community
- ✅ GitHub discussions
- ✅ Discord community
- ✅ Contribution guidelines

---

## How to Contribute

Interested in helping? Here's how:

1. **Report bugs** — GitHub Issues
2. **Suggest features** — GitHub Discussions
3. **Contribute code** — Pull Requests (see CONTRIBUTING.md)
4. **Share templates** — Community templates repo
5. **Translate** — Help localize for other languages

---

## Timeline Summary

| Version | Release | Focus |
|---------|---------|-------|
| v1.2.0 | May 2026 | ✅ Complete conjugation coverage |
| v1.3.0 | Q3 2026 | Extended CEFR levels (B1–C2) |
| v1.4.0 | Q4 2026 | LLM-powered reading passages |
| v1.5.0 | Q1 2027 | Batch processing & automation |
| v1.6.0 | Q2 2027 | Customization & templates |
| v1.7.0 | Q3 2027 | Analytics & learning insights |
| v2.0.0 | 2028 | Web & mobile platforms |

---

## Feedback

Have ideas for the roadmap? Let us know!

- **GitHub Issues** — Bug reports and feature requests
- **GitHub Discussions** — Ideas and feedback
- **Email** — Direct feedback (see README)

---

**Thank you for using Italian Learning Workflow! 🇮🇹**
