#!/usr/bin/env python3
"""Italian Verb Flashcard Generator — CLI entry point.

Usage:
    python run.py --verb mangiare
    python run.py --verb mangiare --output ./my_output
    python run.py --verb mangiare --force
    python run.py --list-verbs
"""

import argparse
import sys

# Load .env before importing anything that reads env vars
from dotenv import load_dotenv
load_dotenv()

from src.orchestrator import WorkflowOrchestrator
from src.vocab_tracker import VocabTracker
from src.llm_client import LLMError
from src.verb_conjugator import ConjugatorError
from src.flashcard_builder import FlashcardError
from src.passage_builder import PassageError


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Anki flashcards for an Italian verb.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py --verb mangiare
  python run.py --verb mangiare --output ./my_output
  python run.py --verb mangiare --force
  python run.py --list-verbs
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
        "--list-verbs",
        action="store_true",
        help="List all verbs that have already been processed and exit.",
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

    if not args.verb:
        parser.print_help()
        print("\nError: --verb is required.", file=sys.stderr)
        return 1

    try:
        orchestrator = WorkflowOrchestrator()
        orchestrator.run(
            infinitive=args.verb,
            output_dir=args.output,
            force=args.force,
        )
        return 0

    except LLMError as exc:
        print(f"\n❌ LLM error: {exc}", file=sys.stderr)
        print("   Check your OPENAI_API_KEY in .env and that Ollama is running.", file=sys.stderr)
        return 1

    except ConjugatorError as exc:
        print(f"\n❌ Conjugation failed: {exc}", file=sys.stderr)
        return 1

    except FlashcardError as exc:
        print(f"\n❌ Flashcard generation failed: {exc}", file=sys.stderr)
        return 1

    except PassageError as exc:
        print(f"\n❌ Passage generation failed: {exc}", file=sys.stderr)
        return 1

    except KeyboardInterrupt:
        print("\n\nInterrupted.", file=sys.stderr)
        return 1

    except Exception as exc:
        print(f"\n❌ Unexpected error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
