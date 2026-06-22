"""History presentation boundary."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from snaplex.services import HistoryService
from snaplex.storage import TranslationHistoryEntry


@dataclass(frozen=True)
class HistoryListState:
    history_enabled: bool
    entries: tuple[TranslationHistoryEntry, ...]
    status_text: str


class HistoryPresenter:
    def __init__(
        self,
        history_service: HistoryService,
        *,
        on_copy_result: Callable[[str], None] | None = None,
    ) -> None:
        self._history_service = history_service
        self._on_copy_result = on_copy_result

    def load_state(self) -> HistoryListState:
        enabled = self._history_service.is_enabled()
        entries = self._history_service.list_recent()
        if not enabled:
            status_text = "History disabled"
        elif entries:
            status_text = "History ready"
        else:
            status_text = "History empty"
        return HistoryListState(
            history_enabled=enabled,
            entries=entries,
            status_text=status_text,
        )

    def copy_entry(self, entry_id: str) -> bool:
        entry = self._history_service.get(entry_id)
        if entry is None or self._on_copy_result is None:
            return False
        self._on_copy_result(entry.translated_text)
        return True

    def delete_entry(self, entry_id: str) -> bool:
        return self._history_service.delete(entry_id)

    def clear_history(self) -> None:
        self._history_service.clear()
