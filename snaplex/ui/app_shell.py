"""Minimal desktop shell for SnapLex."""

from __future__ import annotations

import asyncio
from collections.abc import Callable, Coroutine
from threading import Thread
from typing import Any

from snaplex.services import (
    ClipboardService,
    CaptureService,
    FakeCaptureService,
    FakeOcrService,
    HistoryService,
    OcrService,
    QtClipboardService,
    ScreenRegion,
    SettingsService,
    create_default_translation_pipeline,
)
from snaplex.services.translation_service import TranslationPipeline
from snaplex.storage import (
    JsonFileConfigStore,
    JsonFileHistoryStore,
    load_app_config_from_environment,
)
from snaplex.ui.clipboard_presenter import (
    ClipboardTranslationPresenter,
)
from snaplex.ui.region_selector import FixedRegionSelector, QtRegionSelector, RegionSelector
from snaplex.ui.screen_presenter import ScreenTranslationPresenter
from snaplex.ui.history_presenter import HistoryPresenter
from snaplex.ui.settings_presenter import SettingsFormState, SettingsPresenter
from snaplex.ui.translation_result import TranslationResultPresenter, TranslationResultStatus


def is_pyside_available() -> bool:
    try:
        import PySide6.QtWidgets  # noqa: F401
    except ModuleNotFoundError:
        return False

    return True


