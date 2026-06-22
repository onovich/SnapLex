"""Translation provider contracts and local implementations."""

from snaplex.providers.base import (
    TranslationProvider,
    TranslationRequest,
    TranslationResponse,
)
from snaplex.providers.fake import FakeTranslationProvider
from snaplex.errors import (
    StaleTranslationResultError,
    TranslationProviderError,
    TranslationProviderTimeoutError,
    UnsupportedLanguageError,
)

__all__ = [
    "FakeTranslationProvider",
    "StaleTranslationResultError",
    "TranslationProvider",
    "TranslationProviderError",
    "TranslationProviderTimeoutError",
    "TranslationRequest",
    "TranslationResponse",
    "UnsupportedLanguageError",
]
