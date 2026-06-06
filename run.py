#!/usr/bin/env python3
"""Italian Verb Flashcard Generator — CLI entry point.

Usage:
    python run.py --verb mangiare
    python run.py --verb mangiare --table
    python run.py --verb mangiare --output ./my_output
    python run.py --verb mangiare --force
    python run.py --list-verbs
    python run.py --definitions-batch
    python run.py --definitions-batch --output ./my_output
"""

import argparse
import sys

from src.orchestrator import WorkflowOrchestrator
from src.vocab_tracker import VocabTracker
from src.verb_conjugator import ConjugatorError
from src.flashcard_builder import FlashcardError
from src.conjugation_table_builder import ConjugationTableError


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Anki flashcards for Italian verbs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py --verb mangiare
  python run.py --verb mangiare --table
  python run.py --verb mangiare --output ./my_output
  python run.py --verb mangiare --force
  python run.py --list-verbs
  python run.py --definitions-batch
  python run.py --definitions-batch --output ./my_output
        """,
    )
    parser.add_argument(
        "--verb",
        type=str,
        help="Italian verb infinitive to generate flashcards for (e.g. mangiare).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./verb_artifacts",
        help="Root output directory for verb folders (default: ./verb_artifacts).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-generate cards even if this verb has been processed before.",
    )
    parser.add_argument(
        "--table",
        action="store_true",
        help="Generate HTML conjugation reference table in addition to flashcards.",
    )
    parser.add_argument(
        "--list-verbs",
        action="store_true",
        help="List all verbs that have already been processed and exit.",
    )
    parser.add_argument(
        "--definitions-batch",
        action="store_true",
        help="Generate definition Basic cards for all 57 A1-A2 verbs in verb_translations.json.",
    )

    args = parser.parse_args()

    # Handle --list-verbs
    if args.list_verbs:
        tracker = VocabTracker(args.output)
        verbs = tracker.all_verbs()
        if verbs:
            print("Processed verbs:")
            for v in verbs:
                print(f"  {v}")
        else:
            print("No verbs processed yet.")
        return 0

    # Handle --definitions-batch
    if args.definitions_batch:
        try:
            orchestrator = WorkflowOrchestrator()
            orchestrator.generate_definitions_batch(output_dir=args.output)
            return 0
        except Exception as exc:
            print(f"\n❌ Definitions batch generation failed: {exc}", file=sys.stderr)
            return 1

    if not args.verb:
        parser.print_help()
        print("\nError: --verb is required (or use --definitions-batch).", file=sys.stderr)
        return 1

    try:
        orchestrator = WorkflowOrchestrator()
        orchestrator.run(
            infinitive=args.verb,
            output_dir=args.output,
            force=args.force,
            table=args.table,
        )
        return 0

    except ConjugatorError as exc:
        print(f"\n❌ Conjugation failed: {exc}", file=sys.stderr)
        return 1

    except FlashcardError as exc:
        print(f"\n❌ Flashcard generation failed: {exc}", file=sys.stderr)
        return 1

    except ConjugationTableError as exc:
        print(f"\n❌ Conjugation table generation failed: {exc}", file=sys.stderr)
        return 1

    except KeyboardInterrupt:
        print("\n\nInterrupted.", file=sys.stderr)
        return 1

    except Exception as exc:
        print(f"\n❌ Unexpected error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
