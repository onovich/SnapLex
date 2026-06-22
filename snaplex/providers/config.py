"""Runtime configuration for translation providers."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field, replace

from snaplex.errors import MissingProviderCredentialError


@dataclass(frozen=True)
class ProviderRuntimeConfig:
    """Provider runtime settings that intentionally store env var names, not secrets."""

    base_url: str = ""
    api_key_env_var: str = ""
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
) -> str:
    env_var = config.api_key_env_var.strip()
    if not env_var:
        raise MissingProviderCredentialError(
            "Provider credential env var is not configured.",
            env_var="",
            provider_name=provider_name,
        )

    env = os.environ if environ is None else environ
    api_key = env.get(env_var, "").strip()
    if not api_key:
        raise MissingProviderCredentialError(env_var=env_var, provider_name=provider_name)
    return api_key
