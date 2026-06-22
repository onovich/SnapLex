"""Translation cache contracts and in-memory implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from snaplex.providers.base import TranslationRequest, TranslationResponse


@dataclass(frozen=True)
class TranslationCacheKey:
    text: str
    source_lang: str
    target_lang: str
    provider_name: str

    @classmethod
    def from_request(
        cls,
        request: TranslationRequest,
        *,
        provider_name: str,
    ) -> "TranslationCacheKey":
        return cls(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            provider_name=provider_name,
        )


class TranslationCache(Protocol):
    def get(self, key: TranslationCacheKey) -> TranslationResponse | None:
        """Return a cached translation response when present."""
        ...

    def set(self, key: TranslationCacheKey, response: TranslationResponse) -> None:
        """Store a translation response."""
        ...


class InMemoryTranslationCache:
    def __init__(self) -> None:
        self._items: dict[TranslationCacheKey, TranslationResponse] = {}

    def get(self, key: TranslationCacheKey) -> TranslationResponse | None:
        return self._items.get(key)

    def set(self, key: TranslationCacheKey, response: TranslationResponse) -> None:
        self._items[key] = response

    def __len__(self) -> int:
        return len(self._items)
