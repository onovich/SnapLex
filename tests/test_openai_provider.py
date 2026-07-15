from __future__ import annotations

import json

import pytest

from snaplex.credentials import (
    CredentialService,
    CredentialSource,
    InMemoryCredentialStore,
    keyring_credential_reference,
)
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
from snaplex.providers.openai import OpenAITranslationProvider


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
    credential_service: CredentialService | None = None,
) -> tuple[OpenAITranslationProvider, RecordingTransport]:
    transport = RecordingTransport(response)
    provider = OpenAITranslationProvider(
        config=config
        or ProviderRuntimeConfig(
            base_url="https://api.openai.example/v1",
            api_key_env_var="SNAPLEX_OPENAI_API_KEY",
            timeout_seconds=4.0,
            options={"model": "gpt-test"},
        ),
        transport=transport,
        environ={"SNAPLEX_OPENAI_API_KEY": "openai-secret"} if environ is None else environ,
        credential_service=credential_service,
    )
    return provider, transport


def request_body(transport: RecordingTransport) -> dict[str, object]:
    body = transport.requests[0].body
    assert body is not None
    payload = json.loads(body.decode("utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_openai_provider_translates_successfully() -> None:
    provider, transport = make_provider(HttpResponse(200, b'{"output_text":"hola"}'))

    result = provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))

    assert result.translated_text == "hola"
    assert result.provider_name == "openai"
    sent_request = transport.requests[0]
    assert sent_request.method == "POST"
    assert sent_request.url == "https://api.openai.example/v1/responses"
    assert sent_request.headers["Authorization"] == "Bearer openai-secret"
    assert sent_request.timeout_seconds == 4.0
    payload = request_body(transport)
    assert payload["model"] == "gpt-test"
    assert payload["input"] == "hello"
    assert payload["store"] is False
    assert "from en to es" in str(payload["instructions"])


def test_openai_provider_reads_nested_response_output_text() -> None:
    provider, _transport = make_provider(
        HttpResponse(
            200,
            b'{"output":[{"content":[{"type":"output_text","text":"hola mundo"}]}]}',
        ),
    )

    result = provider.translate(
        TranslationRequest("hello world", source_lang="en", target_lang="es")
    )

    assert result.translated_text == "hola mundo"


def test_openai_provider_requires_configured_api_key() -> None:
    config = ProviderRuntimeConfig(
        base_url="https://api.openai.example/v1",
        api_key_env_var="SNAPLEX_OPENAI_API_KEY",
    )
    provider, transport = make_provider(
        HttpResponse(200, b"{}"),
        config=config,
        environ={},
    )

    with pytest.raises(MissingProviderCredentialError) as exc_info:
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))

    assert exc_info.value.provider_name == "openai"
    assert exc_info.value.env_var == "SNAPLEX_OPENAI_API_KEY"
    assert transport.requests == []


def test_openai_provider_resolves_keyring_credential_without_secret_repr() -> None:
    reference = keyring_credential_reference("openai")
    credential_store = InMemoryCredentialStore()
    credential_store.save(reference, "keyring-secret")
    provider, transport = make_provider(
        HttpResponse(200, b'{"output_text":"hola"}'),
        config=ProviderRuntimeConfig(
            base_url="https://api.openai.example/v1",
            credential_source="keyring",
            options={"model": "gpt-test"},
        ),
        environ={},
        credential_service=CredentialService({CredentialSource.KEYRING: credential_store}),
    )

    result = provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))

    assert result.translated_text == "hola"
    assert transport.requests[0].headers["Authorization"] == "Bearer keyring-secret"
    assert "keyring-secret" not in repr(result)


def test_openai_provider_maps_timeout() -> None:
    provider, _transport = make_provider(HttpTransportTimeout("timed out"))

    with pytest.raises(TranslationProviderTimeoutError):
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))


def test_openai_provider_maps_network_error() -> None:
    provider, _transport = make_provider(HttpTransportError("connection refused"))

    with pytest.raises(TranslationProviderError) as exc_info:
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))

    assert exc_info.value.provider_name == "openai"


def test_openai_provider_maps_language_error_to_unsupported_language() -> None:
    provider, _transport = make_provider(
        HttpResponse(400, b'{"error":{"message":"unsupported language requested"}}'),
    )

    with pytest.raises(UnsupportedLanguageError) as exc_info:
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="xx"))

    assert exc_info.value.source_lang == "en"
    assert exc_info.value.target_lang == "xx"


def test_openai_provider_maps_http_error() -> None:
    provider, _transport = make_provider(HttpResponse(401, b'{"error":{"message":"bad key"}}'))

    with pytest.raises(TranslationProviderError) as exc_info:
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))

    assert exc_info.value.provider_name == "openai"


def test_openai_provider_maps_malformed_json() -> None:
    provider, _transport = make_provider(HttpResponse(200, b"not json"))

    with pytest.raises(StaleTranslationResultError):
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))


def test_openai_provider_maps_missing_output_text() -> None:
    provider, _transport = make_provider(HttpResponse(200, b'{"output":[]}'))

    with pytest.raises(StaleTranslationResultError):
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))


def test_openai_provider_requires_base_url() -> None:
    config = ProviderRuntimeConfig(api_key_env_var="SNAPLEX_OPENAI_API_KEY")
    provider, _transport = make_provider(
        HttpResponse(200, b"{}"),
        config=config,
    )

    with pytest.raises(TranslationProviderError) as exc_info:
        provider.translate(TranslationRequest("hello", source_lang="en", target_lang="es"))

    assert exc_info.value.provider_name == "openai"
