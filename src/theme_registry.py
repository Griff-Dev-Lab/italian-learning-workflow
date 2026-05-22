"""Theme registry — loads and validates themes.yaml."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml


class ThemeRegistryError(Exception):
    """Raised when themes.yaml is missing or cannot be parsed."""


class UnknownThemeError(Exception):
    """Raised when a requested theme is not in the registry."""


@dataclass
class Theme:
    id: str
    label: str
    description: str


class ThemeRegistry:
    """Loads themes from themes.yaml and provides lookup by id."""

    def __init__(self, themes_path: Path | str | None = None) -> None:
        if themes_path is None:
            # Default: themes.yaml in project root (parent of src/)
            themes_path = Path(__file__).parent.parent / "themes.yaml"
        self._path = Path(themes_path)
        self._themes: dict[str, Theme] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            raise ThemeRegistryError(
                f"themes.yaml not found at '{self._path}'. "
                "Please ensure the file exists in the project root."
            )
        try:
            with self._path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            raise ThemeRegistryError(
                f"Failed to parse '{self._path}': {exc}"
            ) from exc

        if not isinstance(data, dict) or "themes" not in data:
            raise ThemeRegistryError(
                f"'{self._path}' must contain a top-level 'themes' list."
            )

        for entry in data["themes"]:
            theme = Theme(
                id=entry["id"],
                label=entry.get("label", entry["id"]),
                description=entry.get("description", ""),
            )
            self._themes[theme.id.lower()] = theme

    def get_theme(self, name: str) -> Theme:
        """Return a Theme by id (case-insensitive).

        Raises UnknownThemeError listing all available themes if not found.
        """
        key = name.strip().lower()
        if key not in self._themes:
            available = ", ".join(t.label for t in self._themes.values())
            raise UnknownThemeError(
                f"Unknown theme '{name}'. Available themes: {available}"
            )
        return self._themes[key]

    def all_themes(self) -> List[Theme]:
        return list(self._themes.values())
