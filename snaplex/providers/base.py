"""Translation provider contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from snaplex.errors import TranslationProviderError as TranslationProviderError


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    source_lang: str = "auto"
    target_lang: str = "en"


@dataclass(frozen=True)
class TranslationResponse:
    translated_text: str
    provider_name: str
    source_lang: str
    target_lang: str


class TranslationProvider(Protocol):
    name: str

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """Translate text through a concrete provider."""
        ...
