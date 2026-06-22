"""Deterministic translation provider for local development and tests."""

from __future__ import annotations

from collections.abc import Mapping
from enum import Enum

from snaplex.providers.base import (
    TranslationProviderError,
    TranslationRequest,
    TranslationResponse,
)
from snaplex.errors import (
    StaleTranslationResultError,
    TranslationProviderTimeoutError,
    UnsupportedLanguageError,
)


class FakeTranslationScenario(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    UNSUPPORTED_LANGUAGE = "unsupported_language"
    STALE_RESULT = "stale_result"


class FakeTranslationProvider:
    def __init__(
        self,
        translations: Mapping[str, str] | None = None,
        *,
        name: str = "fake",
        fail: bool = False,
        scenario: FakeTranslationScenario = FakeTranslationScenario.SUCCESS,
    ) -> None:
        self.name = name
        self._translations = dict(translations or {})
        self._scenario = FakeTranslationScenario.FAILURE if fail else scenario

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        if self._scenario == FakeTranslationScenario.FAILURE:
            raise TranslationProviderError(
                "Fake translation provider was configured to fail.",
                provider_name=self.name,
            )
        if self._scenario == FakeTranslationScenario.TIMEOUT:
            raise TranslationProviderTimeoutError(provider_name=self.name)
        if self._scenario == FakeTranslationScenario.UNSUPPORTED_LANGUAGE:
            raise UnsupportedLanguageError(
                source_lang=request.source_lang,
                target_lang=request.target_lang,
                provider_name=self.name,
            )
        if self._scenario == FakeTranslationScenario.STALE_RESULT:
            raise StaleTranslationResultError(provider_name=self.name)

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
