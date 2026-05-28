# Requirements Document

## Introduction

The Italian Learning Workflow is a CLI tool for A1–A2 Italian learners that generates Anki-ready flashcard CSVs and optional conjugation reference tables for any Italian verb. All content is generated using the mlconjug3 linguistic library — no LLM, no internet connection, and no API keys are required. The tool produces 100% accurate Italian conjugations every time.

## Glossary

- **Verb**: An Italian verb infinitive provided by the user (e.g. `mangiare`, `dormire`, `andare`).
- **Conjugation**: The inflected forms of a verb across persons and tenses.
- **Basic Card**: An Anki flashcard with a prompt on the front (e.g. `mangiare (io, Presente Indicativo)`) and the conjugated form on the back (e.g. `mangio`).
- **Cloze Grid Card**: An Anki flashcard displaying all 6 persons in a grid format with one conjugated form hidden as `{{c1::form}}` for the learner to fill in.
- **Definition Card**: An Anki cloze card for vocabulary learning (e.g. `{{c1::mangiare}}` → `to eat`).
- **Conjugation Table**: An HTML file showing all conjugated forms for a verb in a clean reference layout with English translation in the title.
- **Verb Folder**: A directory named after the verb (e.g. `verb_artifacts/mangiare/`) that stores all generated artifacts.
- **mlconjug3**: A Python linguistic library providing accurate Italian verb conjugations.
- **Passato Prossimo**: Italian compound past tense (e.g. `ho mangiato`, `sono andato`).
- **Futuro Semplice**: Italian simple future tense (e.g. `mangerò`, `dormirò`).
- **Presente Indicativo**: Italian simple present tense (e.g. `mangio`, `dormo`).
- **Avere/Essere**: The two Italian auxiliary verbs used in passato prossimo — most verbs use `avere`, motion/state verbs use `essere`.
- **A1–A2 Verbs**: 57 verified Italian verbs covering beginner to elementary proficiency levels.

---

## Requirements

### Requirement 1: Verb Flashcard Generation

**User Story:** As a language learner, I want to generate Anki flashcards for any Italian verb, so that I can drill conjugation forms using spaced repetition.

#### Acceptance Criteria

1. WHEN the workflow is executed with a verb infinitive, THE Workflow SHALL generate two CSV files: `flashcards_basic.csv` and `flashcards_cloze.csv`.
2. THE `flashcards_basic.csv` SHALL contain exactly 18 rows: 6 present tense forms (io, tu, lui/lei, noi, voi, loro), 6 passato prossimo forms (io, tu, lui/lei, noi, voi, loro), and 6 futuro semplice forms (io, tu, lui/lei, noi, voi, loro).
3. THE `flashcards_cloze.csv` SHALL contain exactly 18 rows covering all 6 persons across present, past, and future tenses.
4. ALL conjugated forms SHALL be sourced from the mlconjug3 library — no LLM or external API calls.
5. THE Workflow SHALL work for any valid Italian verb infinitive including irregular verbs (essere, avere, andare, venire, etc.).
6. THE Workflow SHALL correctly select the auxiliary verb (avere or essere) for passato prossimo forms.

---

### Requirement 2: Basic Flashcard Format

**User Story:** As a language learner, I want Basic flashcards that drill individual conjugated forms, so that I can memorise each form in isolation.

#### Acceptance Criteria

1. EACH Basic card front SHALL follow the format: `{infinitive} ({person}, {tense})` — e.g. `mangiare (io, Presente Indicativo)`.
2. THE tense names SHALL be explicit Italian names: `Presente Indicativo`, `Passato Prossimo`, `Futuro Semplice`.
3. EACH Basic card back SHALL contain only the conjugated form — e.g. `mangio`.
4. THE `flashcards_basic.csv` SHALL use columns: `front`, `back`.
5. THE file SHALL use UTF-8 encoding to support Italian diacritical characters (è, à, ò, ù, ì, etc.).
6. THE file SHALL conform to RFC 4180 CSV formatting.

---

### Requirement 3: Cloze Grid Flashcard Format

**User Story:** As a language learner, I want Cloze Grid flashcards that test pattern recognition and conjugation accuracy, so that I can learn all forms in context without memorizing phrases.

#### Acceptance Criteria

1. THE `flashcards_cloze.csv` SHALL contain exactly 3 rows per verb: one for Presente Indicativo, one for Passato Prossimo, one for Futuro Semplice.
2. EACH Cloze Grid card `text` field SHALL display an HTML grid showing all 6 persons (io, tu, lui/lei, noi, voi, loro) with one conjugated form hidden as `{{c1::form}}`.
3. THE hidden form SHALL be randomized across the 3 cards — no two cards SHALL hide the same person.
4. EACH Cloze Grid card `extra` field SHALL display the complete grid with all forms revealed (shown on the back).
5. THE `flashcards_cloze.csv` SHALL use columns: `text`, `extra`.
6. THE file SHALL use UTF-8 encoding to support Italian diacritical characters.
7. THE file SHALL conform to RFC 4180 CSV formatting.

---

### Requirement 4: Conjugation Accuracy

**User Story:** As a language learner, I want all conjugations to be grammatically correct, so that I am not learning incorrect Italian.

#### Acceptance Criteria

1. ALL present tense forms SHALL be simple present indicative (e.g. `dormo`, not `sono addormentato`).
2. ALL past tense forms SHALL be passato prossimo with the correct auxiliary verb (e.g. `ho dormito` for dormire, `sono andato` for andare).
3. ALL future tense forms SHALL be futuro semplice (e.g. `dormirò`, not `sarò dormito`).
4. THE Workflow SHALL use mlconjug3 as the authoritative source for all conjugations.
5. THE Workflow SHALL raise a `ConjugatorError` if mlconjug3 fails to conjugate the given verb.

