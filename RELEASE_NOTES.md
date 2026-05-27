# Release Notes — v1.2.1

**Release Date:** June 10, 2026

## Overview

v1.2.1 adds **comprehensive documentation** to help users get started quickly and understand the project's future direction. This release includes step-by-step Anki setup guides, a curated verb learning list, and a detailed roadmap for upcoming features.

---

## What's New

### 📚 Comprehensive Documentation Structure

New `docs/` directory with organized, user-facing guides:

**[docs/README.md](docs/README.md)** — Documentation Index
- Quick links to all guides
- Learning path overview
- Getting started checklist

**[docs/ANKI_SETUP.md](docs/ANKI_SETUP.md)** — Complete Anki Import Guide
- 6-step setup process with detailed instructions
- Screenshots and descriptions for each step
- Troubleshooting section covering common issues
- Best practices for effective learning
- Mobile sync instructions (AnkiWeb, AnkiDroid)

**[docs/VERB_LIST.md](docs/VERB_LIST.md)** — Top 30 Essential Verbs
- Organized by learning tier (Tier 1, 2, 3)
- **Tier 1:** Core 10 verbs (essere, avere, fare, andare, dire, potere, volere, dovere, sapere, stare)
- **Tier 2:** High-frequency 10 verbs (mangiare, bere, venire, uscire, prendere, mettere, dare, vedere, guardare, parlare)
- **Tier 3:** Life/work 10 verbs (vivere, abitare, lavorare, trovare, sentire, chiedere, arrivare, partire, comprare, capire)
- Ready-to-copy CLI commands for each verb
- 6-week learning strategy with phase breakdown

**[docs/ROADMAP.md](docs/ROADMAP.md)** — Feature Roadmap
- Detailed plans for v1.3.0–v2.0.0
- **v1.3.0:** Extended CEFR levels (B1, B2, C1, C2)
- **v1.4.0:** LLM-powered reading passages (Ollama, OpenAI, Google Gemini)
- **v1.5.0:** Batch processing & automation
- **v1.6.0:** Customization & templates
- **v1.7.0:** Analytics & learning insights
- **v2.0.0:** Web interface & mobile app
- Timeline summary and contribution guidelines

### 📖 Documentation Reorganization

**Main README.md:**
- Simplified to focus on quick start
- Links to comprehensive guides in `docs/`
- Cleaner structure for new users

### 🎯 User Experience Improvements

- **Clearer learning path** — Tier-based verb list guides progression
- **Better onboarding** — Step-by-step Anki setup removes friction
- **Transparency** — Roadmap shows project direction and timeline
- **Community engagement** — Contribution guidelines and feedback channels

---

## Breaking Changes

⚠️ **None** — This is a documentation-only release. All code remains unchanged from v1.2.0.

---

## What's Included

### Files Added
- `docs/README.md` — Documentation index
- `docs/ANKI_SETUP.md` — Anki import guide
- `docs/ROADMAP.md` — Feature roadmap
- `docs/VERB_LIST.md` — Verb learning list

### Files Updated
- `README.md` — Simplified with links to docs

### Code
- No code changes (v1.2.0 functionality unchanged)

---

## Migration Guide

No migration needed. This is a documentation release.

If you're upgrading from v1.2.0:
1. Pull the latest code
2. Check out the new guides in `docs/`
3. Use [docs/VERB_LIST.md](docs/VERB_LIST.md) to plan your learning
4. Follow [docs/ANKI_SETUP.md](docs/ANKI_SETUP.md) for Anki setup

---

## Known Limitations

- Documentation is English-only (future versions may add translations)
- Roadmap dates are estimates and subject to change
- Some planned features (v1.4.0+) are not yet implemented

---

## What's Next

### Planned for v1.3.0 (Q3 2026)

- **Extended CEFR Levels** — Support for B1, B2, C1, C2 with additional tenses
  - Imperfetto (imperfect past)
  - Condizionale (conditional)
  - Congiuntivo (subjunctive)
  - Imperativo (imperative)
- **`--level` flag** — Generate cards for specific CEFR levels
- **Expanded conjugation tables** — Show all tenses organized by mood

### Planned for v1.4.0 (Q4 2026)

- **LLM-Powered Reading Passages** — Optional `--passage` flag
- **Local models via Ollama** — Free, fully offline
- **API-driven models** — OpenAI, Google Gemini support
- **Configurable via `config.yaml`** — Switch providers without code changes

See [docs/ROADMAP.md](docs/ROADMAP.md) for complete details.

---

## Contributors

- Andrew Griffith (@Griff-Dev-Lab)

---

## Support

