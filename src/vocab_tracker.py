"""Vocabulary tracker — prevents the same verb being processed twice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List


class VocabTracker:
    """Tracks which verbs have been processed across runs.

    State is persisted to vocab_state.json in the output root directory.
    """

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
            self._state = {"verbs": []}

    def save(self) -> None:
        """Persist current state to disk."""
        self._root.mkdir(parents=True, exist_ok=True)
        with self._state_path.open("w", encoding="utf-8") as f:
            json.dump(self._state, f, ensure_ascii=False, indent=2)

    def has_verb(self, infinitive: str) -> bool:
        """Return True if this verb has already been processed."""
        return infinitive.lower().strip() in self._state.get("verbs", [])

    def mark_verb(self, infinitive: str) -> None:
        """Mark a verb as processed."""
        key = infinitive.lower().strip()
        if "verbs" not in self._state:
            self._state["verbs"] = []
        if key not in self._state["verbs"]:
            self._state["verbs"].append(key)

    def all_verbs(self) -> List[str]:
        """Return all verbs that have been processed."""
        return list(self._state.get("verbs", []))
