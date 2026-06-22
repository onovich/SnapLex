"""Recent translation history service."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timezone
from uuid import uuid4

from snaplex.storage import ConfigStore
from snaplex.storage.history import HistoryStore, TranslationHistoryEntry


class HistoryService:
    def __init__(
        self,
        *,
        config_store: ConfigStore,
        history_store: HistoryStore,
        id_factory: Callable[[], str] | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._config_store = config_store
        self._history_store = history_store
        self._id_factory = id_factory or (lambda: uuid4().hex)
        self._clock = clock or (lambda: datetime.now(timezone.utc))

    def add_translation(
        self,
        *,
        source_text: str,
        translated_text: str,
        provider_name: str,
        source_lang: str,
        target_lang: str,
        flow: str,
    ) -> TranslationHistoryEntry | None:
        config = self._config_store.load()
        if not config.history_enabled or config.history_max_entries <= 0:
            return None
        if not source_text.strip() or not translated_text.strip():
            return None

        entry = TranslationHistoryEntry(
            id=self._id_factory(),
            source_text=source_text,
            translated_text=translated_text,
            provider_name=provider_name,
            source_lang=source_lang,
            target_lang=target_lang,
            flow=flow,
            created_at=self._clock().astimezone(timezone.utc).isoformat(),
        )
        entries = (entry, *self._history_store.list_entries())
        retained_entries = entries[: config.history_max_entries]
        self._history_store.replace_entries(retained_entries)
        return entry

    def list_recent(self) -> tuple[TranslationHistoryEntry, ...]:
        return self._history_store.list_entries()

    def get(self, entry_id: str) -> TranslationHistoryEntry | None:
        for entry in self._history_store.list_entries():
            if entry.id == entry_id:
                return entry
        return None

    def delete(self, entry_id: str) -> bool:
        entries = self._history_store.list_entries()
        retained_entries = tuple(entry for entry in entries if entry.id != entry_id)
        if len(retained_entries) == len(entries):
            return False
        self._history_store.replace_entries(retained_entries)
        return True

    def clear(self) -> None:
        self._history_store.replace_entries(())
