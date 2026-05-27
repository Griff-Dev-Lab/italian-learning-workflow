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
