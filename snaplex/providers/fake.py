"""Deterministic translation provider for local development and tests."""

from __future__ import annotations

from collections.abc import Mapping

from snaplex.providers.base import (
    TranslationProviderError,
    TranslationRequest,
    TranslationResponse,
)


class FakeTranslationProvider:
    name = "fake"

    def __init__(
        self,
        translations: Mapping[str, str] | None = None,
        *,
        fail: bool = False,
    ) -> None:
        self._translations = dict(translations or {})
        self._fail = fail

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        if self._fail:
            raise TranslationProviderError("Fake translation provider was configured to fail.")

        translated_text = self._translations.get(
            request.text,
            f"{request.text} [{request.target_lang}]",
        )
        return TranslationResponse(
            translated_text=translated_text,
            provider_name=self.name,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
        )
