"""Translation provider contracts and local implementations."""

from snaplex.providers.base import (
    TranslationProvider,
    TranslationRequest,
    TranslationResponse,
)
from snaplex.providers.config import (
    ProviderRuntimeConfig,
    copy_provider_runtime_configs,
    default_provider_runtime_configs,
    provider_credential_reference,
    resolve_api_key,
)
from snaplex.providers.deepl import DeepLTranslationProvider
from snaplex.providers.fake import FakeTranslationProvider, FakeTranslationScenario
from snaplex.providers.http import (
    HttpRequest,
    HttpResponse,
    HttpTransport,
    HttpTransportError,
    HttpTransportTimeout,
    UrllibHttpTransport,
)
from snaplex.providers.libretranslate import LibreTranslateProvider
from snaplex.providers.openai import OpenAITranslationProvider
from snaplex.providers.registry import ProviderRegistry, create_default_provider_registry
from snaplex.providers.retry import RetryingTranslationProvider
from snaplex.errors import (
    MissingProviderCredentialError,
    StaleTranslationResultError,
    TranslationProviderError,
    TranslationProviderTimeoutError,
    UnsupportedLanguageError,
)

__all__ = [
    "FakeTranslationProvider",
    "FakeTranslationScenario",
    "HttpRequest",
    "HttpResponse",
    "HttpTransport",
    "HttpTransportError",
    "HttpTransportTimeout",
    "LibreTranslateProvider",
    "MissingProviderCredentialError",
    "OpenAITranslationProvider",
    "ProviderRegistry",
    "ProviderRuntimeConfig",
    "DeepLTranslationProvider",
    "RetryingTranslationProvider",
    "StaleTranslationResultError",
    "TranslationProvider",
    "TranslationProviderError",
    "TranslationProviderTimeoutError",
    "TranslationRequest",
    "TranslationResponse",
    "UnsupportedLanguageError",
    "UrllibHttpTransport",
    "copy_provider_runtime_configs",
    "create_default_provider_registry",
    "default_provider_runtime_configs",
    "provider_credential_reference",
    "resolve_api_key",
]
