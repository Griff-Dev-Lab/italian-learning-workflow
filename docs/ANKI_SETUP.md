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
4. You should see: **"Imported 18 notes."**

### What you're importing:
- 18 cloze cards per verb
- Format: `(mangiare) Ogni giorno io {{c1::mangio}}.`
- Perfect for testing conjugations in context

---

## Step 5: Review Your Cards

1. Click on the **"Italian Verbs"** deck
2. Click **"Study Now"** to start reviewing
3. You'll see:
   - **Basic cards**: Front shows the prompt → Back shows the answer
   - **Cloze cards**: Shows the sentence with a blank → Reveal to see the answer

### Card examples:

**Basic Card:**
```
Front: mangiare (io, present)
Back:  mangio
```

**Cloze Card:**
```
Front: (mangiare) Ogni giorno io _____.
Back:  mangio (revealed after you answer)
```

---

## Step 6: Sync to AnkiWeb (Optional)

To access your cards on mobile (AnkiDroid, AnkiWeb):

### Create an AnkiWeb Account

1. Go to [ankiweb.net](https://ankiweb.net)
2. Click **"Sign up"**
3. Create a free account (email + password)

### Sync from Desktop

1. In Anki Desktop: **Anki** → **Preferences** → **Network**
2. Enter your AnkiWeb email and password
3. Click **OK**
4. Click the **Sync** button (top right of Anki window)
5. Your deck will upload to AnkiWeb

### Access on Mobile

1. Install **AnkiDroid** (Android) or **AnkiWeb** (iOS)
2. Log in with your AnkiWeb credentials
3. Your "Italian Verbs" deck will appear
4. Start studying on the go!

---

## Troubleshooting

### "Import failed" error

**Problem:** Anki can't read the CSV file.

**Solution:**
- Make sure the file is named exactly `flashcards_basic.csv` or `flashcards_cloze.csv`
- Check that the file is in the correct folder
- Try re-generating the files with the workflow

### Cloze cards show as blank

**Problem:** The `{{c1::}}` syntax isn't rendering.

**Solution:**
- During import, make sure **"Allow HTML in fields"** is checked ✓
- Delete the imported cards and re-import with the checkbox enabled

### Cards appear in wrong deck

**Problem:** Cards imported to the wrong deck.

**Solution:**
- During import, double-check the **"Deck"** dropdown
- You can move cards after import: right-click card → "Change Deck"

### Too many cards imported

**Problem:** You see 19 or 20 cards instead of 18.

**Solution:**
- This happens if the CSV file has a header row
- The workflow should not include headers, but if it does, delete the extra card manually

---

## Best Practices

### 1. Review Daily
- Spaced repetition works best with consistent daily review
- Even 10 minutes a day is better than cramming

### 2. Use Both Card Types
- **Basic cards** drill individual forms
- **Cloze cards** test contextual understanding
- Together they reinforce conjugations from multiple angles

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
2. **Study consistently** — Review your deck daily
3. **Track progress** — Anki shows your learning stats
4. **Expand to other tenses** — Future versions will support conditional, subjunctive, etc.

---

**Happy studying! 🇮🇹**
