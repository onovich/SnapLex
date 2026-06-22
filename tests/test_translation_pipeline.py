import asyncio

import pytest

from snaplex.errors import (
    FallbackExhaustedError,
    MissingProviderCredentialError,
    TranslationProviderTimeoutError,
    TranslationProviderError,
    UnknownTranslationProviderError,
    UnsupportedLanguageError,
)
from snaplex.providers import (
    FakeTranslationProvider,
    FakeTranslationScenario,
    ProviderRegistry,
    TranslationRequest,
    TranslationResponse,
)
from snaplex.services import TranslationPipeline, create_default_translation_pipeline
from snaplex.services.translation_cache import InMemoryTranslationCache, TranslationCacheKey
from snaplex.storage import AppConfig, InMemoryConfigStore
from snaplex.providers.config import ProviderRuntimeConfig
from snaplex.providers.http import HttpRequest, HttpResponse, HttpTransportTimeout


def make_pipeline(
    config: AppConfig,
    *providers: FakeTranslationProvider,
    cache: InMemoryTranslationCache | None = None,
) -> TranslationPipeline:
    return TranslationPipeline(
        config_store=InMemoryConfigStore(config),
        provider_registry=ProviderRegistry(providers),
        cache=cache,
    )


def test_pipeline_translates_with_configured_provider() -> None:
    pipeline = make_pipeline(
        AppConfig(provider_name="local", target_lang="es"),
        FakeTranslationProvider(name="local", translations={"Hello world": "Hola mundo"}),
    )

    result = pipeline.translate_text("  Hello    world  ")

    assert result.translated_text == "Hola mundo"
    assert result.provider_name == "local"
    assert result.source_lang == "auto"
    assert result.target_lang == "es"


def test_pipeline_allows_language_overrides() -> None:
    pipeline = make_pipeline(
        AppConfig(provider_name="fake", source_lang="auto", target_lang="en"),
        FakeTranslationProvider(name="fake"),
    )

    result = pipeline.translate_text("hello", source_lang="fr", target_lang="de")

    assert result.source_lang == "fr"
    assert result.target_lang == "de"


def test_pipeline_returns_empty_result_without_provider_call() -> None:
    pipeline = make_pipeline(
        AppConfig(provider_name="fake"),
        FakeTranslationProvider(name="fake", scenario=FakeTranslationScenario.FAILURE),
    )

    result = pipeline.translate_text("   ")

    assert result.translated_text == ""
    assert result.provider_name == "fake"


def test_pipeline_raises_for_unknown_provider() -> None:
    pipeline = make_pipeline(AppConfig(provider_name="missing"))

    with pytest.raises(UnknownTranslationProviderError) as exc_info:
        pipeline.translate_text("hello")

    assert exc_info.value.provider_name == "missing"


def test_pipeline_maps_provider_failure_to_fallback_exhaustion() -> None:
    pipeline = make_pipeline(
        AppConfig(provider_name="fake"),
        FakeTranslationProvider(name="fake", scenario=FakeTranslationScenario.FAILURE),
    )

    with pytest.raises(FallbackExhaustedError) as exc_info:
        pipeline.translate_text("hello")

    assert len(exc_info.value.provider_errors) == 1
    assert isinstance(exc_info.value.provider_errors[0], TranslationProviderError)
    assert exc_info.value.provider_errors[0].provider_name == "fake"


def test_pipeline_maps_unsupported_language_to_fallback_exhaustion() -> None:
    pipeline = make_pipeline(
        AppConfig(provider_name="fake"),
        FakeTranslationProvider(
            name="fake",
            scenario=FakeTranslationScenario.UNSUPPORTED_LANGUAGE,
        ),
    )

    with pytest.raises(FallbackExhaustedError) as exc_info:
        pipeline.translate_text("hello", source_lang="en", target_lang="xx")

    error = exc_info.value.provider_errors[0]
    assert isinstance(error, UnsupportedLanguageError)
    assert error.source_lang == "en"
    assert error.target_lang == "xx"


def test_default_pipeline_uses_fake_provider() -> None:
    pipeline = create_default_translation_pipeline()

    result = pipeline.translate_text("hello")

    assert result.translated_text == "hello [en]"
    assert result.provider_name == "fake"


def test_pipeline_returns_cached_response_before_provider_call() -> None:
    cache = InMemoryTranslationCache()
    cache_key = TranslationCacheKey("hello", "auto", "en", "fake")
    cache.set(cache_key, TranslationResponse("cached", "fake", "auto", "en"))
    assert cache_key == TranslationCacheKey.from_request(
        TranslationRequest("hello"),
        provider_name="fake",
    )
    pipeline = make_pipeline(
        AppConfig(provider_name="fake"),
        FakeTranslationProvider(name="fake", scenario=FakeTranslationScenario.FAILURE),
        cache=cache,
    )

    result = pipeline.translate_text("hello")

    assert result.translated_text == "cached"


def test_pipeline_writes_successful_response_to_cache() -> None:
    cache = InMemoryTranslationCache()
    pipeline = make_pipeline(
        AppConfig(provider_name="fake"),
        FakeTranslationProvider(name="fake", translations={"hello": "hola"}),
        cache=cache,
    )

    result = pipeline.translate_text("hello")

    cache_key = TranslationCacheKey("hello", "auto", "en", "fake")
    assert cache.get(cache_key) == result


