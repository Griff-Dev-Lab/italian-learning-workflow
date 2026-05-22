#!/usr/bin/env python3
"""Italian Learning Workflow — CLI entry point.

Usage:
    python run.py --theme food
    python run.py --theme travel --output ./my_output
    python run.py --list-themes
"""

import argparse
import sys
from pathlib import Path

# Load .env before importing anything that reads env vars
from dotenv import load_dotenv
load_dotenv()

from src.orchestrator import WorkflowOrchestrator
from src.theme_registry import ThemeRegistry, ThemeRegistryError, UnknownThemeError
from src.llm_client import LLMError
from src.flashcard_builder import FlashcardError
from src.passage_builder import PassageError
from src.quiz_builder import QuizError


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate weekly Italian learning artifacts (flashcards, passage, quiz).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py --theme food
  python run.py --theme travel --output ./my_output
  python run.py --list-themes
        """,
    )
    parser.add_argument(
        "--theme",
        type=str,
        help="Theme name for this week's content (e.g. food, travel, family).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./weekly_artifacts",
        help="Root output directory for weekly artifact folders (default: ./weekly_artifacts).",
    )
    parser.add_argument(
        "--list-themes",
        action="store_true",
        help="List all available themes and exit.",
    )

    args = parser.parse_args()

    # Handle --list-themes
    if args.list_themes:
        try:
            registry = ThemeRegistry()
            print("Available themes:")
            for theme in registry.all_themes():
                print(f"  {theme.id:<16} {theme.label}")
        except ThemeRegistryError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        return 0

    if not args.theme:
        parser.print_help()
        print("\nError: --theme is required. Use --list-themes to see available themes.", file=sys.stderr)
        return 1

    try:
        orchestrator = WorkflowOrchestrator()
        orchestrator.run(theme_name=args.theme, output_dir=args.output)
        return 0

    except ThemeRegistryError as exc:
        print(f"\n❌ Theme registry error: {exc}", file=sys.stderr)
        return 1

    except UnknownThemeError as exc:
        print(f"\n❌ {exc}", file=sys.stderr)
        print("   Run 'python run.py --list-themes' to see all available themes.", file=sys.stderr)
        return 1

    except LLMError as exc:
        print(f"\n❌ LLM error: {exc}", file=sys.stderr)
        print("   Check your OPENAI_API_KEY in .env and your internet connection.", file=sys.stderr)
        return 1

    except FlashcardError as exc:
        print(f"\n❌ Flashcard generation failed: {exc}", file=sys.stderr)
        return 1

    except PassageError as exc:
        print(f"\n❌ Passage generation failed: {exc}", file=sys.stderr)
        return 1

    except QuizError as exc:
        print(f"\n❌ Quiz generation failed: {exc}", file=sys.stderr)
        return 1

    except KeyboardInterrupt:
        print("\n\nInterrupted.", file=sys.stderr)
        return 1

    except Exception as exc:
        print(f"\n❌ Unexpected error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
