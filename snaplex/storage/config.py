"""Configuration storage boundary."""

from __future__ import annotations

import json
import os
from pathlib import Path
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from typing import Protocol

from snaplex.providers.config import (
    ProviderRuntimeConfig,
    copy_provider_runtime_configs,
    default_provider_runtime_configs,
)
from snaplex.storage.paths import default_app_data_dir


CONFIG_FILE_VERSION = 1
CONFIG_FILE_NAME = "config.json"


@dataclass(frozen=True)
class AppConfig:
    source_lang: str = "auto"
    target_lang: str = "en"
    provider_name: str = "fake"
    provider_order: tuple[str, ...] = ("fake",)
    provider_configs: dict[str, ProviderRuntimeConfig] = field(
        default_factory=default_provider_runtime_configs,
    )
    history_enabled: bool = False
    history_max_entries: int = 50
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
            history_max_entries=max(0, self._config.history_max_entries),
            ui_preferences=dict(self._config.ui_preferences),
        )

    def save(self, config: AppConfig) -> None:
        self._config = replace(
            config,
            provider_order=tuple(config.provider_order),
            provider_configs=copy_provider_runtime_configs(config.provider_configs),
            history_max_entries=max(0, config.history_max_entries),
            ui_preferences=dict(config.ui_preferences),
        )


class JsonFileConfigStore:
    """JSON file-backed config storage with default fallback and migration hooks."""

    def __init__(
        self,
        config_path: Path | None = None,
        *,
        default_config: AppConfig | None = None,
    ) -> None:
        self._config_path = config_path or default_app_data_dir() / CONFIG_FILE_NAME
        self._default_config = default_config or AppConfig()

    @property
    def config_path(self) -> Path:
        return self._config_path

    def load(self) -> AppConfig:
        if not self._config_path.exists():
            return _copy_app_config(self._default_config)

        try:
            payload = json.loads(self._config_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            return _copy_app_config(self._default_config)

        if not isinstance(payload, dict):
            return _copy_app_config(self._default_config)
        return app_config_from_dict(payload)

    def save(self, config: AppConfig) -> None:
        self._config_path.parent.mkdir(parents=True, exist_ok=True)
        payload = app_config_to_dict(config)
        temp_path = self._config_path.with_name(f"{self._config_path.name}.tmp")
        temp_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        temp_path.replace(self._config_path)


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


def app_config_to_dict(config: AppConfig) -> dict[str, object]:
    """Serialize config using only app-owned, non-secret fields."""

    return {
        "version": CONFIG_FILE_VERSION,
        "source_lang": config.source_lang,
        "target_lang": config.target_lang,
        "provider_name": config.provider_name,
        "provider_order": list(config.provider_order),
        "provider_configs": {
            provider_name: _provider_runtime_config_to_dict(provider_config)
            for provider_name, provider_config in config.provider_configs.items()
        },
        "history_enabled": config.history_enabled,
        "history_max_entries": max(0, config.history_max_entries),
        "ui_preferences": dict(config.ui_preferences),
    }


def _copy_app_config(config: AppConfig) -> AppConfig:
    return replace(
        config,
        provider_order=tuple(config.provider_order),
        provider_configs=copy_provider_runtime_configs(config.provider_configs),
        history_max_entries=max(0, config.history_max_entries),
        ui_preferences=dict(config.ui_preferences),
    )


def app_config_from_dict(payload: Mapping[str, object]) -> AppConfig:
    migrated_payload = _migrate_config_payload(payload)
    defaults = AppConfig()
    provider_configs = copy_provider_runtime_configs(defaults.provider_configs)
    raw_provider_configs = migrated_payload.get("provider_configs")
    if isinstance(raw_provider_configs, dict):
        provider_configs.update(_provider_runtime_configs_from_dict(raw_provider_configs))

    return AppConfig(
        source_lang=_string_value(migrated_payload.get("source_lang"), defaults.source_lang),
        target_lang=_string_value(migrated_payload.get("target_lang"), defaults.target_lang),
        provider_name=_string_value(migrated_payload.get("provider_name"), defaults.provider_name),
        provider_order=_string_tuple_value(
            migrated_payload.get("provider_order"),
            defaults.provider_order,
        ),
        provider_configs=provider_configs,
        history_enabled=_bool_value(
            migrated_payload.get("history_enabled"),
            defaults.history_enabled,
        ),
        history_max_entries=_non_negative_int_value(
            migrated_payload.get("history_max_entries"),
            defaults.history_max_entries,
        ),
        ui_preferences=_string_dict_value(migrated_payload.get("ui_preferences")),
    )


def _migrate_config_payload(payload: Mapping[str, object]) -> dict[str, object]:
    version = _non_negative_int_value(payload.get("version"), 0)
    migrated_payload = dict(payload)
    if version <= 0:
        migrated_payload.setdefault("version", CONFIG_FILE_VERSION)
    return migrated_payload


def _provider_runtime_config_to_dict(config: ProviderRuntimeConfig) -> dict[str, object]:
    return {
        "base_url": config.base_url,
        "api_key_env_var": config.api_key_env_var,
        "timeout_seconds": config.timeout_seconds,
        "retry_count": config.retry_count,
        "options": dict(config.options),
    }


def _provider_runtime_configs_from_dict(
    payload: Mapping[object, object],
) -> dict[str, ProviderRuntimeConfig]:
    provider_configs: dict[str, ProviderRuntimeConfig] = {}
    for raw_provider_name, raw_provider_config in payload.items():
        if not isinstance(raw_provider_name, str) or not isinstance(raw_provider_config, dict):
            continue
        provider_configs[raw_provider_name] = _provider_runtime_config_from_dict(
            raw_provider_config,
        )
    return provider_configs


def _provider_runtime_config_from_dict(payload: Mapping[object, object]) -> ProviderRuntimeConfig:
    defaults = ProviderRuntimeConfig()
    return ProviderRuntimeConfig(
        base_url=_string_value(payload.get("base_url"), defaults.base_url),
        api_key_env_var=_string_value(
            payload.get("api_key_env_var"),
            defaults.api_key_env_var,
        ),
        timeout_seconds=_positive_float_value(
            payload.get("timeout_seconds"),
            defaults.timeout_seconds,
        ),
        retry_count=_non_negative_int_value(payload.get("retry_count"), defaults.retry_count),
        options=_string_dict_value(payload.get("options")),
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


def _string_value(value: object, default: str) -> str:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped if stripped else default
    return default


def _string_tuple_value(value: object, default: tuple[str, ...]) -> tuple[str, ...]:
    if isinstance(value, str):
        return tuple(item.strip() for item in value.split(",") if item.strip()) or default
    if not isinstance(value, list):
        return default
    values = tuple(item.strip() for item in value if isinstance(item, str) and item.strip())
    return values or default


def _string_dict_value(value: object) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {
        key: raw_value
        for key, raw_value in value.items()
        if isinstance(key, str) and isinstance(raw_value, str)
    }


def _bool_value(value: object, default: bool) -> bool:
    return value if isinstance(value, bool) else default


def _positive_float_value(value: object, default: float) -> float:
    if isinstance(value, int | float):
        parsed_value = float(value)
        return parsed_value if parsed_value > 0 else default
    if isinstance(value, str):
        try:
            parsed_value = float(value)
        except ValueError:
            return default
        return parsed_value if parsed_value > 0 else default
    return default


def _non_negative_int_value(value: object, default: int) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value if value >= 0 else default
    if isinstance(value, str):
        try:
            parsed_value = int(value)
        except ValueError:
            return default
        return parsed_value if parsed_value >= 0 else default
    return default