def test_pipeline_uses_provider_order_for_fallback_success() -> None:
    pipeline = make_pipeline(
        AppConfig(provider_name="primary", provider_order=("primary", "backup")),
        FakeTranslationProvider(name="primary", scenario=FakeTranslationScenario.FAILURE),
        FakeTranslationProvider(name="backup", translations={"hello": "backup result"}),
    )

    result = pipeline.translate_text("hello")

    assert result.translated_text == "backup result"
    assert result.provider_name == "backup"


def test_pipeline_can_fallback_after_provider_timeout() -> None:
    pipeline = make_pipeline(
        AppConfig(provider_name="primary", provider_order=("primary", "backup")),
        FakeTranslationProvider(name="primary", scenario=FakeTranslationScenario.TIMEOUT),
        FakeTranslationProvider(name="backup", translations={"hello": "after timeout"}),
    )

    result = pipeline.translate_text("hello")

    assert result.translated_text == "after timeout"
    assert result.provider_name == "backup"


def test_pipeline_does_not_cache_failed_response() -> None:
    cache = InMemoryTranslationCache()
    pipeline = make_pipeline(
        AppConfig(provider_name="fake"),
        FakeTranslationProvider(name="fake", scenario=FakeTranslationScenario.FAILURE),
        cache=cache,
    )

    with pytest.raises(FallbackExhaustedError):
        pipeline.translate_text("hello")

    assert len(cache) == 0


def test_pipeline_timeout_exhaustion_preserves_timeout_error() -> None:
    pipeline = make_pipeline(
        AppConfig(provider_name="fake"),
        FakeTranslationProvider(name="fake", scenario=FakeTranslationScenario.TIMEOUT),
    )

    with pytest.raises(FallbackExhaustedError) as exc_info:
        pipeline.translate_text("hello")

    assert isinstance(exc_info.value.provider_errors[0], TranslationProviderTimeoutError)


def test_pipeline_async_boundary_returns_translation() -> None:
    pipeline = make_pipeline(
        AppConfig(provider_name="fake"),
        FakeTranslationProvider(name="fake", translations={"hello": "async hello"}),
    )

    result = asyncio.run(pipeline.translate_text_async("hello"))

    assert result.translated_text == "async hello"
    assert result.provider_name == "fake"


def test_pipeline_async_boundary_propagates_errors() -> None:
    pipeline = make_pipeline(
        AppConfig(provider_name="fake"),
        FakeTranslationProvider(name="fake", scenario=FakeTranslationScenario.TIMEOUT),
    )

    with pytest.raises(FallbackExhaustedError):
        asyncio.run(pipeline.translate_text_async("hello"))


class SequenceTransport:
    def __init__(self, responses: list[HttpResponse | Exception]) -> None:
        self.responses = responses
        self.requests: list[HttpRequest] = []

    def send(self, request: HttpRequest) -> HttpResponse:
        self.requests.append(request)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def test_default_pipeline_can_use_configured_libretranslate_provider() -> None:
    transport = SequenceTransport([HttpResponse(200, b'{"translatedText":"hola"}')])
    config = AppConfig(
        provider_name="libretranslate",
        provider_order=("libretranslate",),
        provider_configs={
            "libretranslate": ProviderRuntimeConfig(base_url="https://libre.example"),
        },
    )
    pipeline = create_default_translation_pipeline(
        config_store=InMemoryConfigStore(config),
        http_transport=transport,
    )

    result = pipeline.translate_text("hello", source_lang="en", target_lang="es")

    assert result.translated_text == "hola"
    assert result.provider_name == "libretranslate"
    assert transport.requests[0].url == "https://libre.example/translate"


def test_default_pipeline_retries_then_falls_back_to_fake_provider() -> None:
    transport = SequenceTransport([HttpTransportTimeout("timed out")])
    config = AppConfig(
        provider_name="libretranslate",
        provider_order=("libretranslate", "fake"),
        provider_configs={
            "libretranslate": ProviderRuntimeConfig(
                base_url="https://libre.example",
                retry_count=0,
            ),
        },
    )
    pipeline = create_default_translation_pipeline(
        config_store=InMemoryConfigStore(config),
        http_transport=transport,
    )

    result = pipeline.translate_text("hello")

    assert result.provider_name == "fake"
    assert result.translated_text == "hello [en]"


def test_default_pipeline_preserves_missing_credential_on_exhaustion() -> None:
    config = AppConfig(
        provider_name="openai",
        provider_order=("openai",),
        provider_configs={
            "openai": ProviderRuntimeConfig(
                base_url="https://api.openai.example/v1",
                api_key_env_var="SNAPLEX_OPENAI_API_KEY",
            ),
        },
    )
    pipeline = create_default_translation_pipeline(config_store=InMemoryConfigStore(config))

    with pytest.raises(FallbackExhaustedError) as exc_info:
        pipeline.translate_text("hello")

    assert isinstance(exc_info.value.provider_errors[0], MissingProviderCredentialError)


def test_default_pipeline_uses_updated_config_store_provider_settings() -> None:
    transport = SequenceTransport([HttpResponse(200, b'{"translatedText":"hola"}')])
    store = InMemoryConfigStore()
    pipeline = create_default_translation_pipeline(
        config_store=store,
        http_transport=transport,
    )
    store.save(
        AppConfig(
            provider_name="libretranslate",
            provider_order=("libretranslate",),
            provider_configs={
                "libretranslate": ProviderRuntimeConfig(base_url="https://libre.example"),
            },
        )
    )

    result = pipeline.translate_text("hello", source_lang="en", target_lang="es")

    assert result.translated_text == "hola"
    assert result.provider_name == "libretranslate"
