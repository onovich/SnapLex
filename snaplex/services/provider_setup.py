"""Provider setup state for trial UX without reading or storing secrets."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum

from snaplex.providers.config import ProviderRuntimeConfig, default_provider_runtime_configs


class ProviderSetupStatus(str, Enum):
    FAKE_SMOKE = "fake_smoke"
    MISSING_CREDENTIAL = "missing_credential"
    READY_FROM_ENVIRONMENT = "ready_from_environment"
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
    can_test_connection: bool = False
    is_fake: bool = False
    is_real_provider: bool = False
    connect_account_label: str = "Connect account"
    connect_account_enabled: bool = False
    connect_account_detail: str = (
        "Account sign-in requires a later SnapLex Cloud or provider-supported flow."
    )


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
    api_key_present = bool(api_key_env_var and env.get(api_key_env_var, "").strip())
    base_url = config.base_url.strip()
    is_missing_required_credential = (
        normalized_provider_name in REQUIRED_CREDENTIAL_PROVIDERS and not api_key_present
    ) or (
        normalized_provider_name == "libretranslate"
        and bool(api_key_env_var)
        and not api_key_present
    )

    if is_missing_required_credential:
        return ProviderSetupState(
            provider_name=normalized_provider_name,
            display_name=display_name,
            status=ProviderSetupStatus.MISSING_CREDENTIAL,
            status_text="Credential missing",
            detail_text=_missing_credential_detail(api_key_env_var, display_name),
            base_url=base_url,
            api_key_env_var=api_key_env_var,
            api_key_present=False,
            can_test_connection=False,
            is_real_provider=True,
        )

    return ProviderSetupState(
        provider_name=normalized_provider_name,
        display_name=display_name,
        status=ProviderSetupStatus.READY_FROM_ENVIRONMENT,
        status_text="Ready to test",
        detail_text=_ready_detail(normalized_provider_name, api_key_env_var, api_key_present),
        base_url=base_url,
        api_key_env_var=api_key_env_var,
        api_key_present=api_key_present,
        can_test_connection=True,
        is_real_provider=True,
    )


def describe_provider_setups(
    provider_configs: Mapping[str, ProviderRuntimeConfig],
    *,
    environ: Mapping[str, str] | None = None,
) -> tuple[ProviderSetupState, ...]:
    """Describe all supported provider setup states in stable display order."""

    default_configs = default_provider_runtime_configs()
    merged_configs = {**default_configs, **provider_configs}
    return tuple(
        describe_provider_setup(provider_name, merged_configs[provider_name], environ=environ)
        for provider_name in ("fake", "libretranslate", "openai", "deepl")
    )


def _missing_credential_detail(api_key_env_var: str, display_name: str) -> str:
    if not api_key_env_var:
        return f"{display_name} needs an API key environment variable name before testing."
    return f"Set {api_key_env_var} in your shell before testing {display_name}."


def _ready_detail(provider_name: str, api_key_env_var: str, api_key_present: bool) -> str:
    if provider_name == "libretranslate" and not api_key_env_var:
        return "Endpoint is configured. If your server requires a key, add an env var name."
    if api_key_present:
        return f"{api_key_env_var} is set in this process. The key value is not stored."
    return "Provider settings are ready for a connection test."