def launch_gui(
    presenter: ClipboardTranslationPresenter | None = None,
    screen_presenter: ScreenTranslationPresenter | None = None,
    clipboard_service: ClipboardService | None = None,
    capture_service: CaptureService | None = None,
    ocr_service: OcrService | None = None,
    pipeline: TranslationPipeline | None = None,
    screen_region: ScreenRegion | None = None,
    region_selector: RegionSelector | None = None,
    settings_service: SettingsService | None = None,
    history_service: HistoryService | None = None,
) -> int:
    try:
        from PySide6.QtCore import QObject, Qt, Signal
        from PySide6.QtWidgets import (
            QApplication,
            QCheckBox,
            QDialog,
            QDialogButtonBox,
            QDoubleSpinBox,
            QFormLayout,
            QHBoxLayout,
            QLabel,
            QLineEdit,
            QListWidget,
            QMainWindow,
            QPushButton,
            QSpinBox,
            QVBoxLayout,
            QWidget,
        )
    except ModuleNotFoundError:
        print(
            "PySide6 is not installed. Run `python -m pip install -e .[gui]` "
            "to start the desktop shell, or `python -m snaplex --no-gui` "
            "for a bootstrap check."
        )
        return 0

    app = QApplication.instance() or QApplication([])
    clipboard_service = clipboard_service or QtClipboardService.from_application()
    capture_service = capture_service or FakeCaptureService()
    ocr_service = ocr_service or FakeOcrService()
    config_store = JsonFileConfigStore(default_config=load_app_config_from_environment())
    settings_service = settings_service or SettingsService(config_store)
    settings_presenter = SettingsPresenter(settings_service)
    history_service = history_service or HistoryService(
        config_store=config_store,
        history_store=JsonFileHistoryStore(),
    )
    history_presenter = HistoryPresenter(
        history_service,
        on_copy_result=clipboard_service.set_text,
    )
    pipeline = pipeline or create_default_translation_pipeline(
        config_store=config_store,
    )
    presenter = presenter or ClipboardTranslationPresenter(
        on_copy_result=clipboard_service.set_text,
        history_service=history_service,
    )
    screen_presenter = screen_presenter or ScreenTranslationPresenter(
        on_copy_result=clipboard_service.set_text,
        history_service=history_service,
    )
    region_selector = region_selector or (
        FixedRegionSelector(screen_region) if screen_region is not None else QtRegionSelector()
    )
    active_presenter: dict[str, TranslationResultPresenter] = {"value": presenter}

    class UiSignals(QObject):
        refresh_requested = Signal()

    ui_signals = UiSignals()
    window = QMainWindow()
    window.setWindowTitle("SnapLex")
    window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

    central = QWidget()
    layout = QVBoxLayout(central)
    layout.addWidget(QLabel("SnapLex"))
    status_label = QLabel(presenter.state.status_text)
    source_label = QLabel("")
    result_label = QLabel("")
    provider_label = QLabel("")
    error_label = QLabel("")
    translate_button = QPushButton("Translate Clipboard")
    translate_screen_button = QPushButton("Translate Screen")
    settings_button = QPushButton("Settings")
    history_button = QPushButton("History")
    copy_button = QPushButton("Copy Result")
    retry_button = QPushButton("Retry")
    close_button = QPushButton("Close Result")
    for label in (status_label, source_label, result_label, provider_label, error_label):
        label.setWordWrap(True)

    def refresh_view() -> None:
        state = active_presenter["value"].state
        is_loading = state.status == TranslationResultStatus.LOADING
        status_label.setText(state.status_text)
        source_label.setText(state.source_text)
        result_label.setText(state.translated_text)
        provider_label.setText(f"Provider: {state.provider_name}" if state.provider_name else "")
        error_label.setText(state.error_message)
        translate_button.setEnabled(not is_loading)
        translate_screen_button.setEnabled(not is_loading)
        copy_button.setEnabled(state.can_copy)
        retry_button.setEnabled(state.can_retry and not is_loading)
        close_button.setEnabled(state.status != TranslationResultStatus.IDLE and not is_loading)

    def run_in_background(operation: Callable[[], Coroutine[Any, Any, object]]) -> None:
        def run_translation() -> None:
            asyncio.run(operation())
            ui_signals.refresh_requested.emit()

        Thread(target=run_translation, daemon=True).start()

    def handle_translate() -> None:
        active_presenter["value"] = presenter
        presenter.request_clipboard_translation()
        refresh_view()
        run_in_background(
            lambda: presenter.translate_clipboard(
                clipboard_service=clipboard_service,
                pipeline=pipeline,
            )
        )

    def handle_screen_translate() -> None:
        active_presenter["value"] = screen_presenter
        screen_presenter.request_screen_translation()
        refresh_view()
        selected_region = region_selector.select_region()
        if selected_region is None:
            screen_presenter.show_selection_cancelled()
            refresh_view()
            return

        run_in_background(
            lambda: screen_presenter.translate_region(
                region=selected_region,
                capture_service=capture_service,
                ocr_service=ocr_service,
                pipeline=pipeline,
            )
        )

    def handle_retry() -> None:
        active = active_presenter["value"]
        active.request_translation(source_text=active.state.source_text)
        refresh_view()
        if active is screen_presenter:
            run_in_background(
                lambda: screen_presenter.retry_translation(
                    capture_service=capture_service,
                    ocr_service=ocr_service,
                    pipeline=pipeline,
                )
            )
            return

        run_in_background(
            lambda: presenter.retry_translation(
                clipboard_service=clipboard_service,
                pipeline=pipeline,
            )
        )

    def handle_copy() -> None:
        active_presenter["value"].copy_result()

    def handle_close() -> None:
        active_presenter["value"].close_result()
        refresh_view()

    def handle_settings() -> None:
        state = settings_presenter.load_state()
        dialog = QDialog(window)
        dialog.setWindowTitle("SnapLex Settings")
        form = QFormLayout(dialog)
        source_lang_edit = QLineEdit(state.source_lang)
        target_lang_edit = QLineEdit(state.target_lang)
        provider_name_edit = QLineEdit(state.provider_name)
        provider_order_edit = QLineEdit(state.provider_order)
        libretranslate_base_url_edit = QLineEdit(state.libretranslate_base_url)
        libretranslate_api_key_env_var_edit = QLineEdit(state.libretranslate_api_key_env_var)
        libretranslate_timeout_spin = _double_spin_box(
            state.libretranslate_timeout_seconds,
            QDoubleSpinBox,
        )
        libretranslate_retry_spin = _int_spin_box(state.libretranslate_retry_count, QSpinBox)
        openai_base_url_edit = QLineEdit(state.openai_base_url)
        openai_api_key_env_var_edit = QLineEdit(state.openai_api_key_env_var)
        openai_timeout_spin = _double_spin_box(state.openai_timeout_seconds, QDoubleSpinBox)
        openai_retry_spin = _int_spin_box(state.openai_retry_count, QSpinBox)
        openai_model_edit = QLineEdit(state.openai_model)
        deepl_base_url_edit = QLineEdit(state.deepl_base_url)
        deepl_api_key_env_var_edit = QLineEdit(state.deepl_api_key_env_var)
        deepl_timeout_spin = _double_spin_box(state.deepl_timeout_seconds, QDoubleSpinBox)
        deepl_retry_spin = _int_spin_box(state.deepl_retry_count, QSpinBox)
        deepl_model_type_edit = QLineEdit(state.deepl_model_type)
        history_enabled_checkbox = QCheckBox()
        history_enabled_checkbox.setChecked(state.history_enabled)
        history_max_entries_spin = _int_spin_box(state.history_max_entries, QSpinBox)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )

        form.addRow("Source", source_lang_edit)
        form.addRow("Target", target_lang_edit)
        form.addRow("Provider", provider_name_edit)
        form.addRow("Fallback Order", provider_order_edit)
        form.addRow("Libre URL", libretranslate_base_url_edit)
        form.addRow("Libre Key Env", libretranslate_api_key_env_var_edit)
        form.addRow("Libre Timeout", libretranslate_timeout_spin)
        form.addRow("Libre Retry", libretranslate_retry_spin)
        form.addRow("OpenAI URL", openai_base_url_edit)
        form.addRow("OpenAI Key Env", openai_api_key_env_var_edit)
        form.addRow("OpenAI Timeout", openai_timeout_spin)
        form.addRow("OpenAI Retry", openai_retry_spin)
        form.addRow("OpenAI Model", openai_model_edit)
        form.addRow("DeepL URL", deepl_base_url_edit)
        form.addRow("DeepL Key Env", deepl_api_key_env_var_edit)
        form.addRow("DeepL Timeout", deepl_timeout_spin)
        form.addRow("DeepL Retry", deepl_retry_spin)
        form.addRow("DeepL Model Type", deepl_model_type_edit)
        form.addRow("History", history_enabled_checkbox)
        form.addRow("History Max", history_max_entries_spin)
        form.addRow(buttons)

        def apply_settings() -> None:
            settings_presenter.apply_state(
                SettingsFormState(
                    source_lang=source_lang_edit.text(),
                    target_lang=target_lang_edit.text(),
                    provider_name=provider_name_edit.text(),
                    provider_order=provider_order_edit.text(),
                    libretranslate_base_url=libretranslate_base_url_edit.text(),
                    libretranslate_api_key_env_var=libretranslate_api_key_env_var_edit.text(),
                    libretranslate_timeout_seconds=libretranslate_timeout_spin.value(),
                    libretranslate_retry_count=libretranslate_retry_spin.value(),
                    openai_base_url=openai_base_url_edit.text(),
                    openai_api_key_env_var=openai_api_key_env_var_edit.text(),
                    openai_timeout_seconds=openai_timeout_spin.value(),
                    openai_retry_count=openai_retry_spin.value(),
                    openai_model=openai_model_edit.text(),
                    deepl_base_url=deepl_base_url_edit.text(),
                    deepl_api_key_env_var=deepl_api_key_env_var_edit.text(),
                    deepl_timeout_seconds=deepl_timeout_spin.value(),
                    deepl_retry_count=deepl_retry_spin.value(),
                    deepl_model_type=deepl_model_type_edit.text(),
                    history_enabled=history_enabled_checkbox.isChecked(),
                    history_max_entries=history_max_entries_spin.value(),
                )
            )
            dialog.accept()

        buttons.accepted.connect(apply_settings)
        buttons.rejected.connect(dialog.reject)
        dialog.exec()

    def handle_history() -> None:
        dialog = QDialog(window)
        dialog.setWindowTitle("SnapLex History")
        layout = QVBoxLayout(dialog)
        status = QLabel("")
        history_list = QListWidget()
        copy_history_button = QPushButton("Copy")
        delete_history_button = QPushButton("Delete")
        clear_history_button = QPushButton("Clear")
        close_history_button = QPushButton("Close")
        button_row = QHBoxLayout()
        button_row.addWidget(copy_history_button)
        button_row.addWidget(delete_history_button)
        button_row.addWidget(clear_history_button)
        button_row.addWidget(close_history_button)
        layout.addWidget(status)
        layout.addWidget(history_list)
        layout.addLayout(button_row)
        entry_ids: list[str] = []

        def refresh_history() -> None:
            state = history_presenter.load_state()
            status.setText(state.status_text)
            history_list.clear()
            entry_ids.clear()
            for entry in state.entries:
                entry_ids.append(entry.id)
                history_list.addItem(
                    f"{entry.created_at} | {entry.flow} | "
                    f"{entry.source_text} -> {entry.translated_text}"
                )

        def selected_entry_id() -> str | None:
            row = history_list.currentRow()
            if row < 0 or row >= len(entry_ids):
                return None
            return entry_ids[row]

        def copy_selected_history() -> None:
            entry_id = selected_entry_id()
            if entry_id is not None:
                history_presenter.copy_entry(entry_id)

        def delete_selected_history() -> None:
            entry_id = selected_entry_id()
            if entry_id is not None:
                history_presenter.delete_entry(entry_id)
                refresh_history()

        def clear_history() -> None:
            history_presenter.clear_history()
            refresh_history()

        copy_history_button.clicked.connect(copy_selected_history)
        delete_history_button.clicked.connect(delete_selected_history)
        clear_history_button.clicked.connect(clear_history)
        close_history_button.clicked.connect(dialog.accept)
        refresh_history()
        dialog.resize(520, 280)
        dialog.exec()

    ui_signals.refresh_requested.connect(refresh_view)
    translate_button.clicked.connect(handle_translate)
    translate_screen_button.clicked.connect(handle_screen_translate)
    settings_button.clicked.connect(handle_settings)
    history_button.clicked.connect(handle_history)
    retry_button.clicked.connect(handle_retry)
    copy_button.clicked.connect(handle_copy)
    close_button.clicked.connect(handle_close)
    layout.addWidget(translate_button)
    layout.addWidget(translate_screen_button)
    layout.addWidget(settings_button)
    layout.addWidget(history_button)
    layout.addWidget(source_label)
    layout.addWidget(result_label)
    layout.addWidget(provider_label)
    layout.addWidget(error_label)
    layout.addWidget(copy_button)
    layout.addWidget(retry_button)
    layout.addWidget(close_button)
    layout.addWidget(status_label)
    refresh_view()

    window.setCentralWidget(central)
    window.resize(360, 240)
    window.show()

    return app.exec()


def _double_spin_box(value: float, spin_box_type: type[Any]) -> Any:
    spin_box = spin_box_type()
    spin_box.setRange(0.1, 120.0)
    spin_box.setDecimals(1)
    spin_box.setValue(value)
    return spin_box


def _int_spin_box(value: int, spin_box_type: type[Any]) -> Any:
    spin_box = spin_box_type()
    spin_box.setRange(0, 1000)
    spin_box.setValue(value)
    return spin_box