For issues, feature requests, or questions:
- GitHub Issues: [italian-learning-workflow/issues](https://github.com/Griff-Dev-Lab/italian-learning-workflow/issues)
- GitHub Discussions: [italian-learning-workflow/discussions](https://github.com/Griff-Dev-Lab/italian-learning-workflow/discussions)
- Documentation: [docs/README.md](docs/README.md)

---

## Changelog

### v1.2.1 (June 10, 2026)
- 📚 Add comprehensive documentation structure in `docs/` directory
- 📖 Add Anki setup guide with 6-step import process and troubleshooting
- 🎯 Add verb learning list with 30 essential verbs organized by tier
- 🗺️ Add detailed roadmap for v1.3.0–v2.0.0
- 📝 Simplify main README with links to comprehensive guides

### v1.2.0 (May 27, 2026)
- ✨ Expand to all 6 persons for past and future tenses (18 basic + 18 cloze cards per verb)
- 📖 Add comprehensive Anki setup guide to README
- 🔧 Update conjugation extraction methods for complete coverage
- 📝 Update all specs and documentation

### v1.1.0 (Previous)
- Remove LLM dependency, use mlconjug3 as sole source
- Add HTML conjugation table generation
- Implement duplicate verb prevention
- 100% accurate conjugations

---

**Thank you for using Italian Learning Workflow! Happy studying! 🇮🇹**

# Release Notes — v1.2.0

**Release Date:** May 27, 2026

## Overview

v1.2.0 expands the Italian Learning Workflow to generate **comprehensive conjugation coverage** with all 6 persons (io, tu, lui/lei, noi, voi, loro) for present, past, and future tenses. This release doubles the card count per verb and adds a detailed Anki setup guide for new users.

---

## What's New

### 🎯 Expanded Card Generation

**Before (v1.1.0):**
- 10 basic cards per verb (6 present + 2 past + 2 future)
- 8 cloze cards per verb (4 present + 2 past + 2 future)
- **Total: 18 cards per verb**

**After (v1.2.0):**
- 18 basic cards per verb (6 present + 6 past + 6 future)
- 18 cloze cards per verb (6 present + 6 past + 6 future)
- **Total: 36 cards per verb** ✨

### 📚 Complete Conjugation Coverage

All 6 persons now covered for every tense:

**Present Tense (Presente Indicativo):**
- io, tu, lui/lei, noi, voi, loro

**Past Tense (Passato Prossimo):**
- io, tu, lui/lei, noi, voi, loro
- Correct auxiliary verbs (avere/essere) for all persons

**Future Tense (Futuro Semplice):**
- io, tu, lui/lei, noi, voi, loro

### 📖 Comprehensive Anki Setup Guide

New step-by-step guide in README covering:
1. Downloading Anki Desktop
2. Creating a deck
3. Importing basic flashcards (with note type selection)
4. Importing cloze flashcards (with HTML field configuration)
5. Reviewing cards
6. Optional AnkiWeb sync for mobile access

### 🔧 Code Improvements

**`verb_conjugator.py`:**
- New `_get_auxiliary_verb_all_forms()` method for all 6 persons
- Updated `_extract_past_forms()` to extract all 6 forms from mlconjug3
- Updated `_extract_future_forms()` to extract all 6 forms
- Updated `_fallback_past_forms()` and `_fallback_future_forms()` with complete conjugation patterns
- Expanded `_generate_cloze_sentences()` from 8 to 18 templates

**`flashcard_builder.py`:**
- Updated `build_basic()` to generate 18 rows (was 10)
- Removed CSV header rows (Anki imports data rows only)

**`conjugation_table_builder.py`:**
- Updated HTML table to display all 6 forms for past and future tenses
- Consistent layout with present tense section

### 📝 Documentation Updates

**README.md:**
- Updated card counts (10/8 → 18/18)
- Added 6-step Anki import guide with screenshots/descriptions
- Updated CLI examples to use `python3`

**Specs:**
- `requirements.md` — Updated Requirement 1 to specify 18 cards per type
- `design.md` — Updated architecture, data models, cloze templates, and correctness properties
- `product.md` — Updated feature descriptions
- `tech.md` — Updated CLI examples

---

## Breaking Changes

⚠️ **None** — This is a backward-compatible release. Existing workflows continue to work unchanged.

---

## Migration Guide

No migration needed. Simply update to v1.2.0 and run:

```bash
python3 run.py --verb mangiare --table
```

You'll now get 36 cards instead of 18 for each verb.

---

## Technical Details

### Conjugation Accuracy

All conjugations remain **100% accurate** via mlconjug3:
- ✅ Regular verbs (mangiare, dormire, partire)
- ✅ Irregular verbs (andare, venire, fare, dire)
- ✅ Correct auxiliary verbs (avere vs essere)
- ✅ All 6 persons for all tenses

### Performance

No performance impact. Generation time remains <1 second per verb.

### Compatibility

- Python 3.10+
- mlconjug3 ≥ 3.8.0
- pyyaml ≥ 6.0
- macOS, Linux, Windows

---

## Known Limitations

- Cloze cards use simple A1–A2 level sentence templates (future versions may add B1+ complexity)
- HTML conjugation table shows present, past, and future only (future versions may add subjunctive, conditional, etc.)
- No LLM-powered reading passages yet (planned for future release)

---

## What's Next

### Planned for v1.3.0+

- **Extended CEFR Levels** — Support for B1, B2, C1, C2 with additional tenses (imperfetto, condizionale, congiuntivo, imperativo)
- **LLM-Powered Reading Passages** — Optional `--passage` flag with Ollama/OpenAI support
- **Customizable Templates** — User-defined cloze sentence templates
- **Batch Processing** — Generate cards for multiple verbs in one run

---

## Contributors

- Andrew Griffith (@Griff-Dev-Lab)

---

## Support

For issues, feature requests, or questions:
- GitHub Issues: [italian-learning-workflow/issues](https://github.com/Griff-Dev-Lab/italian-learning-workflow/issues)
- Documentation: [README.md](README.md)

---

## Changelog

### v1.2.0 (May 27, 2026)
- ✨ Expand to all 6 persons for past and future tenses (18 basic + 18 cloze cards per verb)
- 📖 Add comprehensive Anki setup guide to README
- 🔧 Update conjugation extraction methods for complete coverage
- 📝 Update all specs and documentation
- 🐛 Remove CSV header rows (Anki compatibility fix)

### v1.1.0 (Previous)
- Remove LLM dependency, use mlconjug3 as sole source
- Add HTML conjugation table generation
- Implement duplicate verb prevention
- 100% accurate conjugations

---

**Thank you for using Italian Learning Workflow! Happy studying! 🇮🇹**
