"""Storage manager — creates verb folders and writes artifacts."""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


class StorageManager:
    """Manages the output directory structure and artifact file writing."""

    def __init__(self, output_root: Path | str) -> None:
        self._root = Path(output_root)
        self._log_path = self._root / "verb_log.json"
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

    def resolve_folder_name(self, infinitive: str) -> str:
        """Return a folder name for the verb that does not already exist.

        Base name: {infinitive}
        If taken: {infinitive}-v2, -v3, etc.
        """
        base = infinitive.lower().strip()
        candidate = base
        version = 2
        while (self._root / candidate).exists():
            candidate = f"{base}-v{version}"
            version += 1
        return candidate

    def create_verb_folder(self, folder_name: str) -> Path:
        """Create the verb folder and return its path."""
        folder = self._root / folder_name
        folder.mkdir(parents=True, exist_ok=False)
        return folder

    def write_flashcards(
        self,
        folder: Path,
        basic_csv: str,
        cloze_csv: str,
    ) -> None:
        """Write Basic and Cloze CSV files into the given folder."""
        (folder / "flashcards_basic.csv").write_text(basic_csv, encoding="utf-8")
        (folder / "flashcards_cloze.csv").write_text(cloze_csv, encoding="utf-8")

    def write_conjugation_table(self, folder: Path, table_html: str) -> None:
        """Write the HTML conjugation table file into the given folder."""
        (folder / "conjugation_table.html").write_text(table_html, encoding="utf-8")

    def record_run(self, folder_name: str, infinitive: str, table: bool = False) -> None:
        """Append a run entry to verb_log.json."""
        self._log.append(
            {
                "run": len(self._log) + 1,
                "folder": folder_name,
                "verb": infinitive,
                "table": table,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )
        self._save_log()

    def cleanup(self, folder: Path | None) -> None:
        """Delete a partially written folder on failure."""
        if folder is not None and folder.exists():
            shutil.rmtree(folder)
            print(f"  [Storage] Cleaned up partial folder: {folder}")
