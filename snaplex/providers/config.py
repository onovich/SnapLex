"""Runtime configuration for translation providers."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field, replace

from snaplex.errors import MissingProviderCredentialError
from snaplex.credentials import (
    CredentialReference,
    CredentialService,
    CredentialSource,
    CredentialStoreError,
    create_environment_credential_service,
    environment_credential_reference,
    keyring_credential_reference,
)


@dataclass(frozen=True)
class ProviderRuntimeConfig:
    """Provider runtime settings that intentionally store env var names, not secrets."""

    base_url: str = ""
    api_key_env_var: str = ""
    credential_source: str = ""
    credential_identifier: str = ""
    timeout_seconds: float = 10.0
    retry_count: int = 0
    options: dict[str, str] = field(default_factory=dict)

    def with_copied_options(self) -> ProviderRuntimeConfig:
        return replace(self, options=dict(self.options))

    def base_url_without_trailing_slash(self) -> str:
        return self.base_url.rstrip("/")


def default_provider_runtime_configs() -> dict[str, ProviderRuntimeConfig]:
    """Return default provider config without selecting real providers by default."""

    return {
        "fake": ProviderRuntimeConfig(),
        "libretranslate": ProviderRuntimeConfig(base_url="http://localhost:5000"),
        "openai": ProviderRuntimeConfig(
            base_url="https://api.openai.com/v1",
            api_key_env_var="SNAPLEX_OPENAI_API_KEY",
            timeout_seconds=20.0,
            options={"model": "gpt-5.5"},
        ),
        "deepl": ProviderRuntimeConfig(
            base_url="https://api-free.deepl.com/v2",
            api_key_env_var="SNAPLEX_DEEPL_API_KEY",
            timeout_seconds=20.0,
        ),
    }


def copy_provider_runtime_configs(
    provider_configs: Mapping[str, ProviderRuntimeConfig],
) -> dict[str, ProviderRuntimeConfig]:
    return {name: config.with_copied_options() for name, config in provider_configs.items()}


def resolve_api_key(
    provider_name: str,
    config: ProviderRuntimeConfig,
    *,
    environ: Mapping[str, str] | None = None,
    credential_service: CredentialService | None = None,
) -> str:
    env_var = config.api_key_env_var.strip()
    reference = provider_credential_reference(provider_name, config)
    service = credential_service or create_environment_credential_service(
        os.environ if environ is None else environ,
    )
    try:
        return service.resolve(reference)
    except CredentialStoreError as exc:
        message = (
            "Provider credential env var is not configured."
            if not env_var
            else "Provider credential env var is missing."
        )
        raise MissingProviderCredentialError(
            message,
            env_var=env_var,
            provider_name=provider_name,
        ) from exc


def provider_credential_reference(
    provider_name: str,
    config: ProviderRuntimeConfig,
) -> CredentialReference:
    """Return the configured non-secret credential reference for a provider."""

    source_text = config.credential_source.strip().lower()
    identifier = config.credential_identifier.strip()
    if not source_text:
        return environment_credential_reference(provider_name, config.api_key_env_var)

    try:
        source = CredentialSource(source_text)
    except ValueError:
        return CredentialReference(
            provider_name=provider_name,
            source=CredentialSource.UNSUPPORTED,
            identifier=identifier,
        )

    if source == CredentialSource.ENVIRONMENT:
        return environment_credential_reference(
            provider_name,
            identifier or config.api_key_env_var,
        )
    if source == CredentialSource.KEYRING:
        return keyring_credential_reference(provider_name, identifier)
    if source == CredentialSource.NONE:
        return CredentialReference(provider_name=provider_name)
    return CredentialReference(
        provider_name=provider_name,
        source=source,
        identifier=identifier,
    )
