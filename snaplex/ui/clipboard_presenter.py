"""Clipboard translation presentation state."""

from __future__ import annotations

from collections.abc import Callable

from snaplex.services import ClipboardError, ClipboardService
from snaplex.ui.translation_result import (
    TranslationPipelineLike,
    TranslationResultPresenter,
    TranslationResultState,
    TranslationResultStatus,
    friendly_translation_error_message,
)

ClipboardTranslationStatus = TranslationResultStatus
ClipboardTranslationState = TranslationResultState


class ClipboardTranslationPresenter(TranslationResultPresenter):
    def __init__(
        self,
        on_translate_requested: Callable[[], None] | None = None,
        on_copy_result: Callable[[str], None] | None = None,
    ) -> None:
        super().__init__(
            loading_status_text="Translating clipboard...",
            on_translate_requested=on_translate_requested,
            on_copy_result=on_copy_result,
        )

    def request_clipboard_translation(
        self,
        *,
        source_text: str = "",
    ) -> ClipboardTranslationState:
        return self.request_translation(source_text=source_text)

    def show_empty_clipboard(self) -> ClipboardTranslationState:
        return self.show_empty(
            status_text="Clipboard is empty",
            message="Copy text before translating.",
        )

    async def translate_clipboard(
        self,
        *,
        clipboard_service: ClipboardService,
        pipeline: TranslationPipelineLike,
    ) -> ClipboardTranslationState:
        try:
            source_text = clipboard_service.get_text()
        except ClipboardError as exc:
            return self.show_error(_friendly_clipboard_error_message(exc))

        if not source_text.strip():
            return self.show_empty_clipboard()

        return await self.translate_source_text(source_text=source_text, pipeline=pipeline)

    async def retry_translation(
        self,
        *,
        clipboard_service: ClipboardService,
        pipeline: TranslationPipelineLike,
    ) -> ClipboardTranslationState:
        source_text = self._state.source_text
        if source_text.strip():
            return await self.translate_source_text(
                source_text=source_text,
                pipeline=pipeline,
            )

        return await self.translate_clipboard(
            clipboard_service=clipboard_service,
            pipeline=pipeline,
        )


def _friendly_clipboard_error_message(error: Exception) -> str:
    if isinstance(error, ClipboardError):
        return "Could not read the clipboard. Copy the text again."

    return friendly_translation_error_message(error)
