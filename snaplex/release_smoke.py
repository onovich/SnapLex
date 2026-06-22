"""Deterministic release smoke checks for packaged SnapLex builds."""

from __future__ import annotations

import os
import asyncio
from pathlib import Path

from snaplex.services import (
    FakeCaptureService,
    FakeOcrService,
    HistoryService,
    InMemoryClipboardService,
    ScreenRegion,
    ScreenTranslationService,
    SettingsService,
    create_default_translation_pipeline,
)
from snaplex.storage import (
    APP_DATA_DIR_ENV_VAR,
    CONFIG_FILE_NAME,
    HISTORY_FILE_NAME,
    JsonFileConfigStore,
    JsonFileHistoryStore,
    default_app_data_dir,
)


class PackagedSmokeError(RuntimeError):
    """Raised when deterministic packaged workflow smoke fails."""


def run_packaged_workflow_smoke() -> tuple[str, ...]:
    """Run clipboard/settings/history smoke against packaged runtime modules."""

    if not os.environ.get(APP_DATA_DIR_ENV_VAR, "").strip():
        raise PackagedSmokeError(f"{APP_DATA_DIR_ENV_VAR} must point to a smoke data directory.")

    app_data_dir = default_app_data_dir()
    config_store = JsonFileConfigStore(app_data_dir / CONFIG_FILE_NAME)
    history_store = JsonFileHistoryStore(app_data_dir / HISTORY_FILE_NAME)
    settings_service = SettingsService(config_store)
    history_service = HistoryService(
        config_store=config_store,
        history_store=history_store,
        id_factory=lambda: "packaged-smoke-entry",
    )
    clipboard_service = InMemoryClipboardService("hello")

    settings_service.update_provider_selection(provider_name="fake", provider_order=("fake",))
    settings_service.update_language_defaults(source_lang="auto", target_lang="en")
    settings_service.update_history_preferences(enabled=True, max_entries=5)

    config = settings_service.load()
    if config.provider_name != "fake" or config.provider_order != ("fake",):
        raise PackagedSmokeError("fake provider settings were not persisted.")
    if not config.history_enabled or config.history_max_entries != 5:
        raise PackagedSmokeError("history settings were not persisted.")

    pipeline = create_default_translation_pipeline(config_store=config_store)
    response = pipeline.translate_text(clipboard_service.get_text())
    if response.provider_name != "fake" or response.translated_text != "hello [en]":
        raise PackagedSmokeError("fake clipboard translation did not return the expected result.")
    clipboard_service.set_text(response.translated_text)
    if clipboard_service.get_text() != "hello [en]":
        raise PackagedSmokeError("clipboard copy smoke did not preserve the translated result.")

    entry = history_service.add_translation(
        source_text="hello",
        translated_text=response.translated_text,
        provider_name=response.provider_name,
        source_lang=response.source_lang,
        target_lang=response.target_lang,
        flow="clipboard",
    )
    if entry is None:
        raise PackagedSmokeError("history entry was not recorded while history was enabled.")
    if len(history_service.list_recent()) != 1:
        raise PackagedSmokeError("history list did not contain the recorded entry.")
    if not history_service.delete(entry.id):
        raise PackagedSmokeError("history delete did not remove the recorded entry.")

    screen_service = ScreenTranslationService(
        capture_service=FakeCaptureService(),
        ocr_service=FakeOcrService(text="screen hello"),
        pipeline=pipeline,
    )
    screen_response = asyncio.run(screen_service.translate_region(ScreenRegion(0, 0, 10, 10)))
    if (
        screen_response.source_text != "screen hello"
        or screen_response.translated_text != "screen hello [en]"
    ):
        raise PackagedSmokeError("screen fake capture/OCR translation smoke failed.")

    history_service.add_translation(
        source_text="again",
        translated_text="again [en]",
        provider_name="fake",
        source_lang="auto",
        target_lang="en",
        flow="clipboard",
    )
    history_service.clear()
    if history_service.list_recent():
        raise PackagedSmokeError("history clear left entries behind.")

    _assert_inside_app_data(config_store.config_path, app_data_dir, "config")
    _assert_inside_app_data(history_store.history_path, app_data_dir, "history")

    return (
        f"app data: {app_data_dir}",
        "settings persistence: fake provider, history enabled",
        "clipboard translation: hello -> hello [en]",
        "screen fake capture/OCR translation: screen hello -> screen hello [en]",
        "history record/list/delete/clear: PASS",
    )


def _assert_inside_app_data(path: Path, app_data_dir: Path, label: str) -> None:
    try:
        path.resolve().relative_to(app_data_dir.resolve())
    except ValueError as exc:
        raise PackagedSmokeError(f"{label} file escaped the smoke app data directory.") from exc
