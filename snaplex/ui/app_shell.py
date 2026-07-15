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
from snaplex.services.provider_setup import ProviderSetupState
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
from snaplex.ui.style import SNAPLEX_FONT_FAMILY, build_app_stylesheet
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
        from PySide6.QtGui import QFont
        from PySide6.QtWidgets import (
            QApplication,
            QCheckBox,
            QComboBox,
            QDialog,
            QDialogButtonBox,
            QDoubleSpinBox,
            QFormLayout,
            QGroupBox,
            QHBoxLayout,
            QLabel,
            QLineEdit,
            QListWidget,
            QMainWindow,
            QPushButton,
            QScrollArea,
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

    existing_application = QApplication.instance()
    app: QApplication
    if isinstance(existing_application, QApplication):
        app = existing_application
    else:
        app = QApplication([])
    app.setFont(QFont(SNAPLEX_FONT_FAMILY, 9))
    app.setStyleSheet(build_app_stylesheet())
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
    central.setObjectName("SnapLexRoot")
    layout = QVBoxLayout(central)
    layout.setContentsMargins(18, 16, 18, 16)
    layout.setSpacing(10)
    title_label = QLabel("SnapLex")
    title_label.setObjectName("AppTitle")
    subtitle_label = QLabel("Translate clipboard text or a selected screen region.")
    subtitle_label.setObjectName("AppSubtitle")
    status_label = QLabel(presenter.state.status_text)
    status_label.setObjectName("StatusText")
    source_label = QLabel("")
    source_label.setObjectName("ResultText")
    result_label = QLabel("")
    result_label.setObjectName("ResultText")
    provider_label = QLabel("")
    provider_label.setObjectName("ProviderText")
    provider_notice_label = QLabel("")
    provider_notice_label.setObjectName("ProviderNotice")
    error_label = QLabel("")
    error_label.setObjectName("ErrorText")
    source_caption_label = QLabel("Source")
    source_caption_label.setObjectName("SectionLabel")
    result_caption_label = QLabel("Translation")
    result_caption_label.setObjectName("SectionLabel")
    translate_button = QPushButton("Translate Clipboard")
    translate_button.setObjectName("PrimaryAction")
    translate_screen_button = QPushButton("Translate Screen")
    settings_button = QPushButton("Settings")
    history_button = QPushButton("History")
    copy_button = QPushButton("Copy Result")
    retry_button = QPushButton("Retry")
    close_button = QPushButton("Close Result")
    for label in (
        status_label,
        source_label,
        result_label,
        provider_label,
        provider_notice_label,
        error_label,
    ):
        label.setWordWrap(True)
    for label in (source_label, result_label, error_label):
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

    def refresh_view() -> None:
        state = active_presenter["value"].state
        is_loading = state.status == TranslationResultStatus.LOADING
        status_label.setText(state.status_text)
        source_label.setText(state.source_text)
        result_label.setText(state.translated_text)
        provider_label.setText(f"Provider: {state.provider_name}" if state.provider_name else "")
        provider_notice_label.setText(state.provider_notice)
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
        dialog.resize(640, 680)
        outer_layout = QVBoxLayout(dialog)

        title_label = QLabel("Provider Setup")
        title_label.setObjectName("settingsTitle")
        title_label.setStyleSheet("font-size: 18px; font-weight: 600;")
        intro_label = QLabel(
            "Choose a provider, keep API keys in environment variables, and test "
            "readiness before trying real translation."
        )
        intro_label.setWordWrap(True)
        outer_layout.addWidget(title_label)
        outer_layout.addWidget(intro_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        section_layout = QVBoxLayout(scroll_content)

        provider_group = QGroupBox("Translation Provider")
        provider_form = QFormLayout(provider_group)
        provider_combo = QComboBox()
        provider_combo.addItems(list(state.provider_choices))
        provider_index = provider_combo.findText(state.provider_name)
        if provider_index >= 0:
            provider_combo.setCurrentIndex(provider_index)
        source_lang_edit = QLineEdit(state.source_lang)
        target_lang_edit = QLineEdit(state.target_lang)
        provider_order_edit = QLineEdit(state.provider_order)
        readiness_label = QLabel("")
        readiness_detail_label = QLabel("")
        env_status_label = QLabel("")
        connection_result_label = QLabel("")
        connect_account_button = QPushButton("Connect account (future)")
        connect_account_button.setEnabled(False)
        test_connection_button = QPushButton("Test Connection")
        for label in (
            readiness_label,
            readiness_detail_label,
            env_status_label,
            connection_result_label,
        ):
            label.setWordWrap(True)

        provider_form.addRow("Provider", provider_combo)
        provider_form.addRow("Fallback Order", provider_order_edit)
        provider_form.addRow("Source", source_lang_edit)
        provider_form.addRow("Target", target_lang_edit)
        provider_form.addRow("Readiness", readiness_label)
        provider_form.addRow("Details", readiness_detail_label)
        provider_form.addRow("Env Var", env_status_label)
        provider_form.addRow(connect_account_button)
        provider_form.addRow(test_connection_button)
        provider_form.addRow("Test Result", connection_result_label)

        libretranslate_group = QGroupBox("LibreTranslate")
        libretranslate_form = QFormLayout(libretranslate_group)
        libretranslate_base_url_edit = QLineEdit(state.libretranslate_base_url)
        libretranslate_api_key_env_var_edit = QLineEdit(state.libretranslate_api_key_env_var)
        libretranslate_timeout_spin = _double_spin_box(
            state.libretranslate_timeout_seconds,
            QDoubleSpinBox,
        )
        libretranslate_retry_spin = _int_spin_box(state.libretranslate_retry_count, QSpinBox)
        libretranslate_form.addRow("Base URL", libretranslate_base_url_edit)
        libretranslate_form.addRow("API Key Env", libretranslate_api_key_env_var_edit)
        libretranslate_form.addRow("Timeout", libretranslate_timeout_spin)
        libretranslate_form.addRow("Retry", libretranslate_retry_spin)

        openai_group = QGroupBox("OpenAI")
        openai_form = QFormLayout(openai_group)
        openai_base_url_edit = QLineEdit(state.openai_base_url)
        openai_api_key_env_var_edit = QLineEdit(state.openai_api_key_env_var)
        openai_timeout_spin = _double_spin_box(state.openai_timeout_seconds, QDoubleSpinBox)
        openai_retry_spin = _int_spin_box(state.openai_retry_count, QSpinBox)
        openai_model_edit = QLineEdit(state.openai_model)
        openai_form.addRow("Base URL", openai_base_url_edit)
        openai_form.addRow("API Key Env", openai_api_key_env_var_edit)
        openai_form.addRow("Timeout", openai_timeout_spin)
        openai_form.addRow("Retry", openai_retry_spin)
        openai_form.addRow("Model", openai_model_edit)

        deepl_group = QGroupBox("DeepL")
        deepl_form = QFormLayout(deepl_group)
        deepl_base_url_edit = QLineEdit(state.deepl_base_url)
        deepl_api_key_env_var_edit = QLineEdit(state.deepl_api_key_env_var)
        deepl_timeout_spin = _double_spin_box(state.deepl_timeout_seconds, QDoubleSpinBox)
        deepl_retry_spin = _int_spin_box(state.deepl_retry_count, QSpinBox)
        deepl_model_type_edit = QLineEdit(state.deepl_model_type)
        deepl_form.addRow("Base URL", deepl_base_url_edit)
        deepl_form.addRow("API Key Env", deepl_api_key_env_var_edit)
        deepl_form.addRow("Timeout", deepl_timeout_spin)
        deepl_form.addRow("Retry", deepl_retry_spin)
        deepl_form.addRow("Model Type", deepl_model_type_edit)

        history_group = QGroupBox("History")
        history_form = QFormLayout(history_group)
        history_enabled_checkbox = QCheckBox()
        history_enabled_checkbox.setChecked(state.history_enabled)
        history_max_entries_spin = _int_spin_box(state.history_max_entries, QSpinBox)
        history_form.addRow("Enabled", history_enabled_checkbox)
        history_form.addRow("Max Entries", history_max_entries_spin)

        section_layout.addWidget(provider_group)
        section_layout.addWidget(libretranslate_group)
        section_layout.addWidget(openai_group)
        section_layout.addWidget(deepl_group)
        section_layout.addWidget(history_group)
        section_layout.addStretch(1)
        scroll_area.setWidget(scroll_content)
        outer_layout.addWidget(scroll_area)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        outer_layout.addWidget(buttons)

        def current_form_state() -> SettingsFormState:
            return SettingsFormState(
                source_lang=source_lang_edit.text(),
                target_lang=target_lang_edit.text(),
                provider_name=provider_combo.currentText(),
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

        def selected_setup() -> ProviderSetupState | None:
            refreshed_state = settings_presenter.load_state()
            setups = {setup.provider_name: setup for setup in refreshed_state.provider_setups}
            return setups.get(provider_combo.currentText())

        def refresh_provider_setup() -> None:
            setup = selected_setup()
            if setup is None:
                readiness_label.setText("Provider is not supported")
                readiness_detail_label.setText("Choose fake, LibreTranslate, OpenAI, or DeepL.")
                env_status_label.setText("")
                test_connection_button.setEnabled(False)
                return

            readiness_label.setText(setup.status_text)
            readiness_detail_label.setText(setup.detail_text)
            if setup.api_key_env_var:
                env_status = "present" if setup.api_key_present else "missing"
                env_status_label.setText(f"{setup.api_key_env_var}: {env_status}")
            else:
                env_status_label.setText("No API key env var configured.")
            connect_account_button.setToolTip(setup.connect_account_detail)
            test_connection_button.setEnabled(setup.is_real_provider)

        def apply_settings() -> None:
            settings_presenter.apply_state(current_form_state())
            dialog.accept()

        def run_connection_test() -> None:
            saved_state = settings_presenter.apply_state(current_form_state())
            result = settings_presenter.test_provider_connection(saved_state.provider_name)
            connection_result_label.setText(f"{result.status_text}: {result.detail_text}")
            refresh_provider_setup()

        provider_combo.currentTextChanged.connect(lambda _text: refresh_provider_setup())
        test_connection_button.clicked.connect(run_connection_test)
        buttons.accepted.connect(apply_settings)
        buttons.rejected.connect(dialog.reject)
        refresh_provider_setup()
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
    primary_actions = QHBoxLayout()
    primary_actions.addWidget(translate_button)
    primary_actions.addWidget(translate_screen_button)
    utility_actions = QHBoxLayout()
    utility_actions.addWidget(settings_button)
    utility_actions.addWidget(history_button)

    result_group = QGroupBox("Result")
    result_layout = QVBoxLayout(result_group)
    result_layout.setSpacing(6)
    result_layout.addWidget(source_caption_label)
    result_layout.addWidget(source_label)
    result_layout.addWidget(result_caption_label)
    result_layout.addWidget(result_label)
    result_layout.addWidget(provider_label)
    result_layout.addWidget(provider_notice_label)
    result_layout.addWidget(error_label)

    result_actions = QHBoxLayout()
    result_actions.addWidget(copy_button)
    result_actions.addWidget(retry_button)
    result_actions.addWidget(close_button)
    result_layout.addLayout(result_actions)

    layout.addWidget(title_label)
    layout.addWidget(subtitle_label)
    layout.addLayout(primary_actions)
    layout.addLayout(utility_actions)
    layout.addWidget(result_group)
    layout.addWidget(status_label)
    refresh_view()

    window.setCentralWidget(central)
    window.resize(460, 420)
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
