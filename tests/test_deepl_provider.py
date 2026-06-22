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
from snaplex.providers.deepl import DeepLTranslationProvider
from snaplex.providers.http import (
    HttpRequest,
    HttpResponse,
    HttpTransportError,
    HttpTransportTimeout,
)


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
) -> tuple[DeepLTranslationProvider, RecordingTransport]:
    transport = RecordingTransport(response)
    provider = DeepLTranslationProvider(
        config=config
        or ProviderRuntimeConfig(
            base_url="https://api-free.deepl.example/v2",
            api_key_env_var="SNAPLEX_DEEPL_API_KEY",
            timeout_seconds=5.0,
        ),
        transport=transport,
        environ={"SNAPLEX_DEEPL_API_KEY": "deepl-secret"} if environ is None else environ,
    )
    return provider, transport


def request_body(transport: RecordingTransport) -> dict[str, object]:
    body = transport.requests[0].body
    assert body is not None
    payload = json.loads(body.decode("utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_deepl_provider_translates_successfully() -> None:
    provider, transport = make_provider(
        HttpResponse(
            200,
            b'{"translations":[{"detected_source_language":"EN","text":"hola"}]}',
        ),
    )

    result = provider.translate(TranslationRequest("hello", source_lang="auto", target_lang="es"))

    assert result.translated_text == "hola"
    assert result.provider_name == "deepl"
    assert result.source_lang == "en"
    assert result.target_lang == "es"
    sent_request = transport.requests[0]
    assert sent_request.method == "POST"
    assert sent_request.url == "https://api-free.deepl.example/v2/translate"
    assert sent_request.headers["Authorization"] == "DeepL-Auth-Key deepl-secret"
    assert sent_request.timeout_seconds == 5.0
    assert request_body(transport) == {"text": ["hello"], "target_lang": "ES"}


def test_deepl_provider_sends_source_lang_and_options() -> None:
    config = ProviderRuntimeConfig(
        base_url="https://api-free.deepl.example/v2/",
        api_key_env_var="SNAPLEX_DEEPL_API_KEY",
        options={"model_type": "quality_optimized"},
    )
    provider, transport = make_provider(
        HttpResponse(200, b'{"translations":[{"text":"bonjour"}]}'),
        config=config,
    )

    provider.translate(TranslationRequest("hello", source_lang="en", target_lang="fr"))

    assert transport.requests[0].url == "https://api-free.deepl.example/v2/translate"
    assert request_body(transport) == {
        "text": ["hello"],
        "target_lang": "FR",
        "source_lang": "EN",
        "model_type": "quality_optimized",
    }


def test_deepl_provider_requires_configured_api_key() -> None:
    config = ProviderRuntimeConfig(
        base_url="https://api-free.deepl.example/v2",
        api_key_env_var="SNAPLEX_DEEPL_API_KEY",
    )
    provider, transport = make_provider(
        HttpResponse(200, b"{}"),
        config=config,
        environ={},
    )

    with pytest.raises(MissingProviderCredentialError) as exc_info:
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))

    assert exc_info.value.provider_name == "deepl"
    assert exc_info.value.env_var == "SNAPLEX_DEEPL_API_KEY"
    assert transport.requests == []


def test_deepl_provider_maps_timeout() -> None:
    provider, _transport = make_provider(HttpTransportTimeout("timed out"))

    with pytest.raises(TranslationProviderTimeoutError):
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))


def test_deepl_provider_maps_network_error() -> None:
    provider, _transport = make_provider(HttpTransportError("connection refused"))

    with pytest.raises(TranslationProviderError) as exc_info:
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))

    assert exc_info.value.provider_name == "deepl"


def test_deepl_provider_maps_language_error_to_unsupported_language() -> None:
    provider, _transport = make_provider(
        HttpResponse(400, b'{"message":"Value for target_lang is not supported."}'),
    )

    with pytest.raises(UnsupportedLanguageError) as exc_info:
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="xx"))

    assert exc_info.value.source_lang == "en"
    assert exc_info.value.target_lang == "xx"


def test_deepl_provider_maps_http_error() -> None:
    provider, _transport = make_provider(HttpResponse(403, b'{"message":"bad key"}'))

    with pytest.raises(TranslationProviderError) as exc_info:
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))

    assert exc_info.value.provider_name == "deepl"


def test_deepl_provider_maps_malformed_json() -> None:
    provider, _transport = make_provider(HttpResponse(200, b"not json"))

    with pytest.raises(StaleTranslationResultError):
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))


def test_deepl_provider_maps_missing_translation_text() -> None:
    provider, _transport = make_provider(HttpResponse(200, b'{"translations":[{}]}'))

    with pytest.raises(StaleTranslationResultError):
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))


def test_deepl_provider_requires_base_url() -> None:
    config = ProviderRuntimeConfig(api_key_env_var="SNAPLEX_DEEPL_API_KEY")
    provider, _transport = make_provider(
        HttpResponse(200, b"{}"),
        config=config,
    )

    with pytest.raises(TranslationProviderError) as exc_info:
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))

    assert exc_info.value.provider_name == "deepl"
