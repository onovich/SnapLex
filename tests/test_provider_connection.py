from __future__ import annotations

from snaplex.providers.config import ProviderRuntimeConfig
from snaplex.providers.http import (
    HttpRequest,
    HttpResponse,
    HttpTransportError,
    HttpTransportTimeout,
)
from snaplex.services import (
    CredentialService,
    CredentialSource,
    InMemoryCredentialStore,
    SettingsService,
    keyring_credential_reference,
)
from snaplex.services.provider_setup import ProviderSetupStatus
from snaplex.storage import AppConfig, InMemoryConfigStore
from snaplex.ui.settings_presenter import SettingsPresenter


class RecordingTransport:
    def __init__(self, response: HttpResponse | Exception) -> None:
        self.response = response
        self.requests: list[HttpRequest] = []

    def send(self, request: HttpRequest) -> HttpResponse:
        self.requests.append(request)
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


def test_provider_connection_passes_for_mocked_openai_without_exposing_secret() -> None:
    transport = RecordingTransport(HttpResponse(200, b'{"output_text":"hola"}'))
    service = SettingsService(
        InMemoryConfigStore(
            AppConfig(
                provider_configs={
                    "openai": ProviderRuntimeConfig(
                        base_url="https://api.openai.example/v1",
                        api_key_env_var="OPENAI_API_KEY",
                        options={"model": "gpt-test"},
                    )
                }
            )
        )
    )

    result = service.test_provider_connection(
        "openai",
        http_transport=transport,
        environ={"OPENAI_API_KEY": "secret-value"},
    )

    assert result.status == ProviderSetupStatus.TEST_PASSED
    assert result.translated_text == "hola"
    assert transport.requests[0].url == "https://api.openai.example/v1/responses"
    assert "secret-value" not in repr(result)


def test_provider_connection_passes_for_mocked_openai_keyring_without_exposing_secret() -> None:
    transport = RecordingTransport(HttpResponse(200, b'{"output_text":"hola"}'))
    reference = keyring_credential_reference("openai")
    credential_store = InMemoryCredentialStore()
    credential_store.save(reference, "keyring-secret")
    service = SettingsService(
        InMemoryConfigStore(
            AppConfig(
                provider_configs={
                    "openai": ProviderRuntimeConfig(
                        base_url="https://api.openai.example/v1",
                        credential_source="keyring",
                        options={"model": "gpt-test"},
                    )
                }
            )
        )
    )

    result = service.test_provider_connection(
        "openai",
        http_transport=transport,
        environ={},
        credential_service=CredentialService({CredentialSource.KEYRING: credential_store}),
    )

    assert result.status == ProviderSetupStatus.TEST_PASSED
    assert transport.requests[0].headers["Authorization"] == "Bearer keyring-secret"
    assert "keyring-secret" not in repr(result)


def test_provider_connection_passes_for_mocked_deepl() -> None:
    transport = RecordingTransport(
        HttpResponse(200, b'{"translations":[{"text":"hola"}]}'),
    )
    service = SettingsService(
        InMemoryConfigStore(
            AppConfig(
                provider_configs={
                    "deepl": ProviderRuntimeConfig(
                        base_url="https://api-free.deepl.example/v2",
                        api_key_env_var="DEEPL_API_KEY",
                    )
                }
            )
        )
    )

    result = service.test_provider_connection(
        "deepl",
        http_transport=transport,
        environ={"DEEPL_API_KEY": "secret-value"},
    )

    assert result.status == ProviderSetupStatus.TEST_PASSED
    assert result.provider_name == "deepl"
    assert transport.requests[0].url == "https://api-free.deepl.example/v2/translate"


def test_provider_connection_passes_for_mocked_libretranslate_without_key() -> None:
    transport = RecordingTransport(HttpResponse(200, b'{"translatedText":"hola"}'))
    service = SettingsService(
        InMemoryConfigStore(
            AppConfig(
                provider_configs={
                    "libretranslate": ProviderRuntimeConfig(
                        base_url="https://libre.example",
                    )
                }
            )
        )
    )

    result = service.test_provider_connection("libretranslate", http_transport=transport)

    assert result.status == ProviderSetupStatus.TEST_PASSED
    assert transport.requests[0].url == "https://libre.example/translate"


