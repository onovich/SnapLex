"""Clipboard translation presentation state."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from snaplex.providers import TranslationResponse
from snaplex.services import ClipboardService


class ClipboardTranslationStatus(str, Enum):
    IDLE = "idle"
    LOADING = "loading"
    SUCCESS = "success"
    EMPTY = "empty"
    ERROR = "error"


@dataclass(frozen=True)
class ClipboardTranslationState:
    status: ClipboardTranslationStatus = ClipboardTranslationStatus.IDLE
    status_text: str = "Ready"
    source_text: str = ""
    translated_text: str = ""
    provider_name: str = ""
    error_message: str = ""
    can_copy: bool = False
    can_retry: bool = False


class TranslationPipelineLike(Protocol):
    async def translate_text_async(self, text: str) -> TranslationResponse:
        """Translate text using the P1 pipeline async boundary."""
        ...


class ClipboardTranslationPresenter:
    def __init__(
        self,
        on_translate_requested: Callable[[], None] | None = None,
        on_copy_result: Callable[[str], None] | None = None,
    ) -> None:
        self._on_translate_requested = on_translate_requested
        self._on_copy_result = on_copy_result
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

    def show_success(
        self,
        *,
        source_text: str,
        translated_text: str,
        provider_name: str = "",
    ) -> ClipboardTranslationState:
        self._state = ClipboardTranslationState(
            status=ClipboardTranslationStatus.SUCCESS,
            status_text="Translation ready",
            source_text=source_text,
            translated_text=translated_text,
            provider_name=provider_name,
            can_copy=bool(translated_text),
            can_retry=True,
        )
        return self._state

    def show_empty_clipboard(self) -> ClipboardTranslationState:
        self._state = ClipboardTranslationState(
            status=ClipboardTranslationStatus.EMPTY,
            status_text="Clipboard is empty",
            error_message="Copy text before translating.",
            can_retry=True,
        )
        return self._state

    def show_error(self, message: str, *, source_text: str = "") -> ClipboardTranslationState:
        self._state = ClipboardTranslationState(
            status=ClipboardTranslationStatus.ERROR,
            status_text="Translation failed",
            source_text=source_text,
            error_message=message,
            can_retry=True,
        )
        return self._state

    def copy_result(self) -> bool:
        if not self._state.can_copy or not self._state.translated_text:
            return False
        if self._on_copy_result is not None:
            self._on_copy_result(self._state.translated_text)
        return True

    def close_result(self) -> ClipboardTranslationState:
        return self.reset()

    async def translate_clipboard(
        self,
        *,
        clipboard_service: ClipboardService,
        pipeline: TranslationPipelineLike,
    ) -> ClipboardTranslationState:
        source_text = clipboard_service.get_text()
        if not source_text.strip():
            return self.show_empty_clipboard()

        self.request_clipboard_translation()
        response = await pipeline.translate_text_async(source_text)
        return self.show_success(
            source_text=source_text,
            translated_text=response.translated_text,
            provider_name=response.provider_name,
        )
