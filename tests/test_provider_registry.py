import pytest

from snaplex.errors import (
    MissingProviderCredentialError,
    TranslationProviderTimeoutError,
    UnknownTranslationProviderError,
)
from snaplex.providers import (
    FakeTranslationProvider,
    ProviderRegistry,
    RetryingTranslationProvider,
    TranslationRequest,
    TranslationResponse,
    create_default_provider_registry,
)
from snaplex.providers.config import ProviderRuntimeConfig
from snaplex.providers.http import HttpRequest, HttpResponse, HttpTransportTimeout
from snaplex.storage import AppConfig


def test_registry_returns_registered_provider() -> None:
    provider = FakeTranslationProvider(name="local")
    registry = ProviderRegistry([provider])

    assert registry.get("local") is provider
    assert registry.names() == ("local",)


def test_registry_replaces_provider_by_name() -> None:
    old_provider = FakeTranslationProvider(name="fake", translations={"hello": "old"})
    new_provider = FakeTranslationProvider(name="fake", translations={"hello": "new"})
    registry = ProviderRegistry([old_provider])

    registry.register(new_provider)

    assert registry.get("fake") is new_provider


def test_registry_raises_for_unknown_provider() -> None:
    registry = ProviderRegistry()

    with pytest.raises(UnknownTranslationProviderError) as exc_info:
        registry.get("missing")

    assert exc_info.value.code == "unknown_provider"
    assert exc_info.value.provider_name == "missing"


def test_registry_resolves_provider_order() -> None:
    first = FakeTranslationProvider(name="first")
    second = FakeTranslationProvider(name="second")
    registry = ProviderRegistry([first, second])

    assert registry.resolve_order(["second", "first"]) == (second, first)


def test_default_registry_contains_fake_provider() -> None:
    registry = create_default_provider_registry()

    assert registry.get("fake").name == "fake"
    assert registry.get("libretranslate").name == "libretranslate"
    assert registry.get("openai").name == "openai"
    assert registry.get("deepl").name == "deepl"


class FlakyProvider:
    name = "flaky"

    def __init__(self) -> None:
        self.calls = 0

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        self.calls += 1
        if self.calls == 1:
            raise TranslationProviderTimeoutError(provider_name=self.name)
        return TranslationResponse("ok", self.name, request.source_lang, request.target_lang)


class MissingCredentialProvider:
    name = "missing"

    def __init__(self) -> None:
        self.calls = 0

    def translate(self, _request: TranslationRequest) -> TranslationResponse:
        self.calls += 1
        raise MissingProviderCredentialError(
            env_var="SNAPLEX_MISSING_API_KEY",
            provider_name=self.name,
        )


def test_retrying_provider_retries_provider_failures() -> None:
    provider = FlakyProvider()
    retrying_provider = RetryingTranslationProvider(provider, retry_count=1)

    result = retrying_provider.translate(TranslationRequest("hello"))

    assert result.translated_text == "ok"
    assert provider.calls == 2


def test_retrying_provider_does_not_retry_missing_credentials() -> None:
    provider = MissingCredentialProvider()
    retrying_provider = RetryingTranslationProvider(provider, retry_count=3)

    with pytest.raises(MissingProviderCredentialError):
        retrying_provider.translate(TranslationRequest("hello"))

    assert provider.calls == 1


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


def test_default_registry_applies_provider_retry_count() -> None:
    transport = SequenceTransport(
        [
            HttpTransportTimeout("timed out"),
            HttpResponse(200, b'{"translatedText":"hola"}'),
        ],
    )
    config = AppConfig(
        provider_configs={
            "libretranslate": ProviderRuntimeConfig(
                base_url="https://libre.example",
                retry_count=1,
            ),
        },
    )
    registry = create_default_provider_registry(config, http_transport=transport)

    result = registry.get("libretranslate").translate(
        TranslationRequest("hello", source_lang="en", target_lang="es"),
    )

    assert result.translated_text == "hola"
    assert len(transport.requests) == 2
