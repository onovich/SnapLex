"""Retry wrapper for translation providers."""

from __future__ import annotations

from snaplex.errors import (
    MissingProviderCredentialError,
    TranslationProviderError,
    UnsupportedLanguageError,
)
from snaplex.providers.base import TranslationProvider, TranslationRequest, TranslationResponse


class RetryingTranslationProvider:
    """Retry transient provider failures before pipeline fallback moves on."""

    def __init__(self, provider: TranslationProvider, *, retry_count: int) -> None:
        self._provider = provider
        self.name = provider.name
        self._retry_count = max(0, retry_count)

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        remaining_attempts = self._retry_count + 1
        last_error: TranslationProviderError | None = None

        while remaining_attempts > 0:
            remaining_attempts -= 1
            try:
                return self._provider.translate(request)
            except (MissingProviderCredentialError, UnsupportedLanguageError):
                raise
            except TranslationProviderError as exc:
                last_error = exc
                if remaining_attempts == 0:
                    raise

        if last_error is not None:
            raise last_error
        raise TranslationProviderError(provider_name=self.name)
