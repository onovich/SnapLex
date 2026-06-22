"""Translation application service."""

from __future__ import annotations

from snaplex.errors import FallbackExhaustedError, TranslationError
from snaplex.providers.base import TranslationProvider, TranslationRequest, TranslationResponse
from snaplex.providers.registry import ProviderRegistry, create_default_provider_registry
from snaplex.services.text import normalize_text
from snaplex.storage import AppConfig, ConfigStore, InMemoryConfigStore


class TranslationService:
    def __init__(self, provider: TranslationProvider) -> None:
        self._provider = provider

    def translate_text(
        self,
        text: str,
        *,
        source_lang: str = "auto",
        target_lang: str = "en",
    ) -> TranslationResponse:
        normalized_text = normalize_text(text)
        if not normalized_text:
            return TranslationResponse(
                translated_text="",
                provider_name=self._provider.name,
                source_lang=source_lang,
                target_lang=target_lang,
            )

        request = TranslationRequest(
            text=normalized_text,
            source_lang=source_lang,
            target_lang=target_lang,
        )
        return self._provider.translate(request)


class TranslationPipeline:
    def __init__(self, config_store: ConfigStore, provider_registry: ProviderRegistry) -> None:
        self._config_store = config_store
        self._provider_registry = provider_registry

    def translate_text(
        self,
        text: str,
        *,
        source_lang: str | None = None,
        target_lang: str | None = None,
    ) -> TranslationResponse:
        config = self._config_store.load()
        request = self._build_request(
            text,
            config=config,
            source_lang=source_lang,
            target_lang=target_lang,
        )
        if not request.text:
            return TranslationResponse(
                translated_text="",
                provider_name=config.provider_name,
                source_lang=request.source_lang,
                target_lang=request.target_lang,
            )

        provider = self._provider_registry.get(config.provider_name)
        try:
            return provider.translate(request)
        except TranslationError as exc:
            raise FallbackExhaustedError(provider_errors=(exc,)) from exc

    def _build_request(
        self,
        text: str,
        *,
        config: AppConfig,
        source_lang: str | None,
        target_lang: str | None,
    ) -> TranslationRequest:
        return TranslationRequest(
            text=normalize_text(text),
            source_lang=source_lang or config.source_lang,
            target_lang=target_lang or config.target_lang,
        )


def create_default_translation_pipeline(
    config_store: ConfigStore | None = None,
) -> TranslationPipeline:
    return TranslationPipeline(
        config_store=config_store or InMemoryConfigStore(),
        provider_registry=create_default_provider_registry(),
    )
