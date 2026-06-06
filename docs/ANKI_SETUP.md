# Anki Import Guide

Complete step-by-step instructions for importing Italian Learning Workflow flashcards into Anki.

---

## Prerequisites

- Anki Desktop installed (download from [apps.ankiweb.net](https://apps.ankiweb.net))
- Generated CSV files from the workflow (see [README](../README.md#usage))

---

## Step 1: Download Anki

1. Go to [apps.ankiweb.net](https://apps.ankiweb.net)
2. Download **Anki Desktop** for your platform (macOS, Windows, Linux)
3. Install like any other application

---

## Step 2: Create a Deck

1. Launch Anki
2. Click the **"Create Deck"** button
3. Name it **"Italian Verbs"** (or your preferred name)
4. Click **OK**

This keeps all your Italian verb cards organized in one place.

---

## Step 3: Import Basic Flashcards

1. Go to **File** → **Import**
2. Navigate to your verb folder (e.g. `verb_artifacts/mangiare/`)
3. Select **`flashcards_basic.csv`**
4. In the import dialog:
   - **Note Type**: Select **"Basic"** from the dropdown
   - **Deck**: Select **"Italian Verbs"**
   - Click **Import**
5. You should see: **"Imported 18 notes."**

### What you're importing:
- 18 basic cards per verb
- Front: `mangiare (io, present)` → Back: `mangio`
- Perfect for drilling individual conjugated forms

---

## Step 4: Import Cloze Flashcards

1. Go to **File** → **Import** again
2. Select **`flashcards_cloze.csv`** from the same folder
3. In the import dialog:
   - **Note Type**: Select **"Cloze"** from the dropdown
   - **Deck**: Select **"Italian Verbs"**
   - **Allow HTML in fields**: Check ✓ (ensures `{{c1::}}` cloze syntax works)
   - Click **Import**
4. You should see: **"Imported 3 notes."**

### What you're importing:
- 3 cloze grid cards per verb (one per tense)
- Format: HTML grid showing all 6 persons with one form hidden
- Perfect for testing conjugation patterns and recognition

### Important: Gender/Number Agreement in Past Tense

**For essere-auxiliary verbs** (andare, venire, arrivare, partire, uscire, entrare, essere, stare, rimanere, tornare):
- You'll see gender/number variants displayed — e.g. `sono andato / andata`, `siamo andati / andate`
- This teaches proper agreement rules essential for Italian grammar
- The slash notation (`/`) shows both masculine and feminine forms
- Learn both forms to understand how agreement works with different subjects

**For avere-auxiliary verbs** (mangiare, dormire, etc.):
- Past participles are invariant (same form for all genders) — e.g. `ho mangiato`
- These forms don't change based on gender, so only one form is shown

**Example — andare (to go):**
- Front shows question for one person (e.g., "io")
- Back reveals all 6 persons with gender variants: `sono andato / andata`, `sei andato / andata`, etc.
- This reinforces both the conjugation pattern AND gender agreement rules

---

## Step 8: Import Definition Cards (Optional)

For vocabulary reinforcement, you can also import definition cards:

1. Generate the definitions deck (one-time):
   ```bash
   python3 run.py --definitions-batch
   ```

2. Go to **File** → **Import**
3. Select **`definitions_deck.csv`** from `verb_artifacts/`
4. In the import dialog:
   - **Note Type**: Select **"Basic"** (NOT Cloze)
   - **Deck**: Create new deck **"Italian Verbs — Definitions"**
   - **Field separator**: Set to **Comma `,`** (this is crucial!)
   - Click **Import**
5. You should see: **"Imported 57 notes."**

### ⚠️ Important: Field Separator Setting

The **field separator MUST be set to comma (`,`)** for the definitions deck to import correctly:
- Each line has format: `English definition,Italian verb`
- Example: `to eat,mangiare`
- Anki needs to know the comma separates the front and back fields
- If you skip this step, the entire line will import as the front field only

### What You're Importing

- 57 definition cards (one per A1-A2 verb)
- **Format:** Front shows English definition → Back shows Italian verb
- Example:
  - Front: `to eat`
  - Back: `mangiare`
- Tests vocabulary recall alongside conjugation practice

---

## Summary: Complete Learning System

After all imports, you'll have **two decks**:

### Deck 1: Italian Verbs (Conjugations)
- Basic cards: 18 per verb (6 present + 6 past + 6 future) — Conjugation drilling
- Cloze grid cards: 3 per verb (one per tense) — Pattern recognition with gender/number agreement
- Total: 21 cards per verb (or more if you add custom verbs)

### Deck 2: Italian Verbs — Definitions (Vocabulary)
- Definition cards: 57 total (one per A1-A2 verb)
- Format: Basic cards testing English → Italian recall
- Tests vocabulary knowledge

**Together they create a complete learning system:**
1. Learn what verbs mean (definitions)
2. Learn how to conjugate them (basic + cloze grid)
3. Understand gender/number agreement (especially for essere verbs)
4. Master forms, meanings, and patterns through spaced repetition

---

## Best Practices

### 1. Review Daily
- Spaced repetition works best with consistent daily review
- Even 10 minutes a day is better than cramming

### 2. Use Both Decks
- **Conjugations deck** drills forms and patterns
- **Definitions deck** reinforces vocabulary
- Together they reinforce verbs from multiple angles

### 3. Generate Multiple Verbs
- Start with Tier 1 verbs (see [VERB_LIST.md](VERB_LIST.md))
- Add new verbs gradually as you master previous ones
- Build your deck over time

### 4. Print Conjugation Tables
- Use the `--table` flag when generating verbs
- Print the HTML tables as quick reference sheets
- Review tables before studying cards

### 5. Create Your Own Sentences
- After mastering the cards, write your own sentences using the verbs
- This bridges the gap between flashcards and real conversation

---

## Next Steps

1. **Generate more verbs** — Follow [VERB_LIST.md](VERB_LIST.md) for a structured learning path
2. **Generate definitions deck** — `python3 run.py --definitions-batch`
3. **Study consistently** — Review your decks daily
4. **Track progress** — Anki shows your learning stats
5. **Expand to other tenses** — Future versions will support conditional, subjunctive, etc.

---

**Happy studying! 🇮🇹**
