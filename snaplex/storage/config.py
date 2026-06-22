"""Configuration storage boundary."""

from __future__ import annotations

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
