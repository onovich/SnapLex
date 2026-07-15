"""Shared translation result presentation state."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from snaplex.errors import (
    FallbackExhaustedError,
    StaleTranslationResultError,
    TranslationError,
    TranslationProviderError,
    TranslationProviderTimeoutError,
    UnknownTranslationProviderError,
    UnsupportedLanguageError,
)
from snaplex.providers import TranslationResponse


class TranslationResultStatus(str, Enum):
    IDLE = "idle"
    LOADING = "loading"
    SUCCESS = "success"
    EMPTY = "empty"
    ERROR = "error"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class TranslationResultState:
    status: TranslationResultStatus = TranslationResultStatus.IDLE
    status_text: str = "Ready"
    source_text: str = ""
    translated_text: str = ""
    provider_name: str = ""
    provider_notice: str = ""
    error_message: str = ""
    can_copy: bool = False
    can_retry: bool = False


class TranslationPipelineLike(Protocol):
    async def translate_text_async(self, text: str) -> TranslationResponse:
        """Translate text using the P1 pipeline async boundary."""
        ...


class TranslationHistoryRecorderLike(Protocol):
    def add_translation(
        self,
        *,
        source_text: str,
        translated_text: str,
        provider_name: str,
        source_lang: str,
        target_lang: str,
        flow: str,
    ) -> object | None:
        """Record one successful translation if history is enabled."""
        ...


class TranslationResultPresenter:
    def __init__(
        self,
        *,
        loading_status_text: str,
        on_translate_requested: Callable[[], None] | None = None,
        on_copy_result: Callable[[str], None] | None = None,
        history_service: TranslationHistoryRecorderLike | None = None,
    ) -> None:
        self._loading_status_text = loading_status_text
        self._on_translate_requested = on_translate_requested
        self._on_copy_result = on_copy_result
        self._history_service = history_service
        self._state = TranslationResultState()

    @property
    def state(self) -> TranslationResultState:
        return self._state

    def request_translation(
        self,
        *,
        source_text: str = "",
    ) -> TranslationResultState:
        self._state = TranslationResultState(
            status=TranslationResultStatus.LOADING,
            status_text=self._loading_status_text,
            source_text=source_text,
        )
        if self._on_translate_requested is not None:
            self._on_translate_requested()
        return self._state

    def reset(self) -> TranslationResultState:
        self._state = TranslationResultState()
        return self._state

    def show_success(
        self,
        *,
        source_text: str,
        translated_text: str,
        provider_name: str = "",
    ) -> TranslationResultState:
        self._state = TranslationResultState(
            status=TranslationResultStatus.SUCCESS,
            status_text="Translation ready",
            source_text=source_text,
            translated_text=translated_text,
            provider_name=provider_name,
            provider_notice=provider_notice_for(provider_name),
            can_copy=bool(translated_text),
            can_retry=True,
        )
        return self._state

    def show_empty(self, *, status_text: str, message: str) -> TranslationResultState:
        self._state = TranslationResultState(
            status=TranslationResultStatus.EMPTY,
            status_text=status_text,
            error_message=message,
            can_retry=True,
        )
        return self._state

    def show_error(self, message: str, *, source_text: str = "") -> TranslationResultState:
        self._state = TranslationResultState(
            status=TranslationResultStatus.ERROR,
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

    def close_result(self) -> TranslationResultState:
        return self.reset()

    async def translate_source_text(
        self,
        *,
        source_text: str,
        pipeline: TranslationPipelineLike,
        history_flow: str = "",
    ) -> TranslationResultState:
        self.request_translation(source_text=source_text)
        try:
            response = await pipeline.translate_text_async(source_text)
        except TranslationError as exc:
            return self.show_error(friendly_translation_error_message(exc), source_text=source_text)
        except Exception as exc:
            return self.show_error(friendly_translation_error_message(exc), source_text=source_text)

        self._record_history(
            source_text=source_text,
            translated_text=response.translated_text,
            provider_name=response.provider_name,
            source_lang=response.source_lang,
            target_lang=response.target_lang,
            flow=history_flow,
        )
        return self.show_success(
            source_text=source_text,
            translated_text=response.translated_text,
            provider_name=response.provider_name,
        )

    def _record_history(
        self,
        *,
        source_text: str,
        translated_text: str,
        provider_name: str,
        source_lang: str,
        target_lang: str,
        flow: str,
    ) -> None:
        if self._history_service is None or not flow:
            return
        try:
            self._history_service.add_translation(
                source_text=source_text,
                translated_text=translated_text,
                provider_name=provider_name,
                source_lang=source_lang,
                target_lang=target_lang,
                flow=flow,
            )
        except Exception:
            return


def friendly_translation_error_message(error: Exception) -> str:
    if isinstance(error, FallbackExhaustedError):
        return "All configured translation providers failed. Try again."

    if isinstance(error, TranslationProviderTimeoutError):
        return "Translation timed out. Try again."

    if isinstance(error, UnsupportedLanguageError):
        return f"Language pair {error.source_lang} -> {error.target_lang} is not supported."

    if isinstance(error, StaleTranslationResultError):
        return "Translation result was stale. Try again."

    if isinstance(error, UnknownTranslationProviderError):
        return "Configured translation provider is not available."

    if isinstance(error, TranslationProviderError):
        return "Translation provider failed. Try again."

    if isinstance(error, TranslationError):
        return "Translation failed. Try again."

    return "Translation failed unexpectedly. Try again."


def provider_notice_for(provider_name: str) -> str:
    if provider_name.strip().lower() == "fake":
        return "Fake smoke mode: deterministic placeholder output, not real translation."
    return ""
