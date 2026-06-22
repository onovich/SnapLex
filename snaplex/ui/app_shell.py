"""Minimal desktop shell for SnapLex."""

from __future__ import annotations

import asyncio
from collections.abc import Callable, Coroutine
from threading import Thread
from typing import Any

from snaplex.services import (
    ClipboardService,
    QtClipboardService,
    create_default_translation_pipeline,
)
from snaplex.services.translation_service import TranslationPipeline
from snaplex.ui.clipboard_presenter import (
    ClipboardTranslationPresenter,
    ClipboardTranslationStatus,
)


def is_pyside_available() -> bool:
    try:
        import PySide6.QtWidgets  # noqa: F401
    except ModuleNotFoundError:
        return False

    return True


def launch_gui(
    presenter: ClipboardTranslationPresenter | None = None,
    clipboard_service: ClipboardService | None = None,
    pipeline: TranslationPipeline | None = None,
) -> int:
    try:
        from PySide6.QtCore import QObject, Qt, Signal
        from PySide6.QtWidgets import (
            QApplication,
            QLabel,
            QMainWindow,
            QPushButton,
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
    pipeline = pipeline or create_default_translation_pipeline()
    presenter = presenter or ClipboardTranslationPresenter(
        on_copy_result=clipboard_service.set_text
    )

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
    copy_button = QPushButton("Copy Result")
    retry_button = QPushButton("Retry")
    close_button = QPushButton("Close Result")
    for label in (status_label, source_label, result_label, provider_label, error_label):
        label.setWordWrap(True)

    def refresh_view() -> None:
        state = presenter.state
        is_loading = state.status == ClipboardTranslationStatus.LOADING
        status_label.setText(state.status_text)
        source_label.setText(state.source_text)
        result_label.setText(state.translated_text)
        provider_label.setText(f"Provider: {state.provider_name}" if state.provider_name else "")
        error_label.setText(state.error_message)
        translate_button.setEnabled(not is_loading)
        copy_button.setEnabled(state.can_copy)
        retry_button.setEnabled(state.can_retry and not is_loading)
        close_button.setEnabled(state.status != ClipboardTranslationStatus.IDLE and not is_loading)

    def run_in_background(operation: Callable[[], Coroutine[Any, Any, object]]) -> None:
        def run_translation() -> None:
            asyncio.run(operation())
            ui_signals.refresh_requested.emit()

        Thread(target=run_translation, daemon=True).start()

    def handle_translate() -> None:
        presenter.request_clipboard_translation()
        refresh_view()
        run_in_background(
            lambda: presenter.translate_clipboard(
                clipboard_service=clipboard_service,
                pipeline=pipeline,
            )
        )

    def handle_retry() -> None:
        presenter.request_clipboard_translation(source_text=presenter.state.source_text)
        refresh_view()
        run_in_background(
            lambda: presenter.retry_translation(
                clipboard_service=clipboard_service,
                pipeline=pipeline,
            )
        )

    def handle_copy() -> None:
        presenter.copy_result()

    def handle_close() -> None:
        presenter.close_result()
        refresh_view()

    ui_signals.refresh_requested.connect(refresh_view)
    translate_button.clicked.connect(handle_translate)
    retry_button.clicked.connect(handle_retry)
    copy_button.clicked.connect(handle_copy)
    close_button.clicked.connect(handle_close)
    layout.addWidget(translate_button)
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
