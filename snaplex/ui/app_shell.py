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
from snaplex.ui.translation_result import (
    TranslationResultPresenter,
    TranslationResultStatus,
    build_result_display,
)


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
        from PySide6.QtCore import QObject, QSize, Qt, Signal
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
            QListWidgetItem,
            QMainWindow,
            QPlainTextEdit,
            QPushButton,
            QScrollArea,
            QSpinBox,
            QStyle,
            QTabWidget,
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
    status_label.setObjectName("StatusPill")
    source_label = QPlainTextEdit()
    source_label.setObjectName("ResultText")
    result_label = QPlainTextEdit()
    result_label.setObjectName("ResultText")
    provider_label = QLabel("")
    provider_label.setObjectName("ProviderText")
    provider_notice_label = QLabel("")
    provider_notice_label.setObjectName("ProviderNotice")
    error_label = QLabel("")
    error_label.setObjectName("ErrorText")
    result_state_label = QLabel("")
    result_state_label.setObjectName("ResultStateBadge")
    source_caption_label = QLabel("Source")
    source_caption_label.setObjectName("SectionLabel")
    result_caption_label = QLabel("Translation")
    result_caption_label.setObjectName("SectionLabel")
    translate_button = QPushButton("Translate Clipboard")
    translate_button.setObjectName("PrimaryAction")
    translate_screen_button = QPushButton("Translate Screen")
    translate_screen_button.setObjectName("PrimaryAction")
    settings_button = QPushButton("Settings")
    settings_button.setObjectName("SecondaryAction")
    history_button = QPushButton("History")
    history_button.setObjectName("SecondaryAction")
    copy_button = QPushButton("Copy Result")
    copy_button.setObjectName("ResultAction")
    retry_button = QPushButton("Retry")
    retry_button.setObjectName("ResultAction")
    close_button = QPushButton("Close Result")
    close_button.setObjectName("ResultAction")
    app_style = window.style()
    button_icons = (
        (translate_button, QStyle.StandardPixmap.SP_DialogApplyButton),
        (translate_screen_button, QStyle.StandardPixmap.SP_DesktopIcon),
        (settings_button, QStyle.StandardPixmap.SP_FileDialogDetailedView),
        (history_button, QStyle.StandardPixmap.SP_FileDialogListView),
        (copy_button, QStyle.StandardPixmap.SP_DialogSaveButton),
        (retry_button, QStyle.StandardPixmap.SP_BrowserReload),
        (close_button, QStyle.StandardPixmap.SP_DialogCloseButton),
    )
    for button, icon_name in button_icons:
        button.setIcon(app_style.standardIcon(icon_name))
        button.setIconSize(QSize(16, 16))
    translate_button.setAccessibleName("Translate clipboard text")
    translate_button.setToolTip("Translate the current clipboard text.")
    translate_screen_button.setAccessibleName("Translate selected screen region")
    translate_screen_button.setToolTip("Select a screen region and translate detected text.")
    settings_button.setAccessibleName("Open Settings")
    settings_button.setToolTip("Configure provider setup, languages, and history.")
    history_button.setAccessibleName("Open History")
    history_button.setToolTip("Review recent translations when history is enabled.")
    copy_button.setAccessibleName("Copy translation result")
    retry_button.setAccessibleName("Retry translation")
    close_button.setAccessibleName("Close result")
    translate_button.setMinimumWidth(160)
    translate_screen_button.setMinimumWidth(160)
    settings_button.setMinimumWidth(120)
    history_button.setMinimumWidth(120)
    for label in (
        status_label,
        provider_label,
        provider_notice_label,
        error_label,
    ):
        label.setWordWrap(True)
    error_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    for text_area in (source_label, result_label):
        text_area.setReadOnly(True)
        text_area.setTabChangesFocus(True)
        text_area.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        text_area.setMinimumHeight(74)
        text_area.setMaximumHeight(132)
    source_label.setAccessibleName("Source text")
    result_label.setAccessibleName("Translated text")

    def refresh_view() -> None:
        state = active_presenter["value"].state
        display = build_result_display(state)
        is_loading = state.status == TranslationResultStatus.LOADING
        status_label.setText(state.status_text)
        result_state_label.setText(display.state_label)
        source_label.setPlainText(display.source_text)
        result_label.setPlainText(display.translated_text)
        provider_label.setText(display.provider_text)
        provider_label.setVisible(display.provider_visible)
        provider_notice_label.setText(display.provider_notice)
        provider_notice_label.setVisible(display.provider_notice_visible)
        error_label.setText(display.error_message)
        error_label.setVisible(display.error_visible)
        for widget in (status_label, result_state_label):
            _set_result_state_property(widget, state.status.value)
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
        settings_tabs = QTabWidget()
        settings_tabs.setAccessibleName("Settings sections")

        provider_group = QGroupBox("Provider Setup")
        provider_form = QFormLayout(provider_group)
        provider_combo = QComboBox()
        _set_accessible(
            provider_combo, "Provider", "Choose fake, LibreTranslate, OpenAI, or DeepL."
        )
        provider_combo.addItems(list(state.provider_choices))
        provider_index = provider_combo.findText(state.provider_name)
        if provider_index >= 0:
            provider_combo.setCurrentIndex(provider_index)
        source_lang_edit = QLineEdit(state.source_lang)
        _set_accessible(source_lang_edit, "Source language", "Use auto for automatic detection.")
        target_lang_edit = QLineEdit(state.target_lang)
        _set_accessible(
            target_lang_edit, "Target language", "Language code used for new translations."
        )
        provider_order_edit = QLineEdit(state.provider_order)
        _set_accessible(
            provider_order_edit,
            "Fallback provider order",
            "Comma-separated provider fallback order. Use fake only for smoke mode.",
        )
        readiness_label = QLabel("")
        readiness_detail_label = QLabel("")
        env_status_label = QLabel("")
        credential_result_label = QLabel("")
        connection_result_label = QLabel("")
        connect_account_button = QPushButton("Connect account (future)")
        connect_account_button.setEnabled(False)
        _set_accessible(
            connect_account_button,
            "Connect account future option",
            "Disabled until secure account or cloud credential support is designed.",
        )
        test_connection_button = QPushButton("Test Connection")
        _set_accessible(
            test_connection_button,
            "Test provider connection",
            "Save current settings and test the selected real provider configuration.",
        )
        for label in (
            readiness_label,
            readiness_detail_label,
            env_status_label,
            credential_result_label,
            connection_result_label,
        ):
            label.setWordWrap(True)

        provider_form.addRow("Provider", provider_combo)
        provider_form.addRow("Fallback Order", provider_order_edit)
        provider_form.addRow("Readiness", readiness_label)
        provider_form.addRow("Details", readiness_detail_label)
        provider_form.addRow("Env Var", env_status_label)
        provider_form.addRow("Credential", credential_result_label)
        provider_form.addRow(connect_account_button)
        provider_form.addRow(test_connection_button)
        provider_form.addRow("Test Result", connection_result_label)

        language_group = QGroupBox("Language Defaults")
        language_form = QFormLayout(language_group)
        language_form.addRow("Source", source_lang_edit)
        language_form.addRow("Target", target_lang_edit)

        credential_source_values = {
            "": "Legacy env var",
            "environment": "Environment variable",
            "keyring": "Local secure credential",
        }

        def credential_source_combo(initial_source: str) -> QComboBox:
            combo = QComboBox()
            for source_value, label in credential_source_values.items():
                combo.addItem(label, source_value)
            index = combo.findData(initial_source)
            combo.setCurrentIndex(index if index >= 0 else 0)
            _set_accessible(
                combo,
                "Credential source",
                "Choose where SnapLex resolves the provider credential.",
            )
            return combo

        def credential_controls(
            provider_name: str,
            initial_source: str,
            initial_identifier: str,
        ) -> tuple[QComboBox, QLineEdit, QLineEdit, QPushButton, QPushButton, QWidget]:
            source_combo = credential_source_combo(initial_source)
            identifier_edit = QLineEdit(initial_identifier)
            _set_accessible(identifier_edit, f"{provider_name} credential reference")
            secret_edit = QLineEdit("")
            secret_edit.setEchoMode(QLineEdit.EchoMode.Password)
            _set_accessible(secret_edit, f"{provider_name} credential secret")
            save_credential_button = QPushButton("Save")
            _set_accessible(save_credential_button, f"Save {provider_name} credential")
            delete_credential_button = QPushButton("Delete")
            _set_accessible(delete_credential_button, f"Delete {provider_name} credential")
            actions = QWidget()
            actions_layout = QHBoxLayout(actions)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.addWidget(secret_edit)
            actions_layout.addWidget(save_credential_button)
            actions_layout.addWidget(delete_credential_button)

            def update_enabled() -> None:
                keyring_selected = source_combo.currentData() == "keyring"
                secret_edit.setEnabled(keyring_selected)
                save_credential_button.setEnabled(keyring_selected)
                delete_credential_button.setEnabled(keyring_selected)

            source_combo.currentIndexChanged.connect(lambda _index: update_enabled())
            update_enabled()
            return (
                source_combo,
                identifier_edit,
                secret_edit,
                save_credential_button,
                delete_credential_button,
                actions,
            )

        libretranslate_group = QGroupBox("LibreTranslate")
        libretranslate_form = QFormLayout(libretranslate_group)
        libretranslate_base_url_edit = QLineEdit(state.libretranslate_base_url)
        _set_accessible(libretranslate_base_url_edit, "LibreTranslate base URL")
        libretranslate_api_key_env_var_edit = QLineEdit(state.libretranslate_api_key_env_var)
        _set_secret_env_accessible(
            libretranslate_api_key_env_var_edit, "LibreTranslate API key env var"
        )
        (
            libretranslate_credential_source_combo,
            libretranslate_credential_identifier_edit,
            libretranslate_secret_edit,
            libretranslate_save_credential_button,
            libretranslate_delete_credential_button,
            libretranslate_credential_actions,
        ) = credential_controls(
            "LibreTranslate",
            state.libretranslate_credential_source,
            state.libretranslate_credential_identifier,
        )
        libretranslate_timeout_spin = _double_spin_box(
            state.libretranslate_timeout_seconds,
            QDoubleSpinBox,
        )
        _set_accessible(libretranslate_timeout_spin, "LibreTranslate timeout seconds")
        libretranslate_retry_spin = _int_spin_box(state.libretranslate_retry_count, QSpinBox)
        _set_accessible(libretranslate_retry_spin, "LibreTranslate retry count")
        libretranslate_form.addRow("Base URL", libretranslate_base_url_edit)
        libretranslate_form.addRow("API Key Env", libretranslate_api_key_env_var_edit)
        libretranslate_form.addRow("Credential Source", libretranslate_credential_source_combo)
        libretranslate_form.addRow(
            "Credential Ref",
            libretranslate_credential_identifier_edit,
        )
        libretranslate_form.addRow("Local Secret", libretranslate_credential_actions)
        libretranslate_form.addRow("Timeout", libretranslate_timeout_spin)
        libretranslate_form.addRow("Retry", libretranslate_retry_spin)

        openai_group = QGroupBox("OpenAI")
        openai_form = QFormLayout(openai_group)
        openai_base_url_edit = QLineEdit(state.openai_base_url)
        _set_accessible(openai_base_url_edit, "OpenAI base URL")
        openai_api_key_env_var_edit = QLineEdit(state.openai_api_key_env_var)
        _set_secret_env_accessible(openai_api_key_env_var_edit, "OpenAI API key env var")
        (
            openai_credential_source_combo,
            openai_credential_identifier_edit,
            openai_secret_edit,
            openai_save_credential_button,
            openai_delete_credential_button,
            openai_credential_actions,
        ) = credential_controls(
            "OpenAI",
            state.openai_credential_source,
            state.openai_credential_identifier,
        )
        openai_timeout_spin = _double_spin_box(state.openai_timeout_seconds, QDoubleSpinBox)
        _set_accessible(openai_timeout_spin, "OpenAI timeout seconds")
        openai_retry_spin = _int_spin_box(state.openai_retry_count, QSpinBox)
        _set_accessible(openai_retry_spin, "OpenAI retry count")
        openai_model_edit = QLineEdit(state.openai_model)
        _set_accessible(openai_model_edit, "OpenAI model")
        openai_form.addRow("Base URL", openai_base_url_edit)
        openai_form.addRow("API Key Env", openai_api_key_env_var_edit)
        openai_form.addRow("Credential Source", openai_credential_source_combo)
        openai_form.addRow("Credential Ref", openai_credential_identifier_edit)
        openai_form.addRow("Local Secret", openai_credential_actions)
        openai_form.addRow("Timeout", openai_timeout_spin)
        openai_form.addRow("Retry", openai_retry_spin)
        openai_form.addRow("Model", openai_model_edit)

        deepl_group = QGroupBox("DeepL")
        deepl_form = QFormLayout(deepl_group)
        deepl_base_url_edit = QLineEdit(state.deepl_base_url)
        _set_accessible(deepl_base_url_edit, "DeepL base URL")
        deepl_api_key_env_var_edit = QLineEdit(state.deepl_api_key_env_var)
        _set_secret_env_accessible(deepl_api_key_env_var_edit, "DeepL API key env var")
        (
            deepl_credential_source_combo,
            deepl_credential_identifier_edit,
            deepl_secret_edit,
            deepl_save_credential_button,
            deepl_delete_credential_button,
            deepl_credential_actions,
        ) = credential_controls(
            "DeepL",
            state.deepl_credential_source,
            state.deepl_credential_identifier,
        )
        deepl_timeout_spin = _double_spin_box(state.deepl_timeout_seconds, QDoubleSpinBox)
        _set_accessible(deepl_timeout_spin, "DeepL timeout seconds")
        deepl_retry_spin = _int_spin_box(state.deepl_retry_count, QSpinBox)
        _set_accessible(deepl_retry_spin, "DeepL retry count")
        deepl_model_type_edit = QLineEdit(state.deepl_model_type)
        _set_accessible(deepl_model_type_edit, "DeepL model type")
        deepl_form.addRow("Base URL", deepl_base_url_edit)
        deepl_form.addRow("API Key Env", deepl_api_key_env_var_edit)
        deepl_form.addRow("Credential Source", deepl_credential_source_combo)
        deepl_form.addRow("Credential Ref", deepl_credential_identifier_edit)
        deepl_form.addRow("Local Secret", deepl_credential_actions)
        deepl_form.addRow("Timeout", deepl_timeout_spin)
        deepl_form.addRow("Retry", deepl_retry_spin)
        deepl_form.addRow("Model Type", deepl_model_type_edit)

        history_group = QGroupBox("History")
        history_form = QFormLayout(history_group)
        history_enabled_checkbox = QCheckBox()
        _set_accessible(history_enabled_checkbox, "Enable translation history")
        history_enabled_checkbox.setChecked(state.history_enabled)
        history_max_entries_spin = _int_spin_box(state.history_max_entries, QSpinBox)
        _set_accessible(history_max_entries_spin, "Maximum history entries")
        history_form.addRow("Enabled", history_enabled_checkbox)
        history_form.addRow("Max Entries", history_max_entries_spin)

        setup_tab = QWidget()
        setup_layout = QVBoxLayout(setup_tab)
        setup_layout.addWidget(provider_group)
        setup_layout.addWidget(language_group)
        setup_layout.addStretch(1)

        details_tab = QWidget()
        details_layout = QVBoxLayout(details_tab)
        details_layout.addWidget(libretranslate_group)
        details_layout.addWidget(openai_group)
        details_layout.addWidget(deepl_group)
        details_layout.addStretch(1)

        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)
        history_layout.addWidget(history_group)
        history_layout.addStretch(1)

        settings_tabs.addTab(setup_tab, "Setup")
        settings_tabs.addTab(details_tab, "Provider Details")
        settings_tabs.addTab(history_tab, "History")
        section_layout.addWidget(settings_tabs)
        section_layout.addStretch(1)
        scroll_area.setWidget(scroll_content)
        outer_layout.addWidget(scroll_area)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        save_button = buttons.button(QDialogButtonBox.StandardButton.Save)
        cancel_button = buttons.button(QDialogButtonBox.StandardButton.Cancel)
        if save_button is not None:
            _set_accessible(save_button, "Save Settings")
            save_button.setDefault(True)
        if cancel_button is not None:
            _set_accessible(cancel_button, "Cancel Settings")
        outer_layout.addWidget(buttons)

        dialog.setTabOrder(provider_combo, provider_order_edit)
        dialog.setTabOrder(provider_order_edit, source_lang_edit)
        dialog.setTabOrder(source_lang_edit, target_lang_edit)
        dialog.setTabOrder(target_lang_edit, test_connection_button)
        dialog.setTabOrder(test_connection_button, libretranslate_base_url_edit)
        dialog.setTabOrder(libretranslate_base_url_edit, libretranslate_api_key_env_var_edit)
        dialog.setTabOrder(
            libretranslate_api_key_env_var_edit,
            libretranslate_credential_source_combo,
        )
        dialog.setTabOrder(
            libretranslate_credential_source_combo,
            libretranslate_credential_identifier_edit,
        )
        dialog.setTabOrder(libretranslate_credential_identifier_edit, libretranslate_secret_edit)
        dialog.setTabOrder(libretranslate_secret_edit, libretranslate_save_credential_button)
        dialog.setTabOrder(
            libretranslate_save_credential_button,
            libretranslate_delete_credential_button,
        )
        dialog.setTabOrder(libretranslate_delete_credential_button, libretranslate_timeout_spin)
        dialog.setTabOrder(libretranslate_timeout_spin, libretranslate_retry_spin)
        dialog.setTabOrder(libretranslate_retry_spin, openai_base_url_edit)
        dialog.setTabOrder(openai_base_url_edit, openai_api_key_env_var_edit)
        dialog.setTabOrder(openai_api_key_env_var_edit, openai_credential_source_combo)
        dialog.setTabOrder(openai_credential_source_combo, openai_credential_identifier_edit)
        dialog.setTabOrder(openai_credential_identifier_edit, openai_secret_edit)
        dialog.setTabOrder(openai_secret_edit, openai_save_credential_button)
        dialog.setTabOrder(openai_save_credential_button, openai_delete_credential_button)
        dialog.setTabOrder(openai_delete_credential_button, openai_timeout_spin)
        dialog.setTabOrder(openai_timeout_spin, openai_retry_spin)
        dialog.setTabOrder(openai_retry_spin, openai_model_edit)
        dialog.setTabOrder(openai_model_edit, deepl_base_url_edit)
        dialog.setTabOrder(deepl_base_url_edit, deepl_api_key_env_var_edit)
        dialog.setTabOrder(deepl_api_key_env_var_edit, deepl_credential_source_combo)
        dialog.setTabOrder(deepl_credential_source_combo, deepl_credential_identifier_edit)
        dialog.setTabOrder(deepl_credential_identifier_edit, deepl_secret_edit)
        dialog.setTabOrder(deepl_secret_edit, deepl_save_credential_button)
        dialog.setTabOrder(deepl_save_credential_button, deepl_delete_credential_button)
        dialog.setTabOrder(deepl_delete_credential_button, deepl_timeout_spin)
        dialog.setTabOrder(deepl_timeout_spin, deepl_retry_spin)
        dialog.setTabOrder(deepl_retry_spin, deepl_model_type_edit)
        dialog.setTabOrder(deepl_model_type_edit, history_enabled_checkbox)
        dialog.setTabOrder(history_enabled_checkbox, history_max_entries_spin)

        def current_form_state() -> SettingsFormState:
            return SettingsFormState(
                source_lang=source_lang_edit.text(),
                target_lang=target_lang_edit.text(),
                provider_name=provider_combo.currentText(),
                provider_order=provider_order_edit.text(),
                libretranslate_base_url=libretranslate_base_url_edit.text(),
                libretranslate_api_key_env_var=libretranslate_api_key_env_var_edit.text(),
                libretranslate_credential_source=str(
                    libretranslate_credential_source_combo.currentData() or ""
                ),
                libretranslate_credential_identifier=libretranslate_credential_identifier_edit.text(),
                libretranslate_timeout_seconds=libretranslate_timeout_spin.value(),
                libretranslate_retry_count=libretranslate_retry_spin.value(),
                openai_base_url=openai_base_url_edit.text(),
                openai_api_key_env_var=openai_api_key_env_var_edit.text(),
                openai_credential_source=str(openai_credential_source_combo.currentData() or ""),
                openai_credential_identifier=openai_credential_identifier_edit.text(),
                openai_timeout_seconds=openai_timeout_spin.value(),
                openai_retry_count=openai_retry_spin.value(),
                openai_model=openai_model_edit.text(),
                deepl_base_url=deepl_base_url_edit.text(),
                deepl_api_key_env_var=deepl_api_key_env_var_edit.text(),
                deepl_credential_source=str(deepl_credential_source_combo.currentData() or ""),
                deepl_credential_identifier=deepl_credential_identifier_edit.text(),
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
                credential_result_label.setText("")
                test_connection_button.setEnabled(False)
                return

            readiness_label.setText(setup.status_text)
            readiness_detail_label.setText(setup.detail_text)
            if setup.api_key_env_var:
                env_status = "present" if setup.api_key_present else "missing"
                env_status_label.setText(f"{setup.api_key_env_var}: {env_status}")
            else:
                env_status_label.setText("No API key env var configured.")
            if setup.credential_source == "keyring":
                credential_result_label.setText(setup.credential_status_text)
            elif setup.credential_source == "environment":
                credential_result_label.setText("Credential resolves from environment.")
            else:
                credential_result_label.setText("Credential source follows API key env var.")
            connect_account_button.setToolTip(setup.connect_account_detail)
            test_connection_button.setEnabled(setup.can_test_connection)

        def save_local_credential(provider_name: str, secret_edit: QLineEdit) -> None:
            settings_presenter.apply_state(current_form_state())
            try:
                status = settings_presenter.save_provider_credential(
                    provider_name,
                    secret_edit.text(),
                )
            except Exception as exc:
                refresh_provider_setup()
                credential_result_label.setText(str(exc))
            else:
                secret_edit.clear()
                refresh_provider_setup()
                credential_result_label.setText(status.status_text)

        def delete_local_credential(provider_name: str) -> None:
            settings_presenter.apply_state(current_form_state())
            try:
                status = settings_presenter.delete_provider_credential(provider_name)
            except Exception as exc:
                refresh_provider_setup()
                credential_result_label.setText(str(exc))
            else:
                refresh_provider_setup()
                credential_result_label.setText(status.status_text)

        def apply_settings() -> None:
            settings_presenter.apply_state(current_form_state())
            dialog.accept()

        def run_connection_test() -> None:
            saved_state = settings_presenter.apply_state(current_form_state())
            result = settings_presenter.test_provider_connection(saved_state.provider_name)
            connection_result_label.setText(f"{result.status_text}: {result.detail_text}")
            refresh_provider_setup()

        provider_combo.currentTextChanged.connect(lambda _text: refresh_provider_setup())
        libretranslate_save_credential_button.clicked.connect(
            lambda: save_local_credential("libretranslate", libretranslate_secret_edit)
        )
        libretranslate_delete_credential_button.clicked.connect(
            lambda: delete_local_credential("libretranslate")
        )
        openai_save_credential_button.clicked.connect(
            lambda: save_local_credential("openai", openai_secret_edit)
        )
        openai_delete_credential_button.clicked.connect(lambda: delete_local_credential("openai"))
        deepl_save_credential_button.clicked.connect(
            lambda: save_local_credential("deepl", deepl_secret_edit)
        )
        deepl_delete_credential_button.clicked.connect(lambda: delete_local_credential("deepl"))
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
        status.setObjectName("StatusText")
        empty_label = QLabel("")
        empty_label.setObjectName("SectionLabel")
        empty_label.setWordWrap(True)
        history_list = QListWidget()
        _set_accessible(history_list, "Translation history list")
        copy_history_button = QPushButton("Copy")
        copy_history_button.setIcon(
            app_style.standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton)
        )
        copy_history_button.setIconSize(QSize(16, 16))
        _set_accessible(copy_history_button, "Copy selected history entry")
        delete_history_button = QPushButton("Delete")
        delete_history_button.setIcon(
            app_style.standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton)
        )
        delete_history_button.setIconSize(QSize(16, 16))
        _set_accessible(delete_history_button, "Delete selected history entry")
        clear_history_button = QPushButton("Clear")
        clear_history_button.setIcon(app_style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        clear_history_button.setIconSize(QSize(16, 16))
        _set_accessible(clear_history_button, "Clear translation history")
        close_history_button = QPushButton("Close")
        close_history_button.setIcon(
            app_style.standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton)
        )
        close_history_button.setIconSize(QSize(16, 16))
        _set_accessible(close_history_button, "Close History")
        button_row = QHBoxLayout()
        button_row.addWidget(copy_history_button)
        button_row.addWidget(delete_history_button)
        button_row.addWidget(clear_history_button)
        button_row.addWidget(close_history_button)
        layout.addWidget(status)
        layout.addWidget(empty_label)
        layout.addWidget(history_list)
        layout.addLayout(button_row)
        entry_ids: list[str] = []

        def update_history_buttons() -> None:
            has_selection = selected_entry_id() is not None
            copy_history_button.setEnabled(has_selection)
            delete_history_button.setEnabled(has_selection)
            clear_history_button.setEnabled(bool(entry_ids))

        def refresh_history() -> None:
            state = history_presenter.load_state()
            status.setText(state.status_text)
            history_list.clear()
            entry_ids.clear()
            if not state.history_enabled:
                empty_label.setText(
                    "Enable history in Settings to keep recent successful translations."
                )
            elif not state.entry_views:
                empty_label.setText("No recent translations yet.")
            else:
                empty_label.setText("")
            empty_label.setVisible(bool(empty_label.text()))
            for entry_view in state.entry_views:
                entry_ids.append(entry_view.id)
                item = QListWidgetItem(
                    f"{entry_view.title}\n{entry_view.detail}\n{entry_view.metadata}"
                )
                item.setToolTip(entry_view.detail)
                history_list.addItem(item)
            update_history_buttons()

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

        history_list.currentRowChanged.connect(lambda _row: update_history_buttons())
        copy_history_button.clicked.connect(copy_selected_history)
        delete_history_button.clicked.connect(delete_selected_history)
        clear_history_button.clicked.connect(clear_history)
        close_history_button.clicked.connect(dialog.accept)
        dialog.setTabOrder(history_list, copy_history_button)
        dialog.setTabOrder(copy_history_button, delete_history_button)
        dialog.setTabOrder(delete_history_button, clear_history_button)
        dialog.setTabOrder(clear_history_button, close_history_button)
        refresh_history()
        dialog.resize(640, 420)
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
    primary_actions.setSpacing(10)
    primary_actions.addWidget(translate_button)
    primary_actions.addWidget(translate_screen_button)
    utility_actions = QHBoxLayout()
    utility_actions.setSpacing(10)
    utility_actions.addWidget(settings_button)
    utility_actions.addWidget(history_button)
    utility_actions.addStretch(1)

    result_group = QGroupBox("Result")
    result_layout = QVBoxLayout(result_group)
    result_layout.setSpacing(6)
    result_layout.addWidget(result_state_label)
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

    title_block = QVBoxLayout()
    title_block.setSpacing(2)
    title_block.addWidget(title_label)
    title_block.addWidget(subtitle_label)
    header_layout = QHBoxLayout()
    header_layout.addLayout(title_block)
    header_layout.addStretch(1)
    header_layout.addWidget(status_label, alignment=Qt.AlignmentFlag.AlignTop)

    layout.addLayout(header_layout)
    layout.addLayout(primary_actions)
    layout.addLayout(utility_actions)
    layout.addWidget(result_group)
    refresh_view()

    window.setCentralWidget(central)
    window.setMinimumSize(390, 420)
    window.resize(520, 500)
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


def _set_result_state_property(widget: Any, value: str) -> None:
    widget.setProperty("resultState", value)
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def _set_accessible(widget: Any, name: str, tooltip: str = "") -> None:
    widget.setAccessibleName(name)
    if tooltip:
        widget.setToolTip(tooltip)


def _set_secret_env_accessible(widget: Any, name: str) -> None:
    _set_accessible(
        widget,
        name,
        "Environment variable name only. Do not paste an API key value here.",
    )
