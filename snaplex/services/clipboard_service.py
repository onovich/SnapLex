"""Clipboard service contracts."""

from __future__ import annotations

from typing import Protocol


class ClipboardError(RuntimeError):
    """Raised when clipboard access fails."""


class ClipboardService(Protocol):
    def get_text(self) -> str:
        """Return the current clipboard text."""
        ...

    def set_text(self, text: str) -> None:
        """Replace the current clipboard text."""
        ...


class InMemoryClipboardService:
    def __init__(self, text: str = "") -> None:
        self._text = text

    def get_text(self) -> str:
        return self._text

    def set_text(self, text: str) -> None:
        self._text = text
