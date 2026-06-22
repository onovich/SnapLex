"""Configuration storage boundary."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Protocol


@dataclass(frozen=True)
class AppConfig:
    source_lang: str = "auto"
    target_lang: str = "en"
    provider_name: str = "fake"
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
        return replace(self._config, ui_preferences=dict(self._config.ui_preferences))

    def save(self, config: AppConfig) -> None:
        self._config = replace(config, ui_preferences=dict(config.ui_preferences))
