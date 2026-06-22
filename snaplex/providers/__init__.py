"""Translation provider contracts and local implementations."""

from snaplex.providers.base import (
    TranslationProvider,
    TranslationProviderError,
    TranslationRequest,
    TranslationResponse,
)
from snaplex.providers.fake import FakeTranslationProvider

__all__ = [
    "FakeTranslationProvider",
    "TranslationProvider",
    "TranslationProviderError",
    "TranslationRequest",
    "TranslationResponse",
]
