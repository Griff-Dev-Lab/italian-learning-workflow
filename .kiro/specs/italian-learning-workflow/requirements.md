# Requirements Document

## Introduction

The Italian Learning Workflow is a CLI tool for A1–A2 Italian learners that generates Anki-ready flashcard CSVs and optional conjugation reference tables for any Italian verb. All content is generated using the mlconjug3 linguistic library — no LLM, no internet connection, and no API keys are required. The tool produces 100% accurate Italian conjugations every time.

## Glossary

- **Verb**: An Italian verb infinitive provided by the user (e.g. `mangiare`, `dormire`, `andare`).
- **Conjugation**: The inflected forms of a verb across persons and tenses.
- **Basic Card**: An Anki flashcard with a prompt on the front (e.g. `mangiare (io, present)`) and the conjugated form on the back (e.g. `mangio`).
- **Cloze Card**: An Anki flashcard where a conjugated form is blanked out in a sentence (e.g. `(mangiare) Ogni giorno io {{c1::mangio}}.`).
- **Conjugation Table**: An HTML file showing all conjugated forms for a verb in a clean reference layout.
- **Verb Folder**: A directory named after the verb (e.g. `verb_artifacts/mangiare/`) that stores all generated artifacts.
- **mlconjug3**: A Python linguistic library providing accurate Italian verb conjugations.
- **Passato Prossimo**: Italian compound past tense (e.g. `ho mangiato`, `sono andato`).
- **Futuro Semplice**: Italian simple future tense (e.g. `mangerò`, `dormirò`).
- **Avere/Essere**: The two Italian auxiliary verbs used in passato prossimo — most verbs use `avere`, motion/state verbs use `essere`.

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

1. EACH Basic card front SHALL follow the format: `{infinitive} ({person}, {tense})` — e.g. `mangiare (io, present)`.
2. EACH Basic card back SHALL contain only the conjugated form — e.g. `mangio`.
3. THE `flashcards_basic.csv` SHALL use columns: `front`, `back`.
4. THE file SHALL use UTF-8 encoding to support Italian diacritical characters (è, à, ò, ù, ì, etc.).
5. THE file SHALL conform to RFC 4180 CSV formatting.

---

### Requirement 3: Cloze Flashcard Format

**User Story:** As a language learner, I want Cloze flashcards that test me in context, so that I can practise conjugating verbs within sentences.

#### Acceptance Criteria

1. EACH Cloze card `text` field SHALL include the verb infinitive in parentheses at the start — e.g. `(mangiare) Ogni giorno io {{c1::mangio}}.`
2. THE infinitive prefix SHALL make the target verb unambiguous — the learner knows which verb to conjugate.
3. EACH sentence SHALL include an explicit subject pronoun (io, tu, lui, lei, noi, voi, loro) to ensure only one conjugated form is correct.
4. THE `{{c1::answer}}` syntax SHALL wrap the conjugated form for Anki cloze deletion.
5. THE `flashcards_cloze.csv` SHALL use columns: `text`, `extra`.
6. THE `extra` field SHALL contain the label — e.g. `mangiare — io, present`.
7. Sentences SHALL use simple, natural Italian templates appropriate for A1–A2 level.

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

### Requirement 5: Conjugation Table (Optional)

**User Story:** As a language learner, I want an optional HTML conjugation reference table, so that I can review all forms at a glance.

#### Acceptance Criteria

1. WHEN the `--table` flag is provided, THE Workflow SHALL generate a `conjugation_table.html` file in the verb folder.
2. THE table SHALL display all conjugated forms grouped by tense: Presente Indicativo, Passato Prossimo, Futuro Semplice.
3. THE table SHALL be a self-contained HTML file that opens in any browser without internet access.
4. ALL forms in the table SHALL be sourced from mlconjug3 — identical to the flashcard data.
5. THE table SHALL be visually clean and printable.

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
6. THE CLI SHALL display user-friendly error messages for all known failure modes.
7. THE CLI SHALL exit with code 0 on success and code 1 on any error.
8. NO API keys, environment variables, or external services SHALL be required to run the tool.
