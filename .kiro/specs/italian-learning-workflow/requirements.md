# Requirements Document

## Introduction

The Italian Learning Workflow is a weekly content generation system for A1-level (beginner) Italian learners. Each week, a theme is selected and the system generates a coordinated set of learning artifacts: an Anki-compatible flashcard CSV (10 cards covering 2 verbs, 2 nouns, and 2 adjectives), a short Italian reading passage, and an offline HTML multiple-choice quiz. All artifacts are stored in a per-week folder. The system supports re-running a theme to produce fresh content, and the theme list can be extended over time. Content is simple, practical, and conversational — no formal grammar instruction.

## Glossary

- **Workflow**: The end-to-end weekly process that selects a theme and generates all learning artifacts.
- **Theme**: A topic (e.g., "food", "travel", "family") that anchors the vocabulary and content for a given week.
- **Theme_Registry**: The managed list of available themes that can be extended over time.
- **Week_Folder**: A directory named by week number and theme (e.g., `week-01-food/`) that stores all artifacts for that week's run.
- **Flashcard_CSV**: A comma-separated values file formatted for import into Anki, containing exactly 10 flashcards per week.
- **Flashcard**: A single study card representing one vocabulary item with its translation and an example sentence.
- **Reading_Passage**: A 150–200 word Italian text written at A1 level that naturally incorporates the week's vocabulary.
- **Quiz**: An offline HTML file containing a Duolingo-style multiple-choice quiz based on the week's vocabulary and passage.
- **Verb**: An Italian verb selected for the week; two verbs are chosen per run.
- **Noun**: An Italian noun selected for the week; two nouns are chosen per run.
- **Adjective**: An Italian adjective selected for the week; two adjectives are chosen per run.
- **Conjugation**: The present-tense forms of a verb across all six persons (io, tu, lui/lei, noi, voi, loro).
- **Tense_Example**: A short Italian sentence demonstrating a verb in past (passato prossimo) or future (futuro semplice) tense, with English translation.
- **A1_Level**: The beginner level of the Common European Framework of Reference (CEFR) for languages, characterized by simple, high-frequency vocabulary and short sentences.
- **Re-run**: Executing the workflow for a theme that has been used before, producing new vocabulary, passage, and quiz content.

---

## Requirements

### Requirement 1: Weekly Workflow Execution

**User Story:** As a language learner, I want to run a weekly workflow for a chosen theme, so that I receive a complete set of coordinated learning materials for that week.

#### Acceptance Criteria

1. WHEN the workflow is executed with a theme name, THE Workflow SHALL generate all three artifacts — Flashcard_CSV, Reading_Passage, and Quiz — for that theme.
2. WHEN the workflow completes, THE Workflow SHALL store all generated artifacts inside a dedicated Week_Folder.
3. THE Week_Folder SHALL be named using the pattern `week-{NN}-{theme}` where `{NN}` is the sequential execution count zero-padded to two digits (e.g., 01, 02) and `{theme}` is the theme name in lowercase kebab-case.
4. WHEN the workflow is executed, THE Workflow SHALL select exactly two Verbs, two Nouns, and two Adjectives where each word belongs to the CEFR A1_Level word list and is semantically related to the chosen theme.
5. THE Workflow SHALL produce content using only A1_Level vocabulary and sentence structures as defined by the CEFR A1_Level specification.
6. IF any single artifact fails to generate, THEN THE Workflow SHALL not write a partial Week_Folder and SHALL report which artifact failed before exiting.

---

### Requirement 2: Anki Flashcard CSV Export

**User Story:** As a language learner, I want an Anki-compatible flashcard CSV with exactly 10 cards per week, so that I can import the week's vocabulary directly into Anki for spaced-repetition study.

#### Acceptance Criteria

