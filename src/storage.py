"""Storage manager — creates week folders and writes artifacts atomically."""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


class StorageManager:
    """Manages the output directory structure and artifact file writing."""

    def __init__(self, output_root: Path | str) -> None:
        self._root = Path(output_root)
        self._log_path = self._root / "run_log.json"
        self._log: list = []
        self._ensure_root()
        self._load_log()

    def _ensure_root(self) -> None:
        self._root.mkdir(parents=True, exist_ok=True)

    def _load_log(self) -> None:
        if self._log_path.exists():
            with self._log_path.open("r", encoding="utf-8") as f:
                self._log = json.load(f)
        else:
            self._log = []

    def _save_log(self) -> None:
        with self._log_path.open("w", encoding="utf-8") as f:
            json.dump(self._log, f, ensure_ascii=False, indent=2)

    def next_run_number(self) -> int:
        """Return the next sequential run number (1-based)."""
        return len(self._log) + 1

    def resolve_folder_name(self, week_num: int, theme_id: str) -> str:
        """Return a folder name that does not already exist.

        Base name: week-{NN}-{theme}
        If taken: week-{NN}-{theme}-v2, -v3, etc.
        """
        base = f"week-{week_num:02d}-{theme_id.lower().replace(' ', '-')}"
        candidate = base
        version = 2
        while (self._root / candidate).exists():
            candidate = f"{base}-v{version}"
            version += 1
        return candidate

    def create_week_folder(self, folder_name: str) -> Path:
        """Create the week folder and return its path."""
        folder = self._root / folder_name
        folder.mkdir(parents=True, exist_ok=False)
        return folder

    def write_artifacts(
        self,
        folder: Path,
        flashcards_csv: str,
        passage_it: str,
        passage_en: str,
        quiz_html: str,
    ) -> None:
        """Write all four artifact files into the given folder."""
        (folder / "flashcards.csv").write_text(flashcards_csv, encoding="utf-8")
        (folder / "passage.txt").write_text(passage_it, encoding="utf-8")
        (folder / "passage_en.txt").write_text(passage_en, encoding="utf-8")
        (folder / "quiz.html").write_text(quiz_html, encoding="utf-8")

    def record_run(self, folder_name: str, theme_id: str, vocab: dict) -> None:
        """Append a run entry to run_log.json."""
        self._log.append(
            {
                "run": len(self._log) + 1,
                "folder": folder_name,
                "theme": theme_id,
                "vocab": vocab,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )
        self._save_log()

    def cleanup(self, folder: Path | None) -> None:
        """Delete a partially written folder on failure."""
        if folder is not None and folder.exists():
            shutil.rmtree(folder)
            print(f"  [Storage] Cleaned up partial folder: {folder}")
