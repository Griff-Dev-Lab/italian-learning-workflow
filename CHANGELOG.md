# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.2] - 2026-06-13

### Added — Gender/Number Agreement for Essere-Auxiliary Verbs

#### Grammatically Accurate Past Participles
- **Gender/number variants now displayed for essere-auxiliary verbs** — e.g., `"sono andato / andata"`, `"siamo andati / andate"`
- **Proper Italian grammar** — Past participles must agree with subject gender and number
- **Comprehensive coverage** — All 10 essere-auxiliary verbs properly implemented:
  - Core: `andare`, `venire`, `arrivare`, `partire`, `uscire`, `entrare`
  - Additional: `essere`, `stare`, `rimanere`, `tornare`
- **Singular forms (io, tu, lui/lei)** — Show m.s./f.s. variants (e.g., `stato / stata`)
- **Plural forms (noi, voi, loro)** — Show m.pl./f.pl. variants (e.g., `stati / state`)

#### Learning Benefits
- **Teaches proper agreement rules** — Essential for A1-A2 learners to understand gender/number concord
- **Anki-ready format** — Slash-separated format (`"stato / stata"`) displays perfectly in Anki cards
- **HTML table readability** — Conjugation tables render gender variants clearly
- **No usability impact** — Format works seamlessly across all builders (flashcard, table)

### Fixed

#### Archaic Form Quirk
- **Fixed `essuto` (archaic) for essere passato prossimo** → Now correctly shows `"stato / stata"` and `"stati / state"`
- **Root cause** — mlconjug3 library quirk; workaround implemented in verb conjugator

#### Gender/Number Agreement Bug
- **Gender agreement now properly implemented for all essere-auxiliary verbs**
- **Before:** Mixed inconsistent forms (e.g., `andate` instead of `andato`)
- **After:** Correct agreement for all 6 persons with both genders shown
- **Avere-auxiliary verbs:** Correctly show invariant forms (no gender agreement needed)

#### Definition Cards Format
- **Changed definition cards from Cloze to Basic format** — simpler and more reliable
- **Before:** `{{c1::mangiare}}` format showed raw syntax in Anki
- **After:** Plain Basic card format: Front `to eat`, Back `mangiare`
- **Import instruction:** Set field separator to **Comma** during Anki import
- **Result:** 57 definition cards for vocabulary learning work perfectly

### Technical Details

#### Modified Files
- `src/verb_conjugator.py`:
  - Updated `_extract_past_forms()` to handle gender/number agreement
  - Implemented special logic for 10 essere-auxiliary verbs
  - Proper masculine/feminine form generation with slash notation
  - Avere-auxiliary verbs continue to show invariant past participles
- `src/orchestrator.py`:
  - Updated `generate_definitions_batch()` to generate plain Basic format (no cloze syntax)
- Documentation:
  - `docs/ANKI_SETUP.md`: Added field separator guidance for definition cards import
  - `tech.md`, `structure.md`, `product.md`: Updated definition card format documentation

#### Compatibility
- ✅ **Flashcard builder** — Accepts slash-separated forms as-is, no changes needed
- ✅ **Conjugation table builder** — Renders forms exactly as provided, no changes needed
- ✅ **Anki import** — CSV format unchanged, slash notation displays perfectly
- ✅ **Backwards compatible** — Existing Anki decks continue to work

### Sample Output

**For `andare` (past tense):**
- io: `sono andato / andata`
- tu: `sei andato / andata`
- lui/lei: `è andato / andata`
- noi: `siamo andati / andate`
- voi: `siete andati / andate`
- loro: `sono andati / andate`

**For `mangiare` (past tense — avere auxiliary, no agreement):**
- io: `ho mangiato` (invariant, same for all genders)
- tu: `hai mangiato`
- lui/lei: `ha mangiato`
- noi: `abbiamo mangiato`
- voi: `avete mangiato`
- loro: `hanno mangiato`

### Accuracy & Validation

- ✅ **100% accuracy maintained** — mlconjug3 conjugations + manual gender/number agreement
- ✅ **Grammar verified** — All forms follow Italian grammar rules
- ✅ **Comprehensive testing** — All 57 A1-A2 verbs scanned and validated
- ✅ **No empty or malformed conjugations** — All persons show correct forms

---

## [1.3.1] - 2026-06-12

### Changed — Documentation & Specifications

#### Steering Documentation
- **`.kiro/steering/tech.md`** — Updated Anki CSV format descriptions for grid-based cloze and batch definitions
- **`.kiro/steering/structure.md`** — Updated project structure, card data models, and architecture patterns
- **`.kiro/steering/product.md`** — Already up-to-date with v1.3.0 features

#### Specification Files
- **`requirements.md`** — Updated glossary, requirements for grid-based cloze cards, batch definitions mode, English translations
- **`design.md`** — Updated architecture diagram, pipeline workflows, data models, interfaces, and correctness properties

