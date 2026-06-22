"""Translation provider contracts and local implementations."""

from snaplex.providers.base import (
    TranslationProvider,
    TranslationRequest,
    TranslationResponse,
)
from snaplex.providers.fake import FakeTranslationProvider, FakeTranslationScenario
from snaplex.providers.registry import ProviderRegistry, create_default_provider_registry
from snaplex.errors import (
    StaleTranslationResultError,
    TranslationProviderError,
    TranslationProviderTimeoutError,
    UnsupportedLanguageError,
)

__all__ = [
    "FakeTranslationProvider",
    "FakeTranslationScenario",
    "ProviderRegistry",
    "StaleTranslationResultError",
    "TranslationProvider",
    "TranslationProviderError",
    "TranslationProviderTimeoutError",
    "TranslationRequest",
    "TranslationResponse",
    "UnsupportedLanguageError",
    "create_default_provider_registry",
]
