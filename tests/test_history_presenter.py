from snaplex.services import HistoryService
from snaplex.storage import (
    AppConfig,
    InMemoryConfigStore,
    InMemoryHistoryStore,
    TranslationHistoryEntry,
)
from snaplex.ui.history_presenter import HistoryPresenter


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


def make_presenter(
    *,
    config: AppConfig | None = None,
    copied: list[str] | None = None,
) -> tuple[HistoryPresenter, InMemoryHistoryStore]:
    history_store = InMemoryHistoryStore((make_entry("entry-1"),))
    service = HistoryService(
        config_store=InMemoryConfigStore(config or AppConfig(history_enabled=True)),
        history_store=history_store,
    )
    copied_results = [] if copied is None else copied
    return HistoryPresenter(service, on_copy_result=copied_results.append), history_store


def test_history_presenter_loads_enabled_history_state() -> None:
    presenter, _history_store = make_presenter()

    state = presenter.load_state()

    assert state.history_enabled is True
    assert state.status_text == "History ready"
    assert [entry.id for entry in state.entries] == ["entry-1"]
    assert state.entry_views[0].title == "Clipboard | fake | en -> es"
    assert state.entry_views[0].detail == "hello -> hola"


def test_history_presenter_reports_disabled_history() -> None:
    presenter, _history_store = make_presenter(config=AppConfig(history_enabled=False))

    state = presenter.load_state()

    assert state.history_enabled is False
    assert state.status_text == "History disabled"


def test_history_presenter_clips_long_entry_views() -> None:
    history_store = InMemoryHistoryStore(
        (
            TranslationHistoryEntry(
                id="entry-long",
                source_text="source " * 40,
                translated_text="translated " * 40,
                provider_name="fake",
                source_lang="en",
                target_lang="es",
                flow="screen",
                created_at="2026-06-22T10:00:00+00:00",
            ),
        )
    )
    service = HistoryService(
        config_store=InMemoryConfigStore(AppConfig(history_enabled=True)),
        history_store=history_store,
    )
    presenter = HistoryPresenter(service)

    state = presenter.load_state()

    view = state.entry_views[0]
    assert view.title == "Screen | fake | en -> es"
    assert len(view.detail) < 210
    assert view.detail.endswith("...")


def test_history_presenter_copies_deletes_and_clears_entries() -> None:
    copied: list[str] = []
    presenter, history_store = make_presenter(copied=copied)

    assert presenter.copy_entry("entry-1") is True
    assert presenter.copy_entry("missing") is False
    assert copied == ["hola"]
    assert presenter.delete_entry("entry-1") is True
    assert history_store.list_entries() == ()

    history_store.replace_entries((make_entry("entry-2"),))
    presenter.clear_history()

    assert history_store.list_entries() == ()
