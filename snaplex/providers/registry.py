"""Provider registry for config-driven translation provider selection."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import TYPE_CHECKING

from snaplex.errors import UnknownTranslationProviderError
from snaplex.providers.base import TranslationProvider
from snaplex.providers.config import ProviderRuntimeConfig, default_provider_runtime_configs
from snaplex.providers.deepl import DeepLTranslationProvider
from snaplex.providers.fake import FakeTranslationProvider
from snaplex.providers.http import HttpTransport
from snaplex.providers.libretranslate import LibreTranslateProvider
from snaplex.providers.openai import OpenAITranslationProvider
from snaplex.providers.retry import RetryingTranslationProvider

if TYPE_CHECKING:
    from snaplex.storage.config import AppConfig


class ProviderRegistry:
    def __init__(self, providers: Iterable[TranslationProvider] = ()) -> None:
        self._providers: dict[str, TranslationProvider] = {}
        for provider in providers:
            self.register(provider)

    def register(self, provider: TranslationProvider) -> None:
        if not provider.name:
            raise ValueError("Translation provider name must not be empty.")

        self._providers[provider.name] = provider

    def get(self, provider_name: str) -> TranslationProvider:
        try:
            return self._providers[provider_name]
        except KeyError as exc:
            raise UnknownTranslationProviderError(provider_name=provider_name) from exc

    def resolve_order(self, provider_names: Iterable[str]) -> tuple[TranslationProvider, ...]:
        return tuple(self.get(provider_name) for provider_name in provider_names)

    def names(self) -> tuple[str, ...]:
        return tuple(self._providers.keys())


def create_default_provider_registry(
    config: AppConfig | None = None,
    *,
    http_transport: HttpTransport | None = None,
    environ: Mapping[str, str] | None = None,
) -> ProviderRegistry:
    provider_configs = _merged_provider_configs(config)
    providers: list[TranslationProvider] = [
        FakeTranslationProvider(),
        _with_retry(
            LibreTranslateProvider(
                config=provider_configs["libretranslate"],
                transport=http_transport,
                environ=environ,
            ),
            provider_configs["libretranslate"],
        ),
        _with_retry(
            OpenAITranslationProvider(
                config=provider_configs["openai"],
                transport=http_transport,
                environ=environ,
            ),
            provider_configs["openai"],
        ),
        _with_retry(
            DeepLTranslationProvider(
                config=provider_configs["deepl"],
                transport=http_transport,
                environ=environ,
            ),
            provider_configs["deepl"],
        ),
    ]
    return ProviderRegistry(providers)


def _with_retry(
    provider: TranslationProvider,
    config: ProviderRuntimeConfig,
) -> TranslationProvider:
    if config.retry_count <= 0:
        return provider
    return RetryingTranslationProvider(provider, retry_count=config.retry_count)


def _merged_provider_configs(
    config: AppConfig | None,
) -> dict[str, ProviderRuntimeConfig]:
    provider_configs = default_provider_runtime_configs()
    if config is None:
        return provider_configs

    provider_configs.update(config.provider_configs)
    return {
        name: provider_config.with_copied_options()
        for name, provider_config in provider_configs.items()
    }
