"""Provider setup state for trial UX without reading or storing secrets."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum

from snaplex.errors import (
    MissingProviderCredentialError,
    StaleTranslationResultError,
    TranslationError,
    TranslationProviderError,
    TranslationProviderTimeoutError,
    UnknownTranslationProviderError,
    UnsupportedLanguageError,
)
from snaplex.providers.base import TranslationRequest
from snaplex.providers.config import (
    ProviderRuntimeConfig,
    default_provider_runtime_configs,
    provider_credential_reference,
)
from snaplex.providers.http import HttpTransport
from snaplex.providers.registry import create_default_provider_registry
from snaplex.credentials import (
    CredentialReference,
    CredentialService,
    CredentialSource,
    CredentialStatusCode,
    create_default_credential_service,
)
from snaplex.storage.config import AppConfig


class ProviderSetupStatus(str, Enum):
    FAKE_SMOKE = "fake_smoke"
    MISSING_CREDENTIAL = "missing_credential"
    READY_FROM_ENVIRONMENT = "ready_from_environment"
    READY_FROM_KEYRING = "ready_from_keyring"
    CREDENTIAL_UNAVAILABLE = "credential_unavailable"
    ENDPOINT_UNAVAILABLE = "endpoint_unavailable"
    TEST_PASSED = "test_passed"
    TEST_FAILED = "test_failed"
    OAUTH_FUTURE = "oauth_future"
    UNSUPPORTED_PROVIDER = "unsupported_provider"


@dataclass(frozen=True)
class ProviderSetupState:
    provider_name: str
    display_name: str
    status: ProviderSetupStatus
    status_text: str
    detail_text: str
    base_url: str = ""
    api_key_env_var: str = ""
    api_key_present: bool = False
    credential_source: str = ""
    credential_identifier: str = ""
    credential_status: CredentialStatusCode = CredentialStatusCode.MISSING
    credential_status_text: str = ""
    credential_detail_text: str = ""
    can_save_credential: bool = False
    can_delete_credential: bool = False
    can_test_connection: bool = False
    is_fake: bool = False
    is_real_provider: bool = False
    connect_account_label: str = "Connect account"
    connect_account_enabled: bool = False
    connect_account_detail: str = (
        "Account sign-in requires a later SnapLex Cloud or provider-supported flow."
    )


@dataclass(frozen=True)
class ProviderConnectionTestResult:
    provider_name: str
    display_name: str
    status: ProviderSetupStatus
    status_text: str
    detail_text: str
    translated_text: str = ""


PROVIDER_DISPLAY_NAMES = {
    "fake": "Fake smoke mode",
    "libretranslate": "LibreTranslate",
    "openai": "OpenAI",
    "deepl": "DeepL",
}

REQUIRED_CREDENTIAL_PROVIDERS = {"openai", "deepl"}


def describe_provider_setup(
    provider_name: str,
    provider_config: ProviderRuntimeConfig | None = None,
    *,
    environ: Mapping[str, str] | None = None,
    credential_service: CredentialService | None = None,
) -> ProviderSetupState:
    """Describe user-facing setup readiness without exposing secret values."""

    normalized_provider_name = provider_name.strip().lower()
    provider_configs = default_provider_runtime_configs()
    config = provider_config or provider_configs.get(
        normalized_provider_name,
        ProviderRuntimeConfig(),
    )
    env = os.environ if environ is None else environ

    if normalized_provider_name == "fake":
        return ProviderSetupState(
            provider_name="fake",
            display_name=PROVIDER_DISPLAY_NAMES["fake"],
            status=ProviderSetupStatus.FAKE_SMOKE,
            status_text="Fake smoke mode",
            detail_text=(
                "Deterministic placeholder translation for tests and package smoke. "
                "This is not real translation."
            ),
            can_test_connection=False,
            is_fake=True,
        )

    display_name = PROVIDER_DISPLAY_NAMES.get(normalized_provider_name, provider_name.strip())
    if normalized_provider_name not in PROVIDER_DISPLAY_NAMES:
        return ProviderSetupState(
            provider_name=normalized_provider_name or provider_name,
            display_name=display_name or "Unknown provider",
            status=ProviderSetupStatus.UNSUPPORTED_PROVIDER,
            status_text="Provider is not supported",
            detail_text="Choose fake, LibreTranslate, OpenAI, or DeepL.",
        )

    api_key_env_var = config.api_key_env_var.strip()
    base_url = config.base_url.strip()
    credential_reference = provider_credential_reference(normalized_provider_name, config)
    service = credential_service or create_default_credential_service(
        env,
        include_keyring=credential_reference.source == CredentialSource.KEYRING,
    )
    credential_status = service.status(credential_reference)
    credential_required = _credential_required(normalized_provider_name, credential_reference)
    credential_ready = credential_status.code == CredentialStatusCode.READY

    if credential_required and not credential_ready:
        setup_status = _setup_status_from_credential_status(credential_status.code)
        return ProviderSetupState(
            provider_name=normalized_provider_name,
            display_name=display_name,
            status=setup_status,
            status_text=credential_status.status_text,
            detail_text=credential_status.detail_text
            or _missing_credential_detail(api_key_env_var, display_name),
            base_url=base_url,
            api_key_env_var=api_key_env_var,
            api_key_present=False,
            credential_source=credential_reference.source.value,
            credential_identifier=credential_reference.identifier,
            credential_status=credential_status.code,
            credential_status_text=credential_status.status_text,
            credential_detail_text=credential_status.detail_text,
            can_save_credential=credential_status.can_save,
            can_delete_credential=credential_status.can_delete,
            can_test_connection=False,
            is_real_provider=True,
        )

    setup_status = _ready_setup_status(credential_reference.source)
    return ProviderSetupState(
        provider_name=normalized_provider_name,
        display_name=display_name,
        status=setup_status,
        status_text="Ready to test",
        detail_text=_ready_detail(
            normalized_provider_name,
            api_key_env_var,
            credential_ready,
            credential_reference.source,
        ),
        base_url=base_url,
        api_key_env_var=api_key_env_var,
        api_key_present=credential_ready,
        credential_source=credential_reference.source.value,
        credential_identifier=credential_reference.identifier,
        credential_status=credential_status.code,
        credential_status_text=credential_status.status_text,
        credential_detail_text=credential_status.detail_text,
        can_save_credential=credential_status.can_save,
        can_delete_credential=credential_status.can_delete,
        can_test_connection=True,
        is_real_provider=True,
    )


def describe_provider_setups(
    provider_configs: Mapping[str, ProviderRuntimeConfig],
    *,
    environ: Mapping[str, str] | None = None,
    credential_service: CredentialService | None = None,
) -> tuple[ProviderSetupState, ...]:
    """Describe all supported provider setup states in stable display order."""

    default_configs = default_provider_runtime_configs()
    merged_configs = {**default_configs, **provider_configs}
    return tuple(
        describe_provider_setup(
            provider_name,
            merged_configs[provider_name],
            environ=environ,
            credential_service=credential_service,
        )
        for provider_name in ("fake", "libretranslate", "openai", "deepl")
    )


def test_provider_connection(
    provider_name: str,
    config: AppConfig,
    *,
    http_transport: HttpTransport | None = None,
    environ: Mapping[str, str] | None = None,
    credential_service: CredentialService | None = None,
    probe_text: str = "hello",
    source_lang: str = "en",
    target_lang: str = "es",
) -> ProviderConnectionTestResult:
    """Run a one-shot provider readiness check through provider boundaries."""

    normalized_provider_name = provider_name.strip().lower()
    setup_state = describe_provider_setup(
        normalized_provider_name,
        config.provider_configs.get(normalized_provider_name),
        environ=environ,
        credential_service=credential_service,
    )
    if setup_state.status in {
        ProviderSetupStatus.FAKE_SMOKE,
        ProviderSetupStatus.MISSING_CREDENTIAL,
        ProviderSetupStatus.CREDENTIAL_UNAVAILABLE,
        ProviderSetupStatus.UNSUPPORTED_PROVIDER,
    }:
        return ProviderConnectionTestResult(
            provider_name=setup_state.provider_name,
            display_name=setup_state.display_name,
            status=setup_state.status,
            status_text=setup_state.status_text,
            detail_text=setup_state.detail_text,
        )

    try:
        registry = create_default_provider_registry(
            config,
            http_transport=http_transport,
            environ=environ,
        )
        response = registry.get(normalized_provider_name).translate(
            TranslationRequest(probe_text, source_lang=source_lang, target_lang=target_lang)
        )
    except UnknownTranslationProviderError:
        return _connection_result(
            setup_state,
            ProviderSetupStatus.UNSUPPORTED_PROVIDER,
            "Provider is not supported",
            "Choose fake, LibreTranslate, OpenAI, or DeepL.",
        )
    except MissingProviderCredentialError as exc:
        return _connection_result(
            setup_state,
            ProviderSetupStatus.MISSING_CREDENTIAL,
            "Credential missing",
            _missing_credential_detail(exc.env_var, setup_state.display_name),
        )
    except TranslationProviderTimeoutError:
        return _connection_result(
            setup_state,
            ProviderSetupStatus.ENDPOINT_UNAVAILABLE,
            "Connection timed out",
            "The provider did not respond before the configured timeout.",
        )
    except UnsupportedLanguageError as exc:
        return _connection_result(
            setup_state,
            ProviderSetupStatus.TEST_FAILED,
            "Language pair not supported",
            f"{setup_state.display_name} rejected {exc.source_lang} -> {exc.target_lang}.",
        )
    except StaleTranslationResultError:
        return _connection_result(
            setup_state,
            ProviderSetupStatus.TEST_FAILED,
            "Unexpected provider response",
            "The provider responded, but SnapLex could not read translated text.",
        )
    except TranslationProviderError:
        return _connection_result(
            setup_state,
            ProviderSetupStatus.TEST_FAILED,
            "Connection failed",
            "Check the provider endpoint, credential environment variable, and account status.",
        )
    except TranslationError:
        return _connection_result(
            setup_state,
            ProviderSetupStatus.TEST_FAILED,
            "Connection failed",
            "The provider test failed before translation completed.",
        )

    return ProviderConnectionTestResult(
        provider_name=setup_state.provider_name,
        display_name=setup_state.display_name,
        status=ProviderSetupStatus.TEST_PASSED,
        status_text="Connection test passed",
        detail_text=f"{setup_state.display_name} returned a test translation.",
        translated_text=response.translated_text,
    )


def _missing_credential_detail(api_key_env_var: str, display_name: str) -> str:
    if not api_key_env_var:
        return f"{display_name} needs an API key environment variable name before testing."
    return f"Set {api_key_env_var} in your shell before testing {display_name}."


def _ready_detail(
    provider_name: str,
    api_key_env_var: str,
    credential_ready: bool,
    credential_source: CredentialSource,
) -> str:
    if provider_name == "libretranslate" and not api_key_env_var:
        return "Endpoint is configured. If your server requires a key, add an env var name."
    if credential_source == CredentialSource.KEYRING and credential_ready:
        return "Local secure credential is available. The key value is not stored in config."
    if credential_ready:
        return f"{api_key_env_var} is set in this process. The key value is not stored."
    return "Provider settings are ready for a connection test."


def _credential_required(
    provider_name: str,
    credential_reference: CredentialReference,
) -> bool:
    if provider_name in REQUIRED_CREDENTIAL_PROVIDERS:
        return True
    if provider_name != "libretranslate":
        return False
    return credential_reference.source != CredentialSource.NONE


def _setup_status_from_credential_status(
    credential_status: CredentialStatusCode,
) -> ProviderSetupStatus:
    if credential_status == CredentialStatusCode.MISSING:
        return ProviderSetupStatus.MISSING_CREDENTIAL
    return ProviderSetupStatus.CREDENTIAL_UNAVAILABLE


def _ready_setup_status(source: CredentialSource) -> ProviderSetupStatus:
    if source == CredentialSource.KEYRING:
        return ProviderSetupStatus.READY_FROM_KEYRING
    return ProviderSetupStatus.READY_FROM_ENVIRONMENT


def _connection_result(
    setup_state: ProviderSetupState,
    status: ProviderSetupStatus,
    status_text: str,
    detail_text: str,
) -> ProviderConnectionTestResult:
    return ProviderConnectionTestResult(
        provider_name=setup_state.provider_name,
        display_name=setup_state.display_name,
        status=status,
        status_text=status_text,
        detail_text=detail_text,
    )
