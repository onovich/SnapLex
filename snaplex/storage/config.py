"""Configuration storage boundary."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from typing import Protocol

from snaplex.providers.config import (
    ProviderRuntimeConfig,
    copy_provider_runtime_configs,
    default_provider_runtime_configs,
)


@dataclass(frozen=True)
class AppConfig:
    source_lang: str = "auto"
    target_lang: str = "en"
    provider_name: str = "fake"
    provider_order: tuple[str, ...] = ("fake",)
    provider_configs: dict[str, ProviderRuntimeConfig] = field(
        default_factory=default_provider_runtime_configs,
    )
    ui_preferences: dict[str, str] = field(default_factory=dict)


class ConfigStore(Protocol):
    def load(self) -> AppConfig:
        """Load application configuration."""
        ...

    def save(self, config: AppConfig) -> None:
        """Persist application configuration."""
        ...


class InMemoryConfigStore:
    def __init__(self, config: AppConfig | None = None) -> None:
        self._config = config or AppConfig()

    def load(self) -> AppConfig:
        return replace(
            self._config,
            provider_order=tuple(self._config.provider_order),
            provider_configs=copy_provider_runtime_configs(self._config.provider_configs),
            ui_preferences=dict(self._config.ui_preferences),
        )

    def save(self, config: AppConfig) -> None:
        self._config = replace(
            config,
            provider_order=tuple(config.provider_order),
            provider_configs=copy_provider_runtime_configs(config.provider_configs),
            ui_preferences=dict(config.ui_preferences),
        )


def load_app_config_from_environment(
    environ: Mapping[str, str] | None = None,
) -> AppConfig:
    """Build local runtime config from environment variables without reading secrets."""

    env = os.environ if environ is None else environ
    provider_name = _env_text(env, "SNAPLEX_PROVIDER", "fake")
    provider_order = _env_csv(env, "SNAPLEX_PROVIDER_ORDER") or (provider_name,)
    provider_configs = _provider_configs_from_environment(env)
    return AppConfig(
        source_lang=_env_text(env, "SNAPLEX_SOURCE_LANG", "auto"),
        target_lang=_env_text(env, "SNAPLEX_TARGET_LANG", "en"),
        provider_name=provider_name,
        provider_order=provider_order,
        provider_configs=provider_configs,
    )


def _provider_configs_from_environment(
    env: Mapping[str, str],
) -> dict[str, ProviderRuntimeConfig]:
    provider_configs = default_provider_runtime_configs()
    for provider_name in ("libretranslate", "openai", "deepl"):
        prefix = f"SNAPLEX_{provider_name.upper()}"
        default_config = provider_configs[provider_name]
        options = dict(default_config.options)
        if provider_name == "openai":
            model = _env_text(env, "SNAPLEX_OPENAI_MODEL", options.get("model", ""))
            if model:
                options["model"] = model
        if provider_name == "deepl":
            model_type = _env_text(env, "SNAPLEX_DEEPL_MODEL_TYPE", "")
            if model_type:
                options["model_type"] = model_type

        provider_configs[provider_name] = ProviderRuntimeConfig(
            base_url=_env_text(env, f"{prefix}_BASE_URL", default_config.base_url),
            api_key_env_var=_env_text(
                env,
                f"{prefix}_API_KEY_ENV",
                default_config.api_key_env_var,
            ),
            timeout_seconds=_env_float(
                env,
                f"{prefix}_TIMEOUT_SECONDS",
                default_config.timeout_seconds,
            ),
            retry_count=_env_int(env, f"{prefix}_RETRY_COUNT", default_config.retry_count),
            options=options,
        )
    return provider_configs


def _env_text(env: Mapping[str, str], key: str, default: str) -> str:
    value = env.get(key, "").strip()
    return value or default


def _env_csv(env: Mapping[str, str], key: str) -> tuple[str, ...]:
    value = env.get(key, "")
    return tuple(item.strip() for item in value.split(",") if item.strip())


def _env_float(env: Mapping[str, str], key: str, default: float) -> float:
    raw_value = env.get(key, "").strip()
    if not raw_value:
        return default
    try:
        value = float(raw_value)
    except ValueError:
        return default
    return value if value > 0 else default


def _env_int(env: Mapping[str, str], key: str, default: int) -> int:
    raw_value = env.get(key, "").strip()
    if not raw_value:
        return default
    try:
        value = int(raw_value)
    except ValueError:
        return default
    return value if value >= 0 else default