---

### Requirement 5: Conjugation Table with English Translation (Optional)

**User Story:** As a language learner, I want an optional HTML conjugation reference table with English translation, so that I can review all forms at a glance and understand what the verb means.

#### Acceptance Criteria

1. WHEN the `--table` flag is provided, THE Workflow SHALL generate a `conjugation_table.html` file in the verb folder.
2. THE table title SHALL display the verb with English translation — e.g. `mangiare (to eat)`.
3. IF the verb is in the A1–A2 list, THE translation SHALL be sourced from `verb_translations.json`.
4. IF the verb is not in the list, THE title SHALL display only the infinitive — e.g. `dormire`.
5. THE table SHALL display all conjugated forms grouped by tense: Presente Indicativo, Passato Prossimo, Futuro Semplice.
6. THE table SHALL be a self-contained HTML file that opens in any browser without internet access.
7. ALL forms in the table SHALL be sourced from mlconjug3 — identical to the flashcard data.
8. THE table SHALL be visually clean and printable.

---

### Requirement 6: Verb Folder Storage

**User Story:** As a language learner, I want each verb's output stored in its own folder, so that I can easily find and import cards for any verb.

#### Acceptance Criteria

1. WHEN the workflow completes, THE Workflow SHALL store all artifacts in a folder named after the verb (e.g. `verb_artifacts/mangiare/`).
2. IF a folder for that verb already exists, THE Workflow SHALL automatically create a versioned folder (`-v2`, `-v3`, etc.) without overwriting existing content.
3. THE Workflow SHALL create the output root directory if it does not exist.
4. IF the workflow fails after creating the folder, THE Workflow SHALL delete the partially written folder before exiting.
5. THE output root directory SHALL be configurable via `--output` CLI flag (default: `./verb_artifacts`).

---

### Requirement 7: Duplicate Verb Prevention

**User Story:** As a language learner, I want the tool to warn me if I try to generate cards for a verb I've already processed, so that I don't create duplicate Anki cards.

#### Acceptance Criteria

1. THE Workflow SHALL maintain a `vocab_state.json` file tracking all processed verbs.
2. WHEN a verb has already been processed, THE Workflow SHALL display a warning and exit without generating new files.
3. WHEN the `--force` flag is provided, THE Workflow SHALL bypass the duplicate check and generate new files regardless.
4. THE `vocab_state.json` SHALL be updated after each successful run.

---

### Requirement 8: CLI Interface

**User Story:** As a user, I want a simple command-line interface, so that I can generate flashcards quickly without configuration.

#### Acceptance Criteria

1. THE CLI SHALL accept `--verb` as a required argument specifying the Italian infinitive.
2. THE CLI SHALL accept `--table` as an optional flag to generate the conjugation table.
3. THE CLI SHALL accept `--output` as an optional argument to specify the output directory.
4. THE CLI SHALL accept `--force` as an optional flag to bypass duplicate verb checking.
5. THE CLI SHALL accept `--list-verbs` as an optional flag to display all processed verbs and exit.
6. THE CLI SHALL accept `--definitions-batch` as an optional flag to generate definition cloze cards for all 57 A1–A2 verbs.
7. THE CLI SHALL display user-friendly error messages for all known failure modes.
8. THE CLI SHALL exit with code 0 on success and code 1 on any error.
9. NO API keys, environment variables, or external services SHALL be required to run the tool.

---

### Requirement 9: Batch Definitions Mode

**User Story:** As a language learner, I want to generate vocabulary cloze cards for all 57 A1–A2 verbs at once, so that I can build a comprehensive vocabulary deck alongside conjugation drilling.

#### Acceptance Criteria

1. WHEN the `--definitions-batch` flag is provided, THE Workflow SHALL generate a single file: `definitions_deck.csv`.
2. THE file SHALL contain exactly 57 rows: one definition cloze card per A1–A2 verb.
3. EACH card `text` field SHALL contain: `{{c1::infinitive}}` — e.g. `{{c1::mangiare}}`.
4. EACH card `extra` field SHALL contain the English translation — e.g. `to eat`.
5. THE file SHALL use columns: `text`, `extra`.
6. THE file SHALL use UTF-8 encoding.
7. THE file SHALL conform to RFC 4180 CSV formatting.
8. THE `--definitions-batch` flag SHALL work with the `--output` flag to specify a custom output directory.
9. THE Workflow SHALL NOT interfere with single-verb generation — both modes work independently.

---

### Requirement 10: Extended A1–A2 Verb Coverage

**User Story:** As a language learner, I want access to a comprehensive list of 57 A1–A2 verbs, so that I can build a complete foundation for beginner Italian.

#### Acceptance Criteria

1. THE Workflow SHALL support all 57 A1–A2 verbs defined in `verb_translations.json`.
2. THE 57 verbs SHALL be organized by priority: Tier 1 (10), Tier 2 (10), Tier 3 (10), High-Priority (4), Medium-Priority (13), Lower-Priority (10).
3. EACH verb SHALL have a verified English translation in `verb_translations.json`.
4. THE Workflow SHALL work for ANY valid Italian verb infinitive, not just the 57 A1–A2 verbs.
5. IF a verb is not in `verb_translations.json`, THE Workflow SHALL still generate 100% accurate conjugations and cards.
6. THE HTML conjugation table SHALL display the English translation if available, or show only the infinitive if not.
7. THE batch definitions mode SHALL generate cards only for the 57 A1–A2 verbs in `verb_translations.json`.