#### Roadmap Refactor
- **`docs/ROADMAP.md`** — Refactored from version-specific (v1.3.0, v1.4.0, etc.) to **Now/Next/Later** format
  - **Now** — Current v1.3.0 features
  - **Next** — High-priority features (Extended CEFR levels, batch processing)
  - **Later** — Future exploration (LLM passages, customization, analytics, web/mobile)
  - Removed specific dates and version numbers for flexibility
  - More responsive to community feedback

### Benefits

- ✅ Steering docs and specs now fully synchronized with v1.3.0 implementation
- ✅ Roadmap is more flexible and maintainable
- ✅ No version drift or constant documentation updates needed
- ✅ Clear separation of current, near-term, and future work

### Technical Details

- No code changes
- Documentation and specification updates only
- All changes committed and ready for release

---

## [1.3.0] - 2026-06-11

### Added — Complete Learning System

#### Grid-Based Cloze Cards
- **Replaced sentence-based cloze with grid format** — Shows all 6 persons with one hidden form
- **Randomized hidden forms** — No two cards hide the same person across the 3 tenses
- **Pattern recognition focus** — Helps learners see conjugation patterns clearly
- **Reduced from 18 to 3 cloze cards per verb** — Higher quality, more focused learning

#### Explicit Italian Tense Names
- **Basic cards now show Italian tense names** — "Presente Indicativo", "Passato Prossimo", "Futuro Semplice"
- **More professional and educational** — Aligns with Italian grammar terminology
- **Helps learners understand proper tense names** — Essential for advanced learning

#### English Translations in HTML Tables
- **Conjugation table titles now include English translation** — e.g., "mangiare (to eat)"
- **Graceful fallback** — Shows just infinitive if verb not in translation list
- **100% offline** — No external APIs, pure data-driven approach

#### Batch Definitions Mode
- **New command: `python3 run.py --definitions-batch`** — Generate all 57 A1-A2 verb definitions at once
- **Single CSV file with 57 definition cloze cards** — Ready to import as separate Anki deck
- **Vocabulary learning pathway** — Complements conjugation cards perfectly
- **Extensible** — Works if users add more verbs to `verb_translations.json`

#### Extended A1-A2 Verb Coverage
- **57 verified Italian verbs** — Complete A1-A2 learning coverage
- **Organized by priority tier** — High-priority, Medium-priority, Lower-priority
- **Comprehensive verb_translations.json** — All 57 verbs with accurate English translations
- **Supports custom verbs** — Users can add their own verbs and translations

### Changed

#### Card Generation
- **Basic cards: 18 per verb** (unchanged, but with new tense names)
- **Cloze cards: 3 per verb** (reduced from 18, grid-based format)
- **Total per verb: 21 cards** (down from 36, higher quality)

#### Documentation
- **README.md** — Updated with new card types and batch definitions command
- **docs/ANKI_SETUP.md** — Added Step 8 for importing definition cards, reorganized best practices
- **docs/VERB_LIST.md** — Added vocabulary learning section, complete learning system overview

#### CLI
- **New flag: `--definitions-batch`** — Generate all definition cards at once
- **Updated help text** — Reflects new batch mode

### Fixed

- **Cloze card quality** — Grid format eliminates phrase memorization issues
- **Conjugation table accuracy** — Translations now verified and consistent
- **Verb extensibility** — Users can now add custom verbs with translations

### Technical Details

#### New Files
- `src/verb_translations.json` — 57 verified Italian verbs with English translations

#### Modified Files
- `src/flashcard_builder.py` — Grid-based cloze card generation with randomization
- `src/conjugation_table_builder.py` — Translation loading and display
- `src/orchestrator.py` — New `generate_definitions_batch()` method
- `run.py` — New `--definitions-batch` CLI flag

### Accuracy & Performance

- ✅ **100% accuracy maintained** — All conjugations via mlconjug3
- ✅ **No external dependencies** — Translations are local data, no APIs
- ✅ **Offline-first** — Works completely offline
- ✅ **Graceful degradation** — Unknown verbs still work, just without translations

### Learning Benefits

**Before v1.3.0:**
- 36 cards per verb (18 basic + 18 cloze)
- Sentence-based cloze cards (potential phrase memorization)
- No vocabulary learning pathway

**After v1.3.0:**
- 21 cards per verb (18 basic + 3 cloze grid)
- Grid-based cloze cards (pattern recognition focus)
- Separate vocabulary deck (57 definition cards)
- **Complete learning system** — Forms + Meanings + Patterns

### Migration Guide

**No breaking changes.** Existing workflows continue to work:

```bash
# Single verb (unchanged)
python3 run.py --verb mangiare --table

# New: Batch definitions (optional)
python3 run.py --definitions-batch
```

**For existing users:**
- Old cloze cards still work in Anki
- New grid-based cloze cards are higher quality
- Regenerate verbs with `--force` to get new format
- Import definitions deck separately

---

## [1.2.1] - 2026-06-10

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