1. THE Flashcard_CSV SHALL contain exactly 10 Flashcard rows per weekly run: 3 rows per Verb (present tense, past tense, future tense) and 1 row per Noun and 1 row per Adjective (base form with translation and example sentence), totalling 2×3 + 2×1 + 2×1 = 10 rows.
2. THE Flashcard_CSV SHALL include the following columns for each row: Italian form, English translation, source word (infinitive for verbs, base form for nouns/adjectives), word type (verb/noun/adjective), tense or form label, Italian example sentence, and English example sentence translation as a separate column.
3. THE Flashcard_CSV SHALL use UTF-8 encoding to support Italian diacritical characters (e.g., è, à, ò, ù, ì).
4. THE Flashcard_CSV SHALL conform to RFC 4180 formatting: comma-delimited, fields containing commas or double-quotes quoted with double-quotes, and double-quotes within fields escaped by doubling.
5. THE Flashcard_CSV SHALL include a header row identifying each column.
6. THE Flashcard_CSV example sentences SHALL use sentences of no more than 12 words each.
7. WHEN any field value contains a comma, THE Flashcard_CSV SHALL enclose that field in double-quotes to prevent Anki's CSV parser from splitting the field incorrectly.

---

### Requirement 3: Italian Reading Passage

**User Story:** As a language learner, I want a short Italian reading passage, so that I can see the week's vocabulary used naturally in context.

#### Acceptance Criteria

1. THE Reading_Passage SHALL be between 150 and 200 words in length.
2. THE Reading_Passage SHALL be written entirely in Italian at A1_Level.
3. THE Reading_Passage SHALL incorporate each of the two Verbs, two Nouns, and two Adjectives from the week's vocabulary at least once, in their base, conjugated, or inflected form.
4. THE Reading_Passage SHALL be accompanied by an English translation saved as `passage_en.txt` in the same Week_Folder; the translation SHALL translate every sentence of the passage.
5. THE Reading_Passage SHALL be saved as a plain text file named `passage.txt` inside the Week_Folder.
6. THE Reading_Passage setting, characters, and actions SHALL relate to the week's Theme.
7. IF the passage word count falls outside the 150–200 word range, THEN THE Workflow SHALL regenerate the passage up to a maximum of 3 attempts; if the constraint is still not met after 3 attempts, THE Workflow SHALL notify the user and halt.

---

### Requirement 4: Offline HTML Multiple-Choice Quiz

**User Story:** As a language learner, I want a gamified multiple-choice quiz I can open in a browser, so that I can test my knowledge of the week's vocabulary without needing an internet connection.

#### Acceptance Criteria

1. THE Quiz SHALL be a single self-contained HTML file that runs entirely offline without external network requests.
2. THE Quiz SHALL contain a minimum of 10 multiple-choice questions derived from the week's Flashcard_CSV content and Reading_Passage.
3. WHEN a learner selects an answer, THE Quiz SHALL highlight the selected option in green if correct or red if incorrect within 300 milliseconds.
4. WHEN a learner completes all questions, THE Quiz SHALL display a final score as a count of correct answers and a percentage.
5. WHEN the HTML file is opened, THE Quiz SHALL present questions in a randomized order and SHALL randomize the position of answer options for each question.
6. WHEN a learner answers incorrectly, THE Quiz SHALL reveal the correct answer and SHALL require the learner to click a "Next" button before advancing to the next question.
7. THE Quiz SHALL include questions of at least two distinct types: Italian-to-English translation and fill-in-the-blank sentence completion.
8. THE Quiz SHALL be saved as `quiz.html` inside the Week_Folder.
9. THE Quiz SHALL be usable on Chrome 90+, Firefox 88+, and Safari 14+ without installing additional software or plugins.
10. EACH multiple-choice question SHALL present exactly four answer options.

---

### Requirement 5: Per-Week Artifact Storage

**User Story:** As a language learner, I want each week's content stored in its own folder, so that I can easily find and review past weeks' materials.

#### Acceptance Criteria

