# Roadmap — Future Enhancements

The Italian Learning Workflow is actively evolving. This roadmap outlines our vision using a flexible **Now / Next / Later** framework that adapts to community feedback and priorities.

---

## 🎯 Now — Current Focus

### ✅ Complete Learning System (v1.3.0)
- Grid-based cloze cards (3 per verb, pattern recognition focus)
- Batch definitions mode (57 A1-A2 verb vocabulary deck)
- English translations in HTML conjugation tables
- Explicit Italian tense names (Presente Indicativo, Passato Prossimo, Futuro Semplice)
- Extended A1-A2 coverage (57 verified verbs)

### 🔄 Ongoing
- Bug fixes and performance improvements
- Community feedback integration
- Documentation updates
- mlconjug3 library updates

---

## 🚀 Next — High Priority

### Extended CEFR Levels (B1, B2, C1, C2)

Expand beyond A1–A2 to support intermediate and advanced learners.

**Features:**
- `--level` flag for CEFR-specific generation
  ```bash
  python3 run.py --verb mangiare --level B1 --table
  ```

- **B1 Level** — Intermediate learner
  - Imperfetto (imperfect past)
  - Condizionale presente (conditional)
  - Imperativo (imperative)

- **B2 Level** — Upper intermediate
  - Congiuntivo presente (subjunctive)
  - Congiuntivo passato (past subjunctive)
  - Trapassato prossimo (pluperfect)

- **C1/C2 Levels** — Advanced
  - Congiuntivo imperfetto (imperfect subjunctive)
  - Futuro anteriore (future perfect)
  - Congiuntivo trapassato (past perfect subjunctive)

**Card Generation:**
- B1: ~30 cards per verb
- B2: ~40 cards per verb
- C1/C2: ~50+ cards per verb

**HTML Tables:**
- Organized by mood (indicative, conditional, subjunctive, imperative)
- All tenses for selected level

---

### Batch Processing & Automation

Generate flashcards for multiple verbs in a single command.

**Features:**
```bash
python3 run.py --batch tier1 --table
python3 run.py --batch custom.txt --table
```

- Predefined batches (tier1, tier2, tier3, all)
- Custom batch files
- Progress tracking with real-time updates
- Combined Anki deck output

---

## 💡 Later — Future Exploration

### LLM-Powered Reading Passages

Generate contextual reading texts built around verb conjugations.

**Concept:**
- `--passage` flag for reading generation
- Local models via Ollama (free, offline)
- API-driven models (OpenAI, Google Gemini)
- Passages use verified mlconjug3 conjugations
- LLM writes prose only, never conjugates

**Output:**
- Plain text passage
- Cloze-style passage for self-testing
- Vocabulary list

---

### Customization & Templates

Allow users to customize sentence templates and card formats.

**Concept:**
- User-defined cloze sentence templates
- Custom card formats (pronunciation, translations, images)
- Community template library
- Easy sharing and reuse

---

### Analytics & Learning Insights

Track learning progress and provide personalized recommendations.

**Concept:**
- Learning dashboard (cards studied, retention rates)
- Weak/strong verb identification
- Personalized recommendations
- Export reports (PDF, CSV)

---

### Web Interface & Mobile App

Bring the workflow to web and mobile platforms.

**Concept:**
- Web UI for flashcard generation
- Mobile app for offline review
- Cloud sync across devices
- Anki integration

---

## 🎓 Ongoing Improvements

### Quality & Accuracy
- Continuous mlconjug3 updates
- Community feedback integration
- Bug fixes and performance improvements

### Documentation
- Video tutorials
- Interactive guides
- Community wiki

### Community
- GitHub discussions
- Discord community
- Contribution guidelines

---

## How to Contribute

Interested in helping? Here's how:

1. **Report bugs** — [GitHub Issues](https://github.com/Griff-Dev-Lab/italian-learning-workflow/issues)
2. **Suggest features** — [GitHub Discussions](https://github.com/Griff-Dev-Lab/italian-learning-workflow/discussions)
3. **Contribute code** — Pull Requests (see CONTRIBUTING.md)
4. **Share templates** — Community templates repo
5. **Translate** — Help localize for other languages

---

## Feedback

Have ideas for the roadmap? Let us know!

- **GitHub Issues** — Bug reports and feature requests
- **GitHub Discussions** — Ideas and feedback
- **Email** — Direct feedback (see README)

---

## Framework Notes

This roadmap uses a **Now / Next / Later** structure to remain flexible and responsive to community needs:

- **Now** — Currently implemented or actively being worked on
- **Next** — High-priority features planned for near-term development
- **Later** — Future exploration, subject to community feedback and priorities

This approach allows us to adapt timelines based on user feedback without constantly updating version numbers and dates.

---

**Thank you for using Italian Learning Workflow! 🇮🇹**
