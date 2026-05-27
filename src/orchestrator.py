"""Workflow orchestrator — wires all modules together for a single verb run."""

from __future__ import annotations

from pathlib import Path

from .verb_conjugator import VerbConjugator, ConjugatorError
from .flashcard_builder import FlashcardBuilder, FlashcardError
from .conjugation_table_builder import ConjugationTableBuilder, ConjugationTableError
from .vocab_tracker import VocabTracker
from .storage import StorageManager


class WorkflowOrchestrator:
    """Runs the full flashcard generation pipeline for a single Italian verb."""

    def run(
        self,
        infinitive: str,
        output_dir: str = "./verb_artifacts",
        force: bool = False,
        table: bool = False,
    ) -> None:
        """Generate Anki flashcard CSVs and optionally conjugation table for a verb.

        Args:
            infinitive: The Italian verb infinitive, e.g. "mangiare".
            output_dir: Root directory for output folders.
            force: If True, skip the duplicate-verb check and run anyway.
            table: If True, generate HTML conjugation table (LLM-free).
        """
        output_root = Path(output_dir)
        storage = StorageManager(output_root)
        vocab_tracker = VocabTracker(output_root)

        verb_folder: Path | None = None

        # Step 1: Validate verb and check for duplicates
        print(f"[1/4] Checking verb '{infinitive}'...")
        infinitive = infinitive.lower().strip()

        if not force and vocab_tracker.has_verb(infinitive):
            print(
                f"\n⚠️  '{infinitive}' has already been processed.\n"
                f"   Use --force to generate cards again anyway."
            )
            return

        # Step 2: Generate conjugation data
        print(f"[2/4] Generating conjugations for '{infinitive}'...")
        conjugator = VerbConjugator()  # No LLM needed for conjugations
        data = conjugator.conjugate(infinitive)
        print(f"      Present: {data.present_io}, {data.present_tu}, {data.present_lui_lei}, "
              f"{data.present_noi}, {data.present_voi}, {data.present_loro}")
        print(f"      Past:    {data.past_io}, {data.past_tu}")
        print(f"      Future:  {data.future_io}, {data.future_tu}")
        print(f"      Cloze sentences: {len(data.cloze_sentences)}")

        # Step 3: Build flashcard CSVs
        print("[3/4] Building flashcards...")
        builder = FlashcardBuilder()
        basic_rows = builder.build_basic(data)
        cloze_rows = builder.build_cloze(data)
        basic_csv = builder.to_basic_csv(basic_rows)
        cloze_csv = builder.to_cloze_csv(cloze_rows)
        print(f"      Basic cards: {len(basic_rows)}")
        print(f"      Cloze cards: {len(cloze_rows)}")

        # Step 4: Write artifacts
        print("[4/4] Writing files...")
        folder_name = storage.resolve_folder_name(infinitive)
        verb_folder = storage.create_verb_folder(folder_name)
        storage.write_flashcards(verb_folder, basic_csv, cloze_csv)

        # Optional: Generate conjugation table
        if table:
            print("      Generating conjugation table...")
            table_builder = ConjugationTableBuilder()
            table_html = table_builder.build_html_table(data)
            storage.write_conjugation_table(verb_folder, table_html)

        storage.record_run(folder_name, infinitive, table=table)
        vocab_tracker.mark_verb(infinitive)
        vocab_tracker.save()

        print(f"\n✅ Done! Artifacts written to: {verb_folder}")
        print(f"   flashcards_basic.csv  — import into Anki as Basic note type")
        print(f"   flashcards_cloze.csv  — import into Anki as Cloze note type")
        if table:
            print(f"   conjugation_table.html — reference table, open in any browser")