1. WHEN the workflow is executed, THE Workflow SHALL create a new Week_Folder before writing any artifacts.
2. THE Week_Folder SHALL contain exactly the following files upon successful completion: `flashcards.csv`, `passage.txt`, `passage_en.txt`, and `quiz.html`.
3. IF a Week_Folder with the same name already exists, THEN THE Workflow SHALL automatically generate a versioned folder name by appending `-v2`, `-v3`, etc. (incrementing until an unused name is found) without prompting the user.
4. THE Workflow SHALL never overwrite the contents of an existing Week_Folder.
5. THE Workflow SHALL store all Week_Folders under a common root output directory that is configurable by the user.
6. IF the root output directory does not exist, THEN THE Workflow SHALL create it before creating the Week_Folder.
7. IF the workflow fails after creating the Week_Folder but before completing all artifacts, THEN THE Workflow SHALL delete the partially written Week_Folder before exiting.

---

### Requirement 6: Re-run Support for Existing Themes

**User Story:** As a language learner, I want to re-run the workflow for a theme I've used before, so that I can get fresh content with different vocabulary and a new passage and quiz.

#### Acceptance Criteria

1. WHEN the workflow is executed with a theme that has been used in a previous week, THE Workflow SHALL select Verbs, Nouns, and Adjectives that all differ from every vocabulary item used in all prior runs of the same theme.
2. WHEN the workflow is re-run for the same theme, THE Workflow SHALL generate a new Reading_Passage and Quiz derived from the newly selected vocabulary set rather than copying any prior artifacts.
3. THE Workflow SHALL maintain a per-theme, per-category record of A1_Level vocabulary items appropriate to that theme that have been used, and SHALL prevent reuse of any item within a category until all items in that category for that theme have been exhausted.
4. IF all A1_Level vocabulary items for a theme in a given category are exhausted, THEN THE Workflow SHALL notify the user with a message identifying the theme name and the exhausted category, and SHALL resume selection for that category starting from the vocabulary items used in the oldest prior run.
5. IF fewer than two unused A1_Level vocabulary items remain in a single category for a theme, THEN THE Workflow SHALL notify the user of the shortfall and SHALL reuse the oldest items in that category to complete the required count of two.

---

### Requirement 7: Theme Registry

**User Story:** As a language learner, I want a list of themes I can choose from and extend over time, so that my weekly learning stays varied and relevant to my interests.

#### Acceptance Criteria

1. THE Theme_Registry SHALL be stored in a `themes.yaml` file in the project root.
2. THE Theme_Registry SHALL include a minimum of 10 pre-defined themes at initial setup (e.g., food, travel, family, weather, shopping, health, home, work, hobbies, transport).
3. WHEN a user adds a new theme to the `themes.yaml` file, THE Workflow SHALL recognize and use the new theme on the next execution without requiring code changes; theme name matching SHALL be case-insensitive.
4. WHEN the workflow is executed with a theme name not present in the Theme_Registry, THE Workflow SHALL display a clear error message that names the unrecognised theme and lists all available theme labels.
5. THE Theme_Registry SHALL store, for each theme, a human-readable label of 1–50 characters and an optional description of up to 200 characters to guide content generation.
6. IF the `themes.yaml` file is missing or cannot be parsed, THEN THE Workflow SHALL display a clear error message identifying the file path and the nature of the problem, and SHALL halt execution.

---

### Requirement 8: Content Quality and A1 Compliance

**User Story:** As a beginner learner, I want all generated content to match my A1 level, so that I am not overwhelmed by vocabulary or grammar beyond my current ability.

#### Acceptance Criteria

1. THE Workflow SHALL restrict all generated vocabulary to words and phrases on the CEFR A1_Level word list; IF a generated artifact contains a word not on the A1_Level word list, THEN THE Workflow SHALL regenerate that artifact.
2. THE Quiz questions and answer options SHALL use only vocabulary present in the week's Flashcard_CSV or Reading_Passage.
3. THE Workflow SHALL not include advanced grammar terminology (e.g., "subjunctive", "gerund", "declension") in any generated artifact; basic word-type labels (e.g., "verb", "noun", "adjective") and tense labels (e.g., "present", "past", "future") used in the Flashcard_CSV are exempt from this restriction.
4. IF any generated artifact is found to contain vocabulary outside the A1_Level word list after regeneration, THEN THE Workflow SHALL log the offending words and halt with an error message.
