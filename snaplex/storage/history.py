"""Translation history storage boundary."""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Protocol

from snaplex.storage.paths import default_app_data_dir


HISTORY_FILE_VERSION = 1
HISTORY_FILE_NAME = "history.json"


@dataclass(frozen=True)
class TranslationHistoryEntry:
    id: str
    source_text: str
    translated_text: str
    provider_name: str
    source_lang: str
    target_lang: str
    flow: str
    created_at: str


class HistoryStore(Protocol):
    def list_entries(self) -> tuple[TranslationHistoryEntry, ...]:
        """Return persisted translation history entries."""
        ...

    def replace_entries(self, entries: tuple[TranslationHistoryEntry, ...]) -> None:
        """Replace persisted translation history entries."""
        ...


class InMemoryHistoryStore:
    def __init__(self, entries: tuple[TranslationHistoryEntry, ...] = ()) -> None:
        self._entries = tuple(entries)

    def list_entries(self) -> tuple[TranslationHistoryEntry, ...]:
        return tuple(_copy_entry(entry) for entry in self._entries)

    def replace_entries(self, entries: tuple[TranslationHistoryEntry, ...]) -> None:
        self._entries = tuple(_copy_entry(entry) for entry in entries)


class JsonFileHistoryStore:
    def __init__(self, history_path: Path | None = None) -> None:
        self._history_path = history_path or default_app_data_dir() / HISTORY_FILE_NAME

    @property
    def history_path(self) -> Path:
        return self._history_path

    def list_entries(self) -> tuple[TranslationHistoryEntry, ...]:
        if not self._history_path.exists():
            return ()

        try:
            payload = json.loads(self._history_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            return ()

        if not isinstance(payload, dict):
            return ()
        return entries_from_dict(payload)

    def replace_entries(self, entries: tuple[TranslationHistoryEntry, ...]) -> None:
        self._history_path.parent.mkdir(parents=True, exist_ok=True)
        payload = entries_to_dict(entries)
        temp_path = self._history_path.with_name(f"{self._history_path.name}.tmp")
        temp_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        temp_path.replace(self._history_path)


def entries_to_dict(entries: tuple[TranslationHistoryEntry, ...]) -> dict[str, object]:
    return {
        "version": HISTORY_FILE_VERSION,
        "entries": [entry_to_dict(entry) for entry in entries],
    }


def entries_from_dict(payload: dict[object, object]) -> tuple[TranslationHistoryEntry, ...]:
    raw_entries = payload.get("entries")
    if not isinstance(raw_entries, list):
        return ()

    entries: list[TranslationHistoryEntry] = []
    for raw_entry in raw_entries:
        if not isinstance(raw_entry, dict):
            continue
        entry = entry_from_dict(raw_entry)
        if entry is not None:
            entries.append(entry)
    return tuple(entries)


def entry_to_dict(entry: TranslationHistoryEntry) -> dict[str, str]:
    return {
        "id": entry.id,
        "source_text": entry.source_text,
        "translated_text": entry.translated_text,
        "provider_name": entry.provider_name,
        "source_lang": entry.source_lang,
        "target_lang": entry.target_lang,
        "flow": entry.flow,
        "created_at": entry.created_at,
    }


def entry_from_dict(payload: dict[object, object]) -> TranslationHistoryEntry | None:
    entry_id = _required_string(payload.get("id"))
    source_text = _required_string(payload.get("source_text"))
    translated_text = _required_string(payload.get("translated_text"))
    provider_name = _required_string(payload.get("provider_name"))
    source_lang = _required_string(payload.get("source_lang"))
    target_lang = _required_string(payload.get("target_lang"))
    flow = _required_string(payload.get("flow"))
    created_at = _required_string(payload.get("created_at"))
    if entry_id is None:
        return None
    if source_text is None:
        return None
    if translated_text is None:
        return None
    if provider_name is None:
        return None
    if source_lang is None:
        return None
    if target_lang is None:
        return None
    if flow is None:
        return None
    if created_at is None:
        return None
    return TranslationHistoryEntry(
        id=entry_id,
        source_text=source_text,
        translated_text=translated_text,
        provider_name=provider_name,
        source_lang=source_lang,
        target_lang=target_lang,
        flow=flow,
        created_at=created_at,
    )


def _copy_entry(entry: TranslationHistoryEntry) -> TranslationHistoryEntry:
    return replace(entry)


def _required_string(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value or None