def test_provider_connection_rejects_missing_credential_before_http() -> None:
    transport = RecordingTransport(HttpResponse(200, b'{"output_text":"hola"}'))
    service = SettingsService(
        InMemoryConfigStore(
            AppConfig(
                provider_configs={
                    "openai": ProviderRuntimeConfig(
                        base_url="https://api.openai.example/v1",
                        api_key_env_var="OPENAI_API_KEY",
                    )
                }
            )
        )
    )

    result = service.test_provider_connection("openai", http_transport=transport, environ={})

    assert result.status == ProviderSetupStatus.MISSING_CREDENTIAL
    assert transport.requests == []


def test_provider_connection_reports_fake_as_smoke_mode_without_http() -> None:
    transport = RecordingTransport(HttpResponse(200, b'{"output_text":"hola"}'))
    service = SettingsService(InMemoryConfigStore())

    result = service.test_provider_connection("fake", http_transport=transport)

    assert result.status == ProviderSetupStatus.FAKE_SMOKE
    assert "not real translation" in result.detail_text
    assert transport.requests == []


def test_provider_connection_maps_timeout_to_endpoint_unavailable() -> None:
    transport = RecordingTransport(HttpTransportTimeout("timed out"))
    service = SettingsService(
        InMemoryConfigStore(
            AppConfig(
                provider_configs={
                    "openai": ProviderRuntimeConfig(
                        base_url="https://api.openai.example/v1",
                        api_key_env_var="OPENAI_API_KEY",
                    )
                }
            )
        )
    )

    result = service.test_provider_connection(
        "openai",
        http_transport=transport,
        environ={"OPENAI_API_KEY": "secret-value"},
    )

    assert result.status == ProviderSetupStatus.ENDPOINT_UNAVAILABLE
    assert "timed out" in result.status_text


def test_provider_connection_maps_network_error_to_test_failed() -> None:
    transport = RecordingTransport(HttpTransportError("connection refused"))
    service = SettingsService(
        InMemoryConfigStore(
            AppConfig(
                provider_configs={
                    "libretranslate": ProviderRuntimeConfig(base_url="https://libre.example")
                }
            )
        )
    )

    result = service.test_provider_connection("libretranslate", http_transport=transport)

    assert result.status == ProviderSetupStatus.TEST_FAILED
    assert "endpoint" in result.detail_text


def test_provider_connection_maps_http_error_to_test_failed() -> None:
    transport = RecordingTransport(HttpResponse(401, b'{"error":{"message":"bad key"}}'))
    service = SettingsService(
        InMemoryConfigStore(
            AppConfig(
                provider_configs={"openai": ProviderRuntimeConfig(api_key_env_var="OPENAI_API_KEY")}
            )
        )
    )

    result = service.test_provider_connection(
        "openai",
        http_transport=transport,
        environ={"OPENAI_API_KEY": "secret-value"},
    )

    assert result.status == ProviderSetupStatus.TEST_FAILED
    assert "credential" in result.detail_text


def test_provider_connection_maps_malformed_response_to_test_failed() -> None:
    transport = RecordingTransport(HttpResponse(200, b"not-json"))
    service = SettingsService(
        InMemoryConfigStore(
            AppConfig(
                provider_configs={
                    "libretranslate": ProviderRuntimeConfig(base_url="https://libre.example")
                }
            )
        )
    )

    result = service.test_provider_connection("libretranslate", http_transport=transport)

    assert result.status == ProviderSetupStatus.TEST_FAILED
    assert result.status_text == "Unexpected provider response"


def test_provider_connection_maps_unsupported_language_to_test_failed() -> None:
    transport = RecordingTransport(HttpResponse(400, b'{"error":"unsupported language"}'))
    service = SettingsService(
        InMemoryConfigStore(
            AppConfig(
                provider_configs={
                    "libretranslate": ProviderRuntimeConfig(base_url="https://libre.example")
                }
            )
        )
    )

    result = service.test_provider_connection(
        "libretranslate",
        http_transport=transport,
        target_lang="xx",
    )

    assert result.status == ProviderSetupStatus.TEST_FAILED
    assert result.status_text == "Language pair not supported"


def test_settings_presenter_runs_provider_connection_test_through_service() -> None:
    transport = RecordingTransport(HttpResponse(200, b'{"output_text":"hola"}'))
    presenter = SettingsPresenter(
        SettingsService(
            InMemoryConfigStore(
                AppConfig(
                    provider_configs={
                        "openai": ProviderRuntimeConfig(
                            base_url="https://api.openai.example/v1",
                            api_key_env_var="OPENAI_API_KEY",
                        )
                    }
                )
            )
        )
    )

    result = presenter.test_provider_connection(
        "openai",
        http_transport=transport,
        environ={"OPENAI_API_KEY": "secret-value"},
    )

    assert result.status == ProviderSetupStatus.TEST_PASSED
