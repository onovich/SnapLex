from __future__ import annotations

import json
from datetime import datetime, timezone

from snaplex.services import HistoryService
from snaplex.storage import (
    AppConfig,
    HISTORY_FILE_VERSION,
    InMemoryConfigStore,
    InMemoryHistoryStore,
    JsonFileHistoryStore,
    TranslationHistoryEntry,
    entries_from_dict,
    entries_to_dict,
)


def make_service(
    history_store: InMemoryHistoryStore,
    *,
    config: AppConfig | None = None,
) -> HistoryService:
    ids = iter(("entry-1", "entry-2", "entry-3"))
    return HistoryService(
        config_store=InMemoryConfigStore(config or AppConfig(history_enabled=True)),
        history_store=history_store,
        id_factory=lambda: next(ids),
        clock=lambda: datetime(2026, 6, 22, 10, 0, tzinfo=timezone.utc),
    )


def make_entry(entry_id: str = "entry-1") -> TranslationHistoryEntry:
    return TranslationHistoryEntry(
        id=entry_id,
        source_text="hello",
        translated_text="hola",
        provider_name="fake",
        source_lang="en",
        target_lang="es",
        flow="clipboard",
        created_at="2026-06-22T10:00:00+00:00",
    )


def test_history_service_adds_and_lists_recent_translation() -> None:
    history_store = InMemoryHistoryStore()
    service = make_service(history_store)

    entry = service.add_translation(
        source_text="hello",
        translated_text="hola",
        provider_name="fake",
        source_lang="en",
        target_lang="es",
        flow="clipboard",
    )

    assert entry == make_entry()
    assert service.list_recent() == (make_entry(),)
    assert service.get("entry-1") == make_entry()


def test_history_service_respects_disabled_history() -> None:
    history_store = InMemoryHistoryStore()
    service = make_service(history_store, config=AppConfig(history_enabled=False))

    entry = service.add_translation(
        source_text="hello",
        translated_text="hola",
        provider_name="fake",
        source_lang="en",
        target_lang="es",
        flow="clipboard",
    )

    assert entry is None
    assert service.list_recent() == ()


def test_history_service_respects_retention_limit() -> None:
    history_store = InMemoryHistoryStore()
    service = make_service(
        history_store, config=AppConfig(history_enabled=True, history_max_entries=2)
    )

    for source_text in ("one", "two", "three"):
        service.add_translation(
            source_text=source_text,
            translated_text=f"{source_text} translated",
            provider_name="fake",
            source_lang="en",
            target_lang="es",
            flow="clipboard",
        )

    entries = service.list_recent()
    assert [entry.id for entry in entries] == ["entry-3", "entry-2"]
    assert [entry.source_text for entry in entries] == ["three", "two"]


def test_history_service_delete_and_clear() -> None:
    history_store = InMemoryHistoryStore((make_entry("entry-1"), make_entry("entry-2")))
    service = make_service(history_store)

    assert service.delete("entry-1") is True
    assert service.delete("missing") is False
    assert [entry.id for entry in service.list_recent()] == ["entry-2"]

    service.clear()

    assert service.list_recent() == ()


def test_history_service_does_not_store_empty_successes() -> None:
    history_store = InMemoryHistoryStore()
    service = make_service(history_store)

    entry = service.add_translation(
        source_text=" ",
        translated_text="hola",
        provider_name="fake",
        source_lang="en",
        target_lang="es",
        flow="clipboard",
    )

    assert entry is None
    assert service.list_recent() == ()


def test_json_file_history_store_handles_missing_and_malformed_files(tmp_path) -> None:
    history_path = tmp_path / "history.json"
    store = JsonFileHistoryStore(history_path)

    assert store.list_entries() == ()

    history_path.write_text("{not-json", encoding="utf-8")

    assert store.list_entries() == ()


def test_json_file_history_store_saves_and_loads_entries(tmp_path) -> None:
    history_path = tmp_path / "history.json"
    store = JsonFileHistoryStore(history_path)

    store.replace_entries((make_entry(),))

    assert store.list_entries() == (make_entry(),)
    assert (tmp_path / "history.json.tmp").exists() is False


def test_history_serialization_uses_text_metadata_only() -> None:
    payload = entries_to_dict((make_entry(),))
    payload_text = json.dumps(payload)

    assert payload["version"] == HISTORY_FILE_VERSION
    assert "hello" in payload_text
    assert "hola" in payload_text
    assert "screenshot" not in payload_text
    assert "image" not in payload_text
    assert entries_from_dict(payload) == (make_entry(),)


def test_history_deserialization_ignores_invalid_entries() -> None:
    payload = {
        "version": HISTORY_FILE_VERSION,
        "entries": [
            {"id": "missing-required-fields"},
            {
                "id": "entry-1",
                "source_text": "hello",
                "translated_text": "hola",
                "provider_name": "fake",
                "source_lang": "en",
                "target_lang": "es",
                "flow": "clipboard",
                "created_at": "2026-06-22T10:00:00+00:00",
            },
        ],
    }

    assert entries_from_dict(payload) == (make_entry(),)
