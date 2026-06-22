"""Translation pipeline and provider error taxonomy."""

from __future__ import annotations


class TranslationError(RuntimeError):
    """Base class for expected translation pipeline failures."""

    code = "translation_error"
    default_message = "Translation failed."

    def __init__(self, message: str | None = None, *, provider_name: str | None = None) -> None:
        self.message = message or self.default_message
        self.provider_name = provider_name
        super().__init__(self.message)


class EmptyTranslationInputError(TranslationError):
    """Raised when a pipeline requires text but receives only empty input."""

    code = "empty_input"
    default_message = "Translation input is empty."


class TranslationProviderError(TranslationError):
    """Raised when a translation provider cannot produce a result."""

    code = "provider_failure"
    default_message = "Translation provider failed."


class TranslationProviderTimeoutError(TranslationProviderError):
    """Raised when a translation provider times out."""

    code = "provider_timeout"
    default_message = "Translation provider timed out."


class UnsupportedLanguageError(TranslationProviderError):
    """Raised when a provider does not support the requested language pair."""

    code = "unsupported_language"
    default_message = "Translation language pair is not supported."

    def __init__(
        self,
        message: str | None = None,
        *,
        source_lang: str,
        target_lang: str,
        provider_name: str | None = None,
    ) -> None:
        self.source_lang = source_lang
        self.target_lang = target_lang
        super().__init__(message, provider_name=provider_name)


class StaleTranslationResultError(TranslationProviderError):
    """Raised when a provider returns a stale or otherwise invalid result."""

    code = "stale_result"
    default_message = "Translation provider returned a stale result."


class UnknownTranslationProviderError(TranslationError):
    """Raised when config requests a provider that is not registered."""

    code = "unknown_provider"
    default_message = "Translation provider is not registered."


class FallbackExhaustedError(TranslationError):
    """Raised when all configured providers fail."""

    code = "fallback_exhausted"
    default_message = "All translation providers failed."

    def __init__(
        self,
        message: str | None = None,
        *,
        provider_errors: tuple[TranslationError, ...] = (),
    ) -> None:
        self.provider_errors = provider_errors
        super().__init__(message)
