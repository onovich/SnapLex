"""Translation application service."""

from __future__ import annotations

from snaplex.providers.base import TranslationProvider, TranslationRequest, TranslationResponse
from snaplex.services.text import normalize_text


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
