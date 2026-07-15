"""Settings service boundary for persisted app configuration."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace

from snaplex.providers.config import ProviderRuntimeConfig, copy_provider_runtime_configs
from snaplex.providers.http import HttpTransport
from snaplex.services.provider_setup import (
    ProviderConnectionTestResult,
    ProviderSetupState,
    describe_provider_setups,
    test_provider_connection,
)
from snaplex.storage import AppConfig, ConfigStore


class SettingsService:
    def __init__(self, config_store: ConfigStore) -> None:
        self._config_store = config_store

    def load(self) -> AppConfig:
        return self._config_store.load()

    def load_provider_setup_states(
        self,
        *,
        environ: Mapping[str, str] | None = None,
    ) -> tuple[ProviderSetupState, ...]:
        config = self._config_store.load()
        return describe_provider_setups(config.provider_configs, environ=environ)

    def test_provider_connection(
        self,
        provider_name: str,
        *,
        http_transport: HttpTransport | None = None,
        environ: Mapping[str, str] | None = None,
        probe_text: str = "hello",
        source_lang: str = "en",
        target_lang: str = "es",
    ) -> ProviderConnectionTestResult:
        config = self._config_store.load()
        return test_provider_connection(
            provider_name,
            config,
            http_transport=http_transport,
            environ=environ,
            probe_text=probe_text,
            source_lang=source_lang,
            target_lang=target_lang,
        )

    def save(self, config: AppConfig) -> AppConfig:
        self._config_store.save(config)
        return self._config_store.load()

    def update_language_defaults(
        self,
        *,
        source_lang: str | None = None,
        target_lang: str | None = None,
    ) -> AppConfig:
        config = self._config_store.load()
        updated_config = replace(
            config,
            source_lang=_clean_text(source_lang, config.source_lang),
            target_lang=_clean_text(target_lang, config.target_lang),
        )
        return self.save(updated_config)

    def update_provider_selection(
        self,
        *,
        provider_name: str,
        provider_order: tuple[str, ...] | list[str] | str | None = None,
    ) -> AppConfig:
        config = self._config_store.load()
        clean_provider_name = _clean_text(provider_name, config.provider_name)
        clean_provider_order = _clean_provider_order(provider_order, (clean_provider_name,))
        updated_config = replace(
            config,
            provider_name=clean_provider_name,
            provider_order=clean_provider_order,
        )
        return self.save(updated_config)

    def update_provider_runtime_config(
        self,
        provider_name: str,
        *,
        base_url: str | None = None,
        api_key_env_var: str | None = None,
        timeout_seconds: float | int | str | None = None,
        retry_count: int | str | None = None,
        options: dict[str, str] | None = None,
    ) -> AppConfig:
        config = self._config_store.load()
        provider_configs = copy_provider_runtime_configs(config.provider_configs)
        existing_provider_config = provider_configs.get(provider_name, ProviderRuntimeConfig())
        provider_configs[provider_name] = replace(
            existing_provider_config,
            base_url=_clean_text(base_url, existing_provider_config.base_url),
            api_key_env_var=_clean_text(
                api_key_env_var,
                existing_provider_config.api_key_env_var,
            ),
            timeout_seconds=_positive_float(
                timeout_seconds,
                existing_provider_config.timeout_seconds,
            ),
            retry_count=_non_negative_int(retry_count, existing_provider_config.retry_count),
            options=_merge_options(existing_provider_config.options, options),
        )
        return self.save(replace(config, provider_configs=provider_configs))

    def update_history_preferences(
        self,
        *,
        enabled: bool | None = None,
        max_entries: int | str | None = None,
    ) -> AppConfig:
        config = self._config_store.load()
        updated_config = replace(
            config,
            history_enabled=config.history_enabled if enabled is None else enabled,
            history_max_entries=_non_negative_int(max_entries, config.history_max_entries),
        )
        return self.save(updated_config)

    def update_ui_preferences(self, preferences: dict[str, str]) -> AppConfig:
        config = self._config_store.load()
        updated_preferences = dict(config.ui_preferences)
        updated_preferences.update(
            {key: value for key, value in preferences.items() if key and isinstance(value, str)}
        )
        return self.save(replace(config, ui_preferences=updated_preferences))


def _clean_text(value: str | None, default: str) -> str:
    if value is None:
        return default
    cleaned = value.strip()
    return cleaned or default


def _clean_provider_order(
    value: tuple[str, ...] | list[str] | str | None,
    default: tuple[str, ...],
) -> tuple[str, ...]:
    if value is None:
        return default
    if isinstance(value, str):
        cleaned = tuple(item.strip() for item in value.split(",") if item.strip())
        return cleaned or default
    cleaned = tuple(item.strip() for item in value if isinstance(item, str) and item.strip())
    return cleaned or default


def _positive_float(value: float | int | str | None, default: float) -> float:
    if value is None:
        return default
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default


def _non_negative_int(value: int | str | None, default: int) -> int:
    if value is None or isinstance(value, bool):
        return default
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed >= 0 else default


def _merge_options(
    existing_options: dict[str, str],
    updates: dict[str, str] | None,
) -> dict[str, str]:
    merged_options = dict(existing_options)
    if updates is None:
        return merged_options
    for key, value in updates.items():
        if not key:
            continue
        if value == "":
            merged_options.pop(key, None)
            continue
        merged_options[key] = value
    return merged_options
