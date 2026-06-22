"""Provider registry for config-driven translation provider selection."""

from __future__ import annotations

from collections.abc import Iterable

from snaplex.errors import UnknownTranslationProviderError
from snaplex.providers.base import TranslationProvider
from snaplex.providers.fake import FakeTranslationProvider


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


def create_default_provider_registry() -> ProviderRegistry:
    return ProviderRegistry([FakeTranslationProvider()])
