"""Clipboard translation presentation state."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum


class ClipboardTranslationStatus(str, Enum):
    IDLE = "idle"
    LOADING = "loading"


@dataclass(frozen=True)
class ClipboardTranslationState:
    status: ClipboardTranslationStatus = ClipboardTranslationStatus.IDLE
    status_text: str = "Ready"
    source_text: str = ""
    translated_text: str = ""
    error_message: str = ""
    can_copy: bool = False
    can_retry: bool = False


class ClipboardTranslationPresenter:
    def __init__(self, on_translate_requested: Callable[[], None] | None = None) -> None:
        self._on_translate_requested = on_translate_requested
        self._state = ClipboardTranslationState()

    @property
    def state(self) -> ClipboardTranslationState:
        return self._state

    def request_clipboard_translation(self) -> ClipboardTranslationState:
        self._state = ClipboardTranslationState(
            status=ClipboardTranslationStatus.LOADING,
            status_text="Translating clipboard...",
        )
        if self._on_translate_requested is not None:
            self._on_translate_requested()
        return self._state

    def reset(self) -> ClipboardTranslationState:
        self._state = ClipboardTranslationState()
        return self._state
