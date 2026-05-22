"""Vocabulary tracker — prevents word reuse across runs of the same theme."""

from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import List


class VocabTracker:
    """Tracks which vocabulary words have been used per theme per category.

    State is persisted to vocab_state.json in the output root directory.
    """

    CATEGORIES = ("verbs", "nouns", "adjectives")

    def __init__(self, output_root: Path | str) -> None:
        self._root = Path(output_root)
        self._state_path = self._root / "vocab_state.json"
        self._state: dict = {}
        self._load()

    def _load(self) -> None:
        if self._state_path.exists():
            with self._state_path.open("r", encoding="utf-8") as f:
                self._state = json.load(f)
        else:
            self._state = {}

    def save(self) -> None:
        """Persist current state to disk."""
        self._root.mkdir(parents=True, exist_ok=True)
        with self._state_path.open("w", encoding="utf-8") as f:
            json.dump(self._state, f, ensure_ascii=False, indent=2)

    def _ensure_theme_category(self, theme_id: str, category: str) -> None:
        if theme_id not in self._state:
            self._state[theme_id] = {}
        if category not in self._state[theme_id]:
            self._state[theme_id][category] = {"used": [], "pool": []}

    def set_pool(self, theme_id: str, category: str, words: List[str]) -> None:
        """Set the full vocabulary pool for a theme/category (called on first use)."""
        self._ensure_theme_category(theme_id, category)
        existing_pool = self._state[theme_id][category]["pool"]
        existing_used = self._state[theme_id][category]["used"]
        # Only add words not already tracked
        known = set(existing_pool) | set(existing_used)
        new_words = [w for w in words if w not in known]
        self._state[theme_id][category]["pool"].extend(new_words)

    def select_words(self, theme_id: str, category: str, count: int) -> List[str]:
        """Return `count` words for the given theme/category.

        Prefers unused words. If the pool is exhausted, cycles from oldest used words.
        Emits warnings when the pool is running low or exhausted.
        """
        self._ensure_theme_category(theme_id, category)
        entry = self._state[theme_id][category]
        pool: List[str] = entry["pool"]
        used: List[str] = entry["used"]

        selected: List[str] = []

        # Take from pool first
        while len(selected) < count and pool:
            selected.append(pool.pop(0))

        # If we still need more, cycle from oldest used
        if len(selected) < count:
            shortfall = count - len(selected)
            if used:
                warnings.warn(
                    f"Vocabulary pool for theme '{theme_id}' / category '{category}' "
                    f"is exhausted. Reusing {shortfall} word(s) from oldest runs.",
                    UserWarning,
                    stacklevel=2,
                )
                recycled = used[:shortfall]
                selected.extend(recycled)
                # Move recycled words to end of used list
                entry["used"] = used[shortfall:] + recycled
            else:
                warnings.warn(
                    f"No vocabulary available for theme '{theme_id}' / category '{category}'.",
                    UserWarning,
                    stacklevel=2,
                )
        elif len(pool) < count:
            warnings.warn(
                f"Vocabulary pool for theme '{theme_id}' / category '{category}' "
                f"is running low ({len(pool)} word(s) remaining after this run).",
                UserWarning,
                stacklevel=2,
            )

        # Mark selected words as used
        entry["used"].extend(selected)

        return selected

    def mark_used(self, theme_id: str, category: str, words: List[str]) -> None:
        """Explicitly mark words as used (called after successful run)."""
        self._ensure_theme_category(theme_id, category)
        entry = self._state[theme_id][category]
        for word in words:
            if word not in entry["used"]:
                entry["used"].append(word)
            if word in entry["pool"]:
                entry["pool"].remove(word)
