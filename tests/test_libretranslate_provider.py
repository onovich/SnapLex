from __future__ import annotations

import json

import pytest

from snaplex.errors import (
    MissingProviderCredentialError,
    StaleTranslationResultError,
    TranslationProviderError,
    TranslationProviderTimeoutError,
    UnsupportedLanguageError,
)
from snaplex.providers import TranslationRequest
from snaplex.providers.config import ProviderRuntimeConfig
from snaplex.providers.http import (
    HttpRequest,
    HttpResponse,
    HttpTransportError,
    HttpTransportTimeout,
)
from snaplex.providers.libretranslate import LibreTranslateProvider


class RecordingTransport:
    def __init__(self, response: HttpResponse | Exception) -> None:
        self.response = response
        self.requests: list[HttpRequest] = []

    def send(self, request: HttpRequest) -> HttpResponse:
        self.requests.append(request)
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


def make_provider(
    response: HttpResponse | Exception,
    *,
    config: ProviderRuntimeConfig | None = None,
    environ: dict[str, str] | None = None,
) -> tuple[LibreTranslateProvider, RecordingTransport]:
    transport = RecordingTransport(response)
    provider = LibreTranslateProvider(
        config=config or ProviderRuntimeConfig(base_url="https://libre.example"),
        transport=transport,
        environ=environ,
    )
    return provider, transport


def request_body(transport: RecordingTransport) -> dict[str, object]:
    body = transport.requests[0].body
    assert body is not None
    payload = json.loads(body.decode("utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_libretranslate_provider_translates_successfully() -> None:
    provider, transport = make_provider(HttpResponse(200, b'{"translatedText":"hola"}'))

    result = provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))

    assert result.translated_text == "hola"
    assert result.provider_name == "libretranslate"
    assert result.source_lang == "en"
    assert result.target_lang == "es"
    sent_request = transport.requests[0]
    assert sent_request.method == "POST"
    assert sent_request.url == "https://libre.example/translate"
    assert sent_request.timeout_seconds == 10.0
    assert request_body(transport) == {
        "q": "hello",
        "source": "en",
        "target": "es",
        "format": "text",
    }


def test_libretranslate_provider_includes_configured_api_key() -> None:
    config = ProviderRuntimeConfig(
        base_url="https://libre.example/",
        api_key_env_var="SNAPLEX_LIBRETRANSLATE_API_KEY",
        timeout_seconds=2.0,
    )
    provider, transport = make_provider(
        HttpResponse(200, b'{"translatedText":"bonjour"}'),
        config=config,
        environ={"SNAPLEX_LIBRETRANSLATE_API_KEY": " libre-secret "},
    )

    provider.translate(TranslationRequest("hello", source_lang="en", target_lang="fr"))

    assert transport.requests[0].url == "https://libre.example/translate"
    assert transport.requests[0].timeout_seconds == 2.0
    assert request_body(transport)["api_key"] == "libre-secret"


def test_libretranslate_provider_raises_when_configured_api_key_is_missing() -> None:
    config = ProviderRuntimeConfig(
        base_url="https://libre.example",
        api_key_env_var="SNAPLEX_LIBRETRANSLATE_API_KEY",
    )
    provider, transport = make_provider(HttpResponse(200, b"{}"), config=config, environ={})

    with pytest.raises(MissingProviderCredentialError) as exc_info:
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="fr"))

    assert exc_info.value.provider_name == "libretranslate"
    assert exc_info.value.env_var == "SNAPLEX_LIBRETRANSLATE_API_KEY"
    assert transport.requests == []


def test_libretranslate_provider_maps_timeout() -> None:
    provider, _transport = make_provider(HttpTransportTimeout("timed out"))

    with pytest.raises(TranslationProviderTimeoutError):
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))


def test_libretranslate_provider_maps_network_error() -> None:
    provider, _transport = make_provider(HttpTransportError("connection refused"))

    with pytest.raises(TranslationProviderError) as exc_info:
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))

    assert exc_info.value.provider_name == "libretranslate"


def test_libretranslate_provider_maps_bad_request_to_unsupported_language() -> None:
    provider, _transport = make_provider(HttpResponse(400, b'{"error":"unsupported language"}'))

    with pytest.raises(UnsupportedLanguageError) as exc_info:
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="xx"))

    assert exc_info.value.source_lang == "en"
    assert exc_info.value.target_lang == "xx"


def test_libretranslate_provider_maps_http_error() -> None:
    provider, _transport = make_provider(HttpResponse(503, b'{"error":"unavailable"}'))

    with pytest.raises(TranslationProviderError) as exc_info:
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))

    assert exc_info.value.provider_name == "libretranslate"


def test_libretranslate_provider_maps_malformed_json() -> None:
    provider, _transport = make_provider(HttpResponse(200, b"not json"))

    with pytest.raises(StaleTranslationResultError):
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))


def test_libretranslate_provider_maps_missing_translated_text() -> None:
    provider, _transport = make_provider(HttpResponse(200, b'{"translated_text":"hola"}'))

    with pytest.raises(StaleTranslationResultError):
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))


def test_libretranslate_provider_requires_base_url() -> None:
    provider, _transport = make_provider(
        HttpResponse(200, b"{}"),
        config=ProviderRuntimeConfig(),
    )

    with pytest.raises(TranslationProviderError) as exc_info:
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))

    assert exc_info.value.provider_name == "libretranslate"
