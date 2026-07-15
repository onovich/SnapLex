"""Settings presentation boundary."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from snaplex.providers.config import ProviderRuntimeConfig
from snaplex.services import SettingsService
from snaplex.services.provider_setup import ProviderSetupState


PROVIDER_CHOICES = ("fake", "libretranslate", "openai", "deepl")


@dataclass(frozen=True)
class SettingsFormState:
    provider_choices: tuple[str, ...] = PROVIDER_CHOICES
    source_lang: str = "auto"
    target_lang: str = "en"
    provider_name: str = "fake"
    provider_order: str = "fake"
    libretranslate_base_url: str = "http://localhost:5000"
    libretranslate_api_key_env_var: str = ""
    libretranslate_timeout_seconds: float = 10.0
    libretranslate_retry_count: int = 0
    openai_base_url: str = "https://api.openai.com/v1"
    openai_api_key_env_var: str = "SNAPLEX_OPENAI_API_KEY"
    openai_timeout_seconds: float = 20.0
    openai_retry_count: int = 0
    openai_model: str = "gpt-5.5"
    deepl_base_url: str = "https://api-free.deepl.com/v2"
    deepl_api_key_env_var: str = "SNAPLEX_DEEPL_API_KEY"
    deepl_timeout_seconds: float = 20.0
    deepl_retry_count: int = 0
    deepl_model_type: str = ""
    history_enabled: bool = False
    history_max_entries: int = 50
    provider_setups: tuple[ProviderSetupState, ...] = field(default_factory=tuple)


class SettingsPresenter:
    def __init__(self, settings_service: SettingsService) -> None:
        self._settings_service = settings_service

    def load_state(self, *, environ: Mapping[str, str] | None = None) -> SettingsFormState:
        config = self._settings_service.load()
        libretranslate_config = config.provider_configs.get(
            "libretranslate",
            ProviderRuntimeConfig(base_url="http://localhost:5000"),
        )
        openai_config = config.provider_configs.get(
            "openai",
            ProviderRuntimeConfig(
                base_url="https://api.openai.com/v1",
                api_key_env_var="SNAPLEX_OPENAI_API_KEY",
                timeout_seconds=20.0,
                options={"model": "gpt-5.5"},
            ),
        )
        deepl_config = config.provider_configs.get(
            "deepl",
            ProviderRuntimeConfig(
                base_url="https://api-free.deepl.com/v2",
                api_key_env_var="SNAPLEX_DEEPL_API_KEY",
                timeout_seconds=20.0,
            ),
        )
        return SettingsFormState(
            source_lang=config.source_lang,
            target_lang=config.target_lang,
            provider_name=config.provider_name,
            provider_order=", ".join(config.provider_order),
            libretranslate_base_url=libretranslate_config.base_url,
            libretranslate_api_key_env_var=libretranslate_config.api_key_env_var,
            libretranslate_timeout_seconds=libretranslate_config.timeout_seconds,
            libretranslate_retry_count=libretranslate_config.retry_count,
            openai_base_url=openai_config.base_url,
            openai_api_key_env_var=openai_config.api_key_env_var,
            openai_timeout_seconds=openai_config.timeout_seconds,
            openai_retry_count=openai_config.retry_count,
            openai_model=openai_config.options.get("model", ""),
            deepl_base_url=deepl_config.base_url,
            deepl_api_key_env_var=deepl_config.api_key_env_var,
            deepl_timeout_seconds=deepl_config.timeout_seconds,
            deepl_retry_count=deepl_config.retry_count,
            deepl_model_type=deepl_config.options.get("model_type", ""),
            history_enabled=config.history_enabled,
            history_max_entries=config.history_max_entries,
            provider_setups=self._settings_service.load_provider_setup_states(environ=environ),
        )

    def apply_state(
        self,
        state: SettingsFormState,
        *,
        environ: Mapping[str, str] | None = None,
    ) -> SettingsFormState:
        self._settings_service.update_language_defaults(
            source_lang=state.source_lang,
            target_lang=state.target_lang,
        )
        self._settings_service.update_provider_selection(
            provider_name=state.provider_name,
            provider_order=state.provider_order,
        )
        self._settings_service.update_provider_runtime_config(
            "libretranslate",
            base_url=state.libretranslate_base_url,
            api_key_env_var=state.libretranslate_api_key_env_var,
            timeout_seconds=state.libretranslate_timeout_seconds,
            retry_count=state.libretranslate_retry_count,
        )
        self._settings_service.update_provider_runtime_config(
            "openai",
            base_url=state.openai_base_url,
            api_key_env_var=state.openai_api_key_env_var,
            timeout_seconds=state.openai_timeout_seconds,
            retry_count=state.openai_retry_count,
            options={"model": state.openai_model},
        )
        self._settings_service.update_provider_runtime_config(
            "deepl",
            base_url=state.deepl_base_url,
            api_key_env_var=state.deepl_api_key_env_var,
            timeout_seconds=state.deepl_timeout_seconds,
            retry_count=state.deepl_retry_count,
            options={"model_type": state.deepl_model_type},
        )
        self._settings_service.update_history_preferences(
            enabled=state.history_enabled,
            max_entries=state.history_max_entries,
        )
        return self.load_state(environ=environ)
