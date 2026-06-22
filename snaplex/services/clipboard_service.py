"""Clipboard service contracts."""

from __future__ import annotations

from typing import Protocol, cast


class ClipboardError(RuntimeError):
    """Raised when clipboard access fails."""


class ClipboardService(Protocol):
    def get_text(self) -> str:
        """Return the current clipboard text."""
        ...

    def set_text(self, text: str) -> None:
        """Replace the current clipboard text."""
        ...


class _DesktopClipboard(Protocol):
    def text(self) -> str:
        """Return clipboard text from a desktop clipboard object."""
        ...

    def setText(self, text: str) -> None:
        """Set clipboard text on a desktop clipboard object."""
        ...


class InMemoryClipboardService:
    def __init__(self, text: str = "") -> None:
        self._text = text

    def get_text(self) -> str:
        return self._text

    def set_text(self, text: str) -> None:
        self._text = text


class QtClipboardService:
    def __init__(self, clipboard: _DesktopClipboard) -> None:
        self._clipboard = clipboard

    @classmethod
    def from_application(cls) -> "QtClipboardService":
        try:
            from PySide6.QtWidgets import QApplication
        except ModuleNotFoundError as exc:
            raise ClipboardError("PySide6 is required for the desktop clipboard.") from exc

        app = QApplication.instance()
        if app is None:
            raise ClipboardError("QApplication is not running.")

        return cls(cast(QApplication, app).clipboard())

    def get_text(self) -> str:
        try:
            return self._clipboard.text()
        except Exception as exc:
            raise ClipboardError("Failed to read clipboard text.") from exc

    def set_text(self, text: str) -> None:
        try:
            self._clipboard.setText(text)
        except Exception as exc:
            raise ClipboardError("Failed to write clipboard text.") from exc